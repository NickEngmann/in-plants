"""embedded_mocks.py — Shared hardware mock library for testing embedded projects.

Import these mocks in your test files:
    from embedded_mocks import MockI2C, MockSPI, MockUART, MockGPIO, MockNeoPixel, ...

All mocks track state so tests can assert pin values, bytes sent, etc.
"""
from unittest.mock import MagicMock


# ── GPIO Pin Simulator ──────────────────────────────────────────────────────
class MockGPIO:
    """Simulates GPIO pins with state tracking."""
    HIGH = 1
    LOW = 0
    INPUT = 0
    OUTPUT = 1
    INPUT_PULLUP = 2
    BCM = 11
    BOARD = 10
    PUD_UP = 22
    PUD_DOWN = 21

    def __init__(self):
        self._mode = None
        self._pins = {}  # pin -> {mode, value, pud}
        self._warnings = True

    def setmode(self, mode):
        self._mode = mode

    def setup(self, pin, mode, pull_up_down=None):
        if isinstance(pin, (list, tuple)):
            for p in pin:
                self.setup(p, mode, pull_up_down)
            return
        self._pins[pin] = {"mode": mode, "value": self.LOW, "pud": pull_up_down}

    def output(self, pin, value):
        if isinstance(pin, (list, tuple)):
            vals = value if isinstance(value, (list, tuple)) else [value] * len(pin)
            for p, v in zip(pin, vals):
                self.output(p, v)
            return
        if pin in self._pins:
            self._pins[pin]["value"] = value

    def input(self, pin):
        return self._pins.get(pin, {}).get("value", self.LOW)

    def cleanup(self):
        self._pins.clear()
        self._mode = None

    def setwarnings(self, flag):
        self._warnings = flag


# ── I2C Bus Simulator ───────────────────────────────────────────────────────
class MockI2C:
    """Simulates an I2C bus — tracks writes and returns configurable read data."""

    def __init__(self, scl=None, sda=None, frequency=100000):
        self.scl = scl
        self.sda = sda
        self.frequency = frequency
        self.written = []  # list of (address, bytes)
        self._read_responses = {}  # address -> bytes to return on read

    def writeto(self, address, buffer, *, start=0, end=None):
        self.written.append((address, bytes(buffer[start:end])))

    def readfrom_into(self, address, buffer, *, start=0, end=None):
        data = self._read_responses.get(address, b"\x00" * len(buffer))
        end = end or len(buffer)
        for i in range(start, min(end, len(buffer))):
            if i - start < len(data):
                buffer[i] = data[i - start]

    def writeto_then_readfrom(self, address, out_buffer, in_buffer,
                               *, out_start=0, out_end=None, in_start=0, in_end=None):
        self.writeto(address, out_buffer, start=out_start, end=out_end)
        self.readfrom_into(address, in_buffer, start=in_start, end=in_end)

    def scan(self):
        return list(self._read_responses.keys())

    def set_read_response(self, address, data):
        """Configure what readfrom_into returns for a given address."""
        self._read_responses[address] = data

    def try_lock(self):
        return True

    def unlock(self):
        pass


# ── SPI Bus Simulator ───────────────────────────────────────────────────────
class MockSPI:
    """Simulates an SPI bus with MOSI/MISO tracking."""

    def __init__(self, clock=None, MOSI=None, MISO=None, baudrate=1000000):
        self.clock = clock
        self.MOSI = MOSI
        self.MISO = MISO
        self.baudrate = baudrate
        self.written = bytearray()
        self._read_data = bytearray()

    def write(self, buffer):
        self.written.extend(buffer)

    def readinto(self, buffer):
        for i in range(len(buffer)):
            if i < len(self._read_data):
                buffer[i] = self._read_data[i]
            else:
                buffer[i] = 0

    def write_readinto(self, out_buffer, in_buffer):
        self.write(out_buffer)
        self.readinto(in_buffer)

    def set_read_data(self, data):
        self._read_data = bytearray(data)

    def try_lock(self):
        return True

    def unlock(self):
        pass

    def configure(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


# ── UART / Serial Simulator ─────────────────────────────────────────────────
class MockUART:
    """Simulates UART / serial communication with configurable rx buffer."""

    def __init__(self, tx=None, rx=None, baudrate=9600, timeout=1):
        self.tx = tx
        self.rx = rx
        self.baudrate = baudrate
        self.timeout = timeout
        self._rx_buffer = bytearray()
        self._tx_log = bytearray()

    def write(self, data):
        if isinstance(data, str):
            data = data.encode()
        self._tx_log.extend(data)
        return len(data)

    def read(self, nbytes=None):
        if nbytes is None:
            data = bytes(self._rx_buffer)
            self._rx_buffer.clear()
            return data
        data = bytes(self._rx_buffer[:nbytes])
        self._rx_buffer = self._rx_buffer[nbytes:]
        return data

    def readline(self):
        idx = self._rx_buffer.find(b"\n")
        if idx == -1:
            return self.read()
        data = bytes(self._rx_buffer[:idx + 1])
        self._rx_buffer = self._rx_buffer[idx + 1:]
        return data

    @property
    def in_waiting(self):
        return len(self._rx_buffer)

    def inject_rx(self, data):
        """Inject data into the receive buffer for test simulation."""
        if isinstance(data, str):
            data = data.encode()
        self._rx_buffer.extend(data)

    def reset_input_buffer(self):
        self._rx_buffer.clear()

    def close(self):
        pass


# ── NeoPixel Simulator ──────────────────────────────────────────────────────
class MockNeoPixel:
    """Simulates a NeoPixel strip — tracks color values per pixel."""

    def __init__(self, pin=None, n=1, brightness=1.0, auto_write=True, pixel_order="GRB"):
        self.pin = pin
        self.n = n
        self.brightness = brightness
        self.auto_write = auto_write
        self._pixels = [(0, 0, 0)] * n
        self._shown = False

    def __setitem__(self, idx, color):
        if isinstance(idx, slice):
            indices = range(*idx.indices(self.n))
            for i in indices:
                self._pixels[i] = color
        else:
            self._pixels[idx] = color

    def __getitem__(self, idx):
        return self._pixels[idx]

    def __len__(self):
        return self.n

    def fill(self, color):
        self._pixels = [color] * self.n

    def show(self):
        self._shown = True

    def deinit(self):
        pass


# ── Display Simulators ──────────────────────────────────────────────────────
class MockSSD1306:
    """Simulates an SSD1306 OLED display (128x64 or 128x32)."""

    def __init__(self, width=128, height=64, i2c=None, addr=0x3C):
        self.width = width
        self.height = height
        self.i2c = i2c
        self.addr = addr
        self._buffer = bytearray(width * height // 8)
        self._shown = False
        self.rotation = 0

    def fill(self, color):
        val = 0xFF if color else 0x00
        for i in range(len(self._buffer)):
            self._buffer[i] = val

    def text(self, text, x, y, color=1):
        pass  # Text rendering is display-internal

    def show(self):
        self._shown = True

    def pixel(self, x, y, color=None):
        if color is not None:
            pass  # Set pixel
        return 0

    def fill_rect(self, x, y, w, h, color):
        pass

    def rect(self, x, y, w, h, color):
        pass

    def line(self, x0, y0, x1, y1, color):
        pass

    def invert(self, flag):
        pass

    @property
    def poweron(self):
        return True


class MockHT16K33:
    """Simulates an HT16K33 LED matrix/7-segment backpack."""

    def __init__(self, i2c=None, address=0x70):
        self.i2c = i2c
        self.address = address
        self._buffer = [0] * 16
        self.brightness = 1.0
        self.blink_rate = 0
        self.auto_write = True

    def fill(self, color):
        val = 0xFF if color else 0x00
        self._buffer = [val] * 16

    def show(self):
        pass

    def __setitem__(self, idx, val):
        if idx < len(self._buffer):
            self._buffer[idx] = val

    def __getitem__(self, idx):
        return self._buffer[idx] if idx < len(self._buffer) else 0


class MockSeg7x4(MockHT16K33):
    """Simulates a 4-digit 7-segment display."""

    def __init__(self, i2c=None, address=0x70):
        super().__init__(i2c, address)
        self._text = "    "
        self.colon = False

    def print(self, value):
        self._text = str(value)[:4]

    def marquee(self, text, delay=0.25, loop=True):
        self._text = text[:4]

    @property
    def text(self):
        return self._text


# ── Rotary Encoder Simulator ────────────────────────────────────────────────
class MockRotaryEncoder:
    """Simulates a rotary encoder with position and button."""

    def __init__(self, pin_a=None, pin_b=None, pin_button=None):
        self._position = 0
        self._last_position = 0
        self._button_pressed = False

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, val):
        self._last_position = self._position
        self._position = val

    def simulate_turn(self, clicks):
        """Simulate turning the encoder by N clicks (positive=CW, negative=CCW)."""
        self._last_position = self._position
        self._position += clicks

    def simulate_press(self):
        self._button_pressed = True

    def simulate_release(self):
        self._button_pressed = False


# ── ADC / PWM / DAC Simulators ──────────────────────────────────────────────
class MockADC:
    """Simulates an analog-to-digital converter."""

    def __init__(self, pin=None, bits=10):
        self.pin = pin
        self.bits = bits
        self._value = 0
        self._voltage = 0.0

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, v):
        self._value = max(0, min(v, (2 ** self.bits) - 1))

    @property
    def voltage(self):
        return self._voltage

    def set_voltage(self, v, ref=3.3):
        """Set the simulated voltage and update the raw value accordingly."""
        self._voltage = v
        self._value = int((v / ref) * ((2 ** self.bits) - 1))


class MockPWM:
    """Simulates a PWM output."""

    def __init__(self, pin=None, frequency=1000, duty_cycle=0):
        self.pin = pin
        self.frequency = frequency
        self.duty_cycle = duty_cycle

    def deinit(self):
        pass


class MockDAC:
    """Simulates a digital-to-analog converter."""

    def __init__(self, pin=None):
        self.pin = pin
        self._value = 0

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, v):
        self._value = max(0, min(v, 65535))


# ── Sensor Simulators ───────────────────────────────────────────────────────
class MockTemperatureSensor:
    """Generic temperature sensor mock (DHT, BME280, etc.)."""

    def __init__(self, temp_c=22.0, humidity=50.0, pressure=1013.25):
        self.temperature = temp_c
        self.humidity = humidity
        self.pressure = pressure
        self.altitude = 0.0

    def set_reading(self, temp_c=None, humidity=None, pressure=None):
        if temp_c is not None:
            self.temperature = temp_c
        if humidity is not None:
            self.humidity = humidity
        if pressure is not None:
            self.pressure = pressure


class MockAccelerometer:
    """Simulates a 3-axis accelerometer (MPU6050, LIS3DH, etc.)."""

    def __init__(self):
        self._acceleration = (0.0, 0.0, 9.8)
        self._gyro = (0.0, 0.0, 0.0)

    @property
    def acceleration(self):
        return self._acceleration

    def set_acceleration(self, x, y, z):
        self._acceleration = (x, y, z)

    @property
    def gyro(self):
        return self._gyro

    def set_gyro(self, x, y, z):
        self._gyro = (x, y, z)


# ── ESP32-Specific Mocks ────────────────────────────────────────────────────
class MockWiFi:
    """Simulates ESP32 WiFi module."""

    def __init__(self):
        self.ssid = ""
        self._connected = False
        self._ip = "192.168.1.100"
        self.radio = self  # CircuitPython wifi.radio pattern

    def connect(self, ssid, password="", **kwargs):
        self.ssid = ssid
        self._connected = True

    def disconnect(self):
        self._connected = False
        self.ssid = ""

    @property
    def connected(self):
        return self._connected

    @property
    def ipv4_address(self):
        return self._ip if self._connected else None

    @property
    def ap_info(self):
        return MagicMock(ssid=self.ssid, rssi=-50) if self._connected else None


class MockBLE:
    """Simulates BLE peripheral/central."""

    def __init__(self):
        self._advertising = False
        self._connected = False
        self._services = []
        self._scan_results = []

    def start_advertising(self, advertisement=None, scan_response=None):
        self._advertising = True

    def stop_advertising(self):
        self._advertising = False

    def start_scan(self, *args, **kwargs):
        return iter(self._scan_results)

    def stop_scan(self):
        pass

    @property
    def connected(self):
        return self._connected

    def add_scan_result(self, name="device", rssi=-60, address="AA:BB:CC:DD:EE:FF"):
        self._scan_results.append(MagicMock(
            complete_name=name, rssi=rssi, address=MagicMock(string=address)))


class MockPreferences:
    """Simulates ESP32 Preferences / NVS storage."""

    def __init__(self, namespace="app"):
        self.namespace = namespace
        self._storage = {}

    def begin(self, namespace=None, read_only=False):
        if namespace:
            self.namespace = namespace

    def end(self):
        pass

    def put_string(self, key, value):
        self._storage[f"{self.namespace}:{key}"] = value

    def get_string(self, key, default=""):
        return self._storage.get(f"{self.namespace}:{key}", default)

    def put_int(self, key, value):
        self._storage[f"{self.namespace}:{key}"] = value

    def get_int(self, key, default=0):
        return self._storage.get(f"{self.namespace}:{key}", default)

    def put_float(self, key, value):
        self._storage[f"{self.namespace}:{key}"] = value

    def get_float(self, key, default=0.0):
        return self._storage.get(f"{self.namespace}:{key}", default)

    def remove(self, key):
        self._storage.pop(f"{self.namespace}:{key}", None)

    def clear(self):
        prefix = f"{self.namespace}:"
        self._storage = {k: v for k, v in self._storage.items() if not k.startswith(prefix)}


class MockSPIFFS:
    """Simulates ESP32 SPIFFS / LittleFS filesystem."""

    def __init__(self):
        self._files = {}
        self._mounted = False

    def mount(self, path="/spiffs"):
        self._mounted = True

    def open(self, path, mode="r"):
        if "w" in mode:
            self._files[path] = ""
            return MockFile(self._files, path, mode)
        if path in self._files:
            return MockFile(self._files, path, mode)
        raise FileNotFoundError(f"No such file: {path}")

    def exists(self, path):
        return path in self._files

    def listdir(self, path="/"):
        return [k for k in self._files.keys() if k.startswith(path)]

    def remove(self, path):
        self._files.pop(path, None)


class MockFile:
    """Helper for MockSPIFFS file operations."""

    def __init__(self, storage, path, mode):
        self._storage = storage
        self._path = path
        self._mode = mode

    def read(self):
        return self._storage.get(self._path, "")

    def write(self, data):
        self._storage[self._path] = data

    def close(self):
        pass

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()


# ── Convenience: Arduino-compatible helpers ──────────────────────────────────
def arduino_map(x, in_min, in_max, out_min, out_max):
    """Arduino map() function re-implemented in Python."""
    return int((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)


def arduino_constrain(x, a, b):
    """Arduino constrain() function."""
    return max(a, min(x, b))


def millis_to_seconds(ms):
    """Convert Arduino millis() to seconds."""
    return ms / 1000.0


def analog_to_voltage(raw, bits=10, ref=3.3):
    """Convert raw ADC reading to voltage."""
    return (raw / ((2 ** bits) - 1)) * ref

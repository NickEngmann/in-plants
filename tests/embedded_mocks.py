"""Mock objects and helpers for testing Arduino code in Python.

This module re-implements Arduino-like functions and provides mock objects
for hardware interfaces to enable unit testing in Python.
"""
import pytest


class ArduinoConstants:
    """Arduino-like constants for testing."""
    HIGH = 1
    LOW = 0
    
    # Analog pins
    A0 = 14
    A1 = 15
    A2 = 16
    A3 = 17
    A4 = 18
    A5 = 19


def arduino_map(x, in_min, in_max, out_min, out_max):
    """Re-implementation of Arduino map() function."""
    return (x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min


def arduino_constrain(x, a, b):
    """Re-implementation of Arduino constrain() function."""
    return max(a, min(x, b))


def analog_to_voltage(value, bits=10, ref=3.3):
    """Convert ADC raw value to voltage."""
    max_value = 2 ** bits - 1
    return (value / max_value) * ref


class MockI2C:
    """Mock I2C bus for testing."""
    def __init__(self, sda=4, scl=5, freq=100000):
        self.sda = sda
        self.scl = scl
        self.freq = freq
        self._devices = []
        self._tx_buffer = b""
        self._rx_buffer = b""
    
    def scan(self):
        """Return list of connected devices."""
        return self._devices
    
    def start(self, address, write=True):
        """Start transmission to address."""
        pass
    
    def stop(self):
        """Stop transmission."""
        pass
    
    def write(self, data):
        """Write data to bus."""
        if isinstance(data, str):
            data = data.encode()
        self._tx_buffer += data
        return len(data)
    
    def read(self, nbyte=-1):
        """Read data from bus."""
        if nbyte == -1:
            result = self._rx_buffer
            self._rx_buffer = b""
            return result
        result = self._rx_buffer[:nbyte]
        self._rx_buffer = self._rx_buffer[nbyte:]
        return result


class MockSPI:
    """Mock SPI bus for testing."""
    def __init__(self, sck=13, miso=12, mosi=11, cs=8):
        self.sck = sck
        self.miso = miso
        self.mosi = mosi
        self.cs = cs
        self._tx_buffer = b""
    
    def begin(self, cs=None):
        """Initialize SPI."""
        if cs is not None:
            self.cs = cs
    
    def transfer(self, data):
        """Send and receive data simultaneously."""
        if isinstance(data, str):
            data = data.encode()
        self._tx_buffer += data
        return b"\x00" * len(data)


class MockUART:
    """Mock UART/Serial for testing."""
    def __init__(self, baudrate=115200, rx_size=256, tx_size=256):
        self.baudrate = baudrate
        self._tx_log = b""
        self._rx_buffer = b""
        self._rx_size = rx_size
        self._tx_size = tx_size
    
    def begin(self, baudrate):
        """Initialize UART with baudrate."""
        self.baudrate = baudrate
    
    def write(self, data):
        """Write data to UART."""
        if isinstance(data, str):
            data = data.encode()
        self._tx_log += data
        return len(data)
    
    def read(self, nbyte=-1):
        """Read data from UART."""
        if nbyte == -1:
            result = self._rx_buffer
            self._rx_buffer = b""
            return result
        result = self._rx_buffer[:nbyte]
        self._rx_buffer = self._rx_buffer[nbyte:]
        return result
    
    def readline(self):
        """Read a line from UART."""
        if b"\n" in self._rx_buffer:
            idx = self._rx_buffer.index(b"\n") + 1
            result = self._rx_buffer[:idx]
            self._rx_buffer = self._rx_buffer[idx:]
            return result
        return b""
    
    def available(self):
        """Return number of bytes available for reading."""
        return len(self._rx_buffer)
    
    def inject_rx(self, data):
        """Inject data into RX buffer (simulate incoming data)."""
        if isinstance(data, str):
            data = data.encode()
        self._rx_buffer += data
    
    def flush(self):
        """Wait for transmission to complete."""
        pass


class MockGPIO:
    """Mock GPIO for testing."""
    def __init__(self):
        self._pins = {}
    
    def pinMode(self, pin, mode):
        """Set pin mode."""
        self._pins[pin] = {"mode": mode, "value": 0}
    
    def digitalWrite(self, pin, value):
        """Set pin value."""
        if pin in self._pins:
            self._pins[pin]["value"] = value
    
    def digitalRead(self, pin):
        """Read pin value."""
        if pin in self._pins:
            return self._pins[pin]["value"]
        return 0
    
    def analogRead(self, pin):
        """Read analog value."""
        # Default to simulated value
        return 512


class MockNeoPixel:
    """Mock NeoPixel/WS2812 for testing."""
    def __init__(self, pin, n, bpp=3, brightness=1.0, auto_write=True):
        self.pin = pin
        self.n = n
        self.bpp = bpp
        self.brightness = brightness
        self.auto_write = auto_write
        self.pixels = [(0, 0, 0)] * n
    
    def fill(self, color):
        """Fill all pixels with color."""
        self.pixels = [color] * self.n
    
    def show(self):
        """Update pixels."""
        pass
    
    def __setitem__(self, idx, color):
        if isinstance(idx, int):
            self.pixels[idx] = color
        else:
            for i in range(*idx.indices(self.n)):
                self.pixels[i] = color
    
    def __getitem__(self, idx):
        return self.pixels[idx]


class MockWiFi:
    """Mock WiFi for testing."""
    def __init__(self):
        self.connected = False
        self.ssid = ""
        self.password = ""
    
    def begin(self, ssid, password=None):
        """Connect to WiFi."""
        self.ssid = ssid
        self.password = password
        self.connected = True
        return True
    
    def status(self):
        """Return connection status."""
        return 3 if self.connected else 0  # WL_CONNECTED = 3
    
    def localIP(self):
        """Return local IP address."""
        return (192, 168, 1, 100) if self.connected else (0, 0, 0, 0)


class MockBLE:
    """Mock BLE for testing."""
    def __init__(self):
        self.connected = False
        self._tx_buffer = b""
    
    def begin(self):
        """Initialize BLE."""
        pass
    
    def available(self):
        """Return number of bytes available."""
        return len(self._tx_buffer)
    
    def read(self, nbyte=-1):
        """Read from BLE."""
        if nbyte == -1:
            result = self._tx_buffer
            self._tx_buffer = b""
            return result
        result = self._tx_buffer[:nbyte]
        self._tx_buffer = self._tx_buffer[nbyte:]
        return result
    
    def write(self, data):
        """Write to BLE."""
        if isinstance(data, str):
            data = data.encode()
        self._tx_buffer += data
        return len(data)


class MockPreferences:
    """Mock Preferences (non-volatile storage) for testing."""
    def __init__(self):
        self._data = {}
    
    def begin(self, namespace, read_only=False):
        """Begin preferences session."""
        pass
    
    def end(self):
        """End preferences session."""
        pass
    
    def putInt(self, key, value):
        """Store integer."""
        self._data[key] = value
    
    def getInt(self, key, default=0):
        """Retrieve integer."""
        return self._data.get(key, default)
    
    def putString(self, key, value):
        """Store string."""
        self._data[key] = value
    
    def getString(self, key, default=""):
        """Retrieve string."""
        return self._data.get(key, default)
    
    def remove(self, key):
        """Remove key."""
        if key in self._data:
            del self._data[key]


@pytest.fixture
def arduino():
    """Provides Arduino-like constants and helpers for testing."""
    return ArduinoConstants()


@pytest.fixture
def i2c():
    """Provides a mock I2C bus."""
    return MockI2C()


@pytest.fixture
def spi():
    """Provides a mock SPI bus."""
    return MockSPI()


@pytest.fixture
def uart():
    """Provides a mock UART/Serial."""
    return MockUART(baudrate=115200)


@pytest.fixture
def gpio():
    """Provides a mock GPIO controller."""
    return MockGPIO()


@pytest.fixture
def neopixel():
    """Provides a mock NeoPixel strip."""
    return MockNeoPixel(pin=12, n=8)


@pytest.fixture
def wifi():
    """Provides a mock WiFi connection."""
    return MockWiFi()


@pytest.fixture
def ble():
    """Provides a mock BLE connection."""
    return MockBLE()


@pytest.fixture
def preferences():
    """Provides mock non-volatile storage."""
    return MockPreferences()

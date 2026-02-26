"""embedded_mocks.py — Mocks for Arduino embedded systems testing."""


class MockI2C:
    """Mock I2C bus for testing."""
    def __init__(self, sda=21, scl=22, freq=100000):
        self.sda = sda
        self.scl = scl
        self.freq = freq
        self._tx_buffer = b""
        self._rx_buffer = b""
        self.addresses = {}

    def write(self, data):
        """Write data to I2C."""
        self._tx_buffer = data

    def read(self, n_bytes=1):
        """Read n_bytes from I2C."""
        result = self._rx_buffer[:n_bytes]
        self._rx_buffer = self._rx_buffer[n_bytes:]
        return result

    def scan(self):
        """Scan for I2C devices."""
        return list(self.addresses.keys())


class MockSPI:
    """Mock SPI bus for testing."""
    def __init__(self, sck=18, miso=19, mosi=23, cs=5):
        self.sck = sck
        self.miso = miso
        self.mosi = mosi
        self.cs = cs
        self._tx_buffer = b""
        self._rx_buffer = b""

    def write(self, data):
        """Write data to SPI."""
        self._tx_buffer = data

    def read(self, n_bytes=1):
        """Read n_bytes from SPI."""
        return self._rx_buffer[:n_bytes]

    def transfer(self, data):
        """Full duplex SPI transfer."""
        self._tx_buffer = data
        return self._rx_buffer


class MockUART:
    """Mock UART/Serial for testing."""
    def __init__(self, baudrate=115200, rx_size=256, tx_size=256):
        self.baudrate = baudrate
        self._tx_log = b""
        self._rx_buffer = b""

    def begin(self, baudrate):
        """Initialize UART with baudrate."""
        self.baudrate = baudrate

    def write(self, data):
        """Write data to UART."""
        if isinstance(data, str):
            data = data.encode()
        self._tx_log += data

    def read(self, n_bytes=1):
        """Read n_bytes from UART."""
        result = self._rx_buffer[:n_bytes]
        self._rx_buffer = self._rx_buffer[n_bytes:]
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
        """Inject data into RX buffer."""
        if isinstance(data, str):
            data = data.encode()
        self._rx_buffer += data


class MockGPIO:
    """Mock GPIO for testing."""
    def __init__(self):
        self.pins = {}

    def pinMode(self, pin, mode):
        """Set pin mode."""
        self.pins[pin] = {"mode": mode, "value": 0}

    def digitalWrite(self, pin, value):
        """Set pin value."""
        if pin in self.pins:
            self.pins[pin]["value"] = value

    def digitalRead(self, pin):
        """Read pin value."""
        if pin in self.pins:
            return self.pins[pin]["value"]
        return 0

    def analogRead(self, pin):
        """Read analog value (0-1023 for 10-bit ADC)."""
        return 0


class MockNeoPixel:
    """Mock NeoPixel/WS2812 for testing."""
    def __init__(self, pin, n_pixels, brightness=1.0):
        self.pin = pin
        self.n_pixels = n_pixels
        self.pixels = [(0, 0, 0)] * n_pixels
        self.brightness = brightness

    def setPixelColor(self, index, r, g, b):
        """Set pixel color."""
        if 0 <= index < self.n_pixels:
            self.pixels[index] = (r, g, b)

    def setPixelColor(self, index, color):
        """Set pixel color from packed integer."""
        if 0 <= index < self.n_pixels:
            r = (color >> 16) & 0xFF
            g = (color >> 8) & 0xFF
            b = color & 0xFF
            self.pixels[index] = (r, g, b)

    def show(self):
        """Update LEDs."""
        pass


class MockWiFi:
    """Mock WiFi for testing."""
    def __init__(self):
        self.connected = False
        self.ssid = ""
        self.ip = "192.168.1.100"

    def begin(self, ssid, passkey):
        """Connect to WiFi."""
        self.ssid = ssid
        self.connected = True

    def status(self):
        """Return connection status."""
        return 3 if self.connected else 0  # WL_CONNECTED = 3

    def localIP(self):
        """Return local IP address."""
        return self.ip


class MockBLE:
    """Mock BLE for testing."""
    def __init__(self):
        self.connected = False
        self.name = ""

    def begin(self, name):
        """Initialize BLE."""
        self.name = name

    def connected(self):
        """Check if connected."""
        return self.connected


class MockPreferences:
    """Mock Preferences (EEPROM-like storage) for testing."""
    def __init__(self):
        self.data = {}

    def begin(self, namespace):
        """Begin preferences session."""
        pass

    def putInt(self, key, value):
        """Store integer."""
        self.data[key] = value

    def getInt(self, key, default=0):
        """Retrieve integer."""
        return self.data.get(key, default)

    def putString(self, key, value):
        """Store string."""
        self.data[key] = value

    def getString(self, key, default=""):
        """Retrieve string."""
        return self.data.get(key, default)


def arduino_map(x, in_min, in_max, out_min, out_max):
    """Re-implementation of Arduino map() function."""
    return (x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min


def arduino_constrain(x, a, b):
    """Re-implementation of Arduino constrain() function."""
    return max(a, min(x, b))


def analog_to_voltage(raw, bits=10, ref=3.3):
    """Convert ADC raw value to voltage."""
    max_val = (1 << bits) - 1
    return (raw / max_val) * ref

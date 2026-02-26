"""Mock libraries for Arduino/embedded C testing in Python.

This module provides mock implementations of common Arduino libraries
(I2C, SPI, UART, GPIO, WiFi, BLE, etc.) that can be used in Python tests.
"""


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
    """Re-implementation of Arduino's map() function."""
    return (x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min


def arduino_constrain(x, a, b):
    """Re-implementation of Arduino's constrain() function."""
    return max(a, min(x, b))


def analog_to_voltage(value, bits=10, ref=3.3):
    """Convert ADC raw value to voltage.
    
    Args:
        value: Raw ADC value
        bits: ADC resolution (default 10 bits = 1024 steps)
        ref: Reference voltage (default 3.3V)
    
    Returns:
        Voltage corresponding to the ADC value
    """
    max_value = 2 ** bits - 1
    return (value / max_value) * ref


class MockI2C:
    """Mock I2C bus for testing."""
    def __init__(self, sda=18, scl=19, frequency=100000):
        self.sda = sda
        self.scl = scl
        self.frequency = frequency
        self._tx_buffer = bytearray()
        self._rx_buffer = bytearray()
        self._address = None
    
    def begin(self, address=None):
        """Initialize I2C as master or slave."""
        self._address = address
        return True
    
    def beginTransmission(self, address):
        """Begin transmission to a slave device."""
        self._address = address
        self._tx_buffer = bytearray()
        return True
    
    def write(self, data):
        """Write data to the transmission buffer."""
        if isinstance(data, int):
            self._tx_buffer.append(data & 0xFF)
        else:
            self._tx_buffer.extend(data)
        return len(data) if isinstance(data, bytes) else 1
    
    def endTransmission(self):
        """End transmission and send data."""
        return 0  # Success
    
    def requestFrom(self, address, quantity):
        """Request data from a slave device."""
        self._rx_buffer = bytearray(quantity)
        return quantity
    
    def available(self):
        """Return number of bytes available for reading."""
        return len(self._rx_buffer)
    
    def read(self):
        """Read a byte from the receive buffer."""
        if self._rx_buffer:
            return self._rx_buffer.pop(0)
        return 0


class MockSPI:
    """Mock SPI bus for testing."""
    def __init__(self, sck=13, miso=12, mosi=11, cs=8):
        self.sck = sck
        self.miso = miso
        self.mosi = mosi
        self.cs = cs
        self._tx_buffer = bytearray()
        self._rx_buffer = bytearray()
    
    def begin(self):
        """Initialize SPI."""
        return True
    
    def transfer(self, data):
        """Transfer data over SPI (full duplex)."""
        if isinstance(data, int):
            self._tx_buffer.append(data)
            return data
        else:
            self._tx_buffer.extend(data)
            return data
    
    def write(self, data):
        """Write data to SPI."""
        if isinstance(data, int):
            self._tx_buffer.append(data)
        else:
            self._tx_buffer.extend(data)
        return len(data) if isinstance(data, bytes) else 1
    
    def read(self):
        """Read data from SPI."""
        if self._rx_buffer:
            return self._rx_buffer.pop(0)
        return 0


class MockUART:
    """Mock UART/Serial for testing."""
    def __init__(self, baudrate=9600, tx_pin=1, rx_pin=3):
        self.baudrate = baudrate
        self.tx_pin = tx_pin
        self.rx_pin = rx_pin
        self._tx_log = bytearray()
        self._rx_buffer = bytearray()
        self._rx_position = 0
    
    def begin(self, baudrate):
        """Initialize UART with specified baudrate."""
        self.baudrate = baudrate
        return True
    
    def write(self, data):
        """Write data to UART."""
        if isinstance(data, str):
            data = data.encode()
        self._tx_log.extend(data)
        return len(data)
    
    def println(self, data):
        """Write data with newline to UART."""
        if isinstance(data, str):
            data = data.encode()
        self._tx_log.extend(data + b"\n")
        return len(data) + 1
    
    def available(self):
        """Return number of bytes available for reading."""
        return len(self._rx_buffer) - self._rx_position
    
    def read(self, size=None):
        """Read bytes from UART."""
        if size is None:
            size = self.available()
        data = self._rx_buffer[self._rx_position:self._rx_position + size]
        self._rx_position += len(data)
        return bytes(data)
    
    def readline(self):
        """Read a line from UART."""
        if b"\n" in self._rx_buffer[self._rx_position:]:
            end = self._rx_buffer.index(b"\n", self._rx_position) + 1
            data = self._rx_buffer[self._rx_position:end]
            self._rx_position = end
            return bytes(data)
        return b""
    
    def inject_rx(self, data):
        """Inject data into the receive buffer."""
        if isinstance(data, str):
            data = data.encode()
        self._rx_buffer.extend(data)
        self._rx_position = 0
    
    def flush(self):
        """Flush the transmit buffer."""
        self._tx_log = bytearray()


class MockGPIO:
    """Mock GPIO for testing."""
    def __init__(self):
        self._pins = {}
        self._mode = {}
    
    def pinMode(self, pin, mode):
        """Set pin mode."""
        self._mode[pin] = mode
    
    def digitalWrite(self, pin, value):
        """Write a value to a pin."""
        self._pins[pin] = value
    
    def digitalRead(self, pin):
        """Read a value from a pin."""
        return self._pins.get(pin, 0)
    
    def analogRead(self, pin):
        """Read analog value from a pin."""
        return self._pins.get(pin, 0)


class MockNeoPixel:
    """Mock NeoPixel/WS2812 LED for testing."""
    def __init__(self, pin, n, bpp=3, brightness=1.0):
        self.pin = pin
        self.n = n
        self.bpp = bpp
        self.brightness = brightness
        self._pixels = [(0, 0, 0)] * n
        self._show_called = False
    
    def begin(self):
        """Initialize NeoPixel."""
        pass
    
    def setPixelColor(self, n, color):
        """Set the color of a pixel."""
        if 0 <= n < self.n:
            self._pixels[n] = color
    
    def show(self):
        """Update the LED strip."""
        self._show_called = True
    
    def getPixelColor(self, n):
        """Get the color of a pixel."""
        if 0 <= n < self.n:
            return self._pixels[n]
        return 0


class MockWiFi:
    """Mock WiFi for testing."""
    def __init__(self):
        self._connected = False
        self._ssid = None
        self._password = None
    
    def begin(self, ssid, password=None):
        """Connect to a WiFi network."""
        self._ssid = ssid
        self._password = password
        self._connected = True
        return True
    
    def status(self):
        """Return WiFi status."""
        return 3 if self._connected else 0  # WL_CONNECTED = 3
    
    def connected(self):
        """Return whether WiFi is connected."""
        return self._connected
    
    def localIP(self):
        """Return local IP address."""
        return (192, 168, 1, 100) if self._connected else (0, 0, 0, 0)


class MockBLE:
    """Mock BLE for testing."""
    def __init__(self):
        self._connected = False
        self._name = None
    
    def begin(self, name):
        """Initialize BLE."""
        self._name = name
        return True
    
    def connected(self):
        """Return whether BLE is connected."""
        return self._connected
    
    def write(self, data):
        """Write data over BLE."""
        return len(data)
    
    def available(self):
        """Return number of bytes available for reading."""
        return 0
    
    def read(self):
        """Read data from BLE."""
        return b""


class MockPreferences:
    """Mock Preferences (non-volatile storage) for testing."""
    def __init__(self):
        self._data = {}
    
    def begin(self, namespace, read_only=False):
        """Begin a preferences session."""
        self._namespace = namespace
        return True
    
    def putInt(self, key, value):
        """Store an integer."""
        self._data[key] = value
        return True
    
    def getInt(self, key, default=0):
        """Retrieve an integer."""
        return self._data.get(key, default)
    
    def putString(self, key, value):
        """Store a string."""
        self._data[key] = value
        return True
    
    def getString(self, key, default=""):
        """Retrieve a string."""
        return self._data.get(key, default)

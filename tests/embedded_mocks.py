"""Mock libraries for Arduino/C++ embedded systems testing.

Provides mock implementations for common embedded hardware interfaces
(I2C, SPI, UART, GPIO, WiFi, BLE, etc.) to enable unit testing in Python.
"""
import time
from unittest.mock import MagicMock


class MockI2C:
    """Mock I2C bus for testing I2C communication."""
    def __init__(self, sda=21, scl=22, frequency=100000):
        self.sda = sda
        self.scl = scl
        self.frequency = frequency
        self._devices = {}
        self._tx_buffer = b''
        self._rx_buffer = b''

    def begin(self, address):
        """Initialize I2C as master or slave."""
        pass

    def beginTransmission(self, address):
        """Start transmission to a device."""
        self._tx_buffer = b''

    def write(self, data):
        """Write data to the transmission buffer."""
        if isinstance(data, int):
            self._tx_buffer += bytes([data])
        elif isinstance(data, bytes):
            self._tx_buffer += data
        elif isinstance(data, str):
            self._tx_buffer += data.encode()
        return len(data)

    def endTransmission(self):
        """End transmission and send data."""
        return 0  # Success

    def requestFrom(self, address, quantity):
        """Request data from a device."""
        self._rx_buffer = self._devices.get(address, b'')[:quantity]
        return len(self._rx_buffer)

    def available(self):
        """Return number of bytes available for reading."""
        return len(self._rx_buffer)

    def read(self):
        """Read a byte from the receive buffer."""
        if self._rx_buffer:
            return self._rx_buffer[0]
        return 0


class MockSPI:
    """Mock SPI bus for testing SPI communication."""
    def __init__(self, sck=18, miso=19, mosi=23, cs=5):
        self.sck = sck
        self.miso = miso
        self.mosi = mosi
        self.cs = cs
        self._mode = 0
        self._bitorder = 0
        self._tx_data = b''
        self._rx_data = b''

    def begin(self):
        """Initialize SPI."""
        pass

    def setMode(self, mode):
        """Set SPI mode (0-3)."""
        self._mode = mode

    def transfer(self, data):
        """Send and receive data simultaneously."""
        if isinstance(data, int):
            return data
        return data


class MockUART:
    """Mock UART/Serial for testing serial communication."""
    def __init__(self, baudrate=9600, bits=8, parity=None, stop=1):
        self.baudrate = baudrate
        self.bits = bits
        self.parity = parity
        self.stop = stop
        self._tx_log = b''
        self._rx_buffer = b''
        self._timeout = 1.0

    def begin(self, baudrate):
        """Initialize serial with given baudrate."""
        self.baudrate = baudrate

    def write(self, data):
        """Write data to transmit buffer."""
        if isinstance(data, str):
            data = data.encode()
        self._tx_log += data
        return len(data)

    def read(self, size=1):
        """Read data from receive buffer."""
        result = self._rx_buffer[:size]
        self._rx_buffer = self._rx_buffer[size:]
        return result

    def readline(self):
        """Read a line ending with newline."""
        if b'\n' in self._rx_buffer:
            idx = self._rx_buffer.index(b'\n') + 1
            result = self._rx_buffer[:idx]
            self._rx_buffer = self._rx_buffer[idx:]
            return result
        return b''

    def readlines(self):
        """Read all lines."""
        lines = self._rx_buffer.split(b'\n')
        self._rx_buffer = b''
        return lines

    def available(self):
        """Return number of bytes available for reading."""
        return len(self._rx_buffer)

    def inject_rx(self, data):
        """Inject data into the receive buffer."""
        if isinstance(data, str):
            data = data.encode()
        self._rx_buffer += data

    def flush(self):
        """Wait for transmission to complete."""
        pass


class MockGPIO:
    """Mock GPIO for testing digital pin operations."""
    def __init__(self):
        self._pins = {}

    def pinMode(self, pin, mode):
        """Set pin mode (INPUT, OUTPUT, INPUT_PULLUP)."""
        self._pins[pin] = {'mode': mode, 'value': 0}

    def digitalWrite(self, pin, value):
        """Set pin value (HIGH, LOW)."""
        if pin in self._pins:
            self._pins[pin]['value'] = value

    def digitalRead(self, pin):
        """Read pin value (HIGH, LOW)."""
        if pin in self._pins:
            return self._pins[pin]['value']
        return 0

    def analogRead(self, pin):
        """Read analog value (0-4095 for 12-bit ADC)."""
        return 0


class MockNeoPixel:
    """Mock NeoPixel/WS2812 LED strip."""
    def __init__(self, pin, n, brightness=255):
        self.pin = pin
        self.n = n
        self.brightness = brightness
        self._pixels = [(0, 0, 0)] * n

    def begin(self):
        """Initialize NeoPixel."""
        pass

    def setPixelColor(self, n, color):
        """Set pixel color (r, g, b)."""
        if 0 <= n < self.n:
            self._pixels[n] = color

    def show(self):
        """Update LED strip."""
        pass

    def getPixelColor(self, n):
        """Get pixel color."""
        if 0 <= n < self.n:
            return self._pixels[n]
        return (0, 0, 0)


class MockWiFi:
    """Mock WiFi connection for testing."""
    def __init__(self, connected=True):
        self._connected = connected
        self._ssid = ''
        self._password = ''

    def begin(self, ssid, password):
        """Connect to WiFi network."""
        self._ssid = ssid
        self._password = password
        return self._connected

    def status(self):
        """Return connection status."""
        return 3 if self._connected else 0  # WL_CONNECTED = 3

    def isConnected(self):
        """Check if connected."""
        return self._connected

    def localIP(self):
        """Return local IP address."""
        return '192.168.1.100' if self._connected else '0.0.0.0'


class MockBLE:
    """Mock Bluetooth Low Energy for testing."""
    def __init__(self, enabled=True):
        self._enabled = enabled
        self._tx_buffer = b''

    def begin(self):
        """Initialize BLE."""
        pass

    def write(self, data):
        """Write data to BLE."""
        if isinstance(data, str):
            data = data.encode()
        self._tx_buffer += data

    def available(self):
        """Check if data is available."""
        return 0

    def read(self):
        """Read data from BLE."""
        return b''


class MockPreferences:
    """Mock non-volatile storage for testing."""
    def __init__(self):
        self._data = {}

    def begin(self, namespace, read_write=True):
        """Begin preferences session."""
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

    def getString(self, key, default=''):
        """Retrieve string."""
        return self._data.get(key, default)

    def end(self):
        """End preferences session."""
        pass


def arduino_map(x, in_min, in_max, out_min, out_max):
    """Arduino map() function re-implementation."""
    return int((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)


def arduino_constrain(x, a, b):
    """Arduino constrain() function re-implementation."""
    return max(a, min(x, b))


def analog_to_voltage(value, bits=10, ref=3.3):
    """Convert analog reading to voltage."""
    max_value = 2 ** bits - 1
    return (value / max_value) * ref


# Mock Arduino constants
HIGH = 1
LOW = 0
INPUT = 0
OUTPUT = 1
INPUT_PULLUP = 2

A0, A1, A2, A3, A4, A5 = range(14, 20)

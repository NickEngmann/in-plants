"""Mock objects and helpers for Arduino project testing.

This module provides mock implementations of Arduino-specific objects
that are used in the .ino source files but cannot be directly imported
into Python tests.
"""

from unittest.mock import MagicMock
import sys


class MockI2C:
    """Mock I2C bus for testing."""
    def __init__(self, sda=21, scl=22, frequency=100000):
        self.sda = sda
        self.scl = scl
        self.frequency = frequency
        self._devices = {}
        self._tx_buffer = b''
    
    def begin(self, sda=None, scl=None):
        """Initialize I2C."""
        if sda is not None:
            self.sda = sda
        if scl is not None:
            self.scl = scl
    
    def beginTransmission(self, address):
        """Begin transmission to a device."""
        self._tx_buffer = b''
    
    def write(self, data):
        """Write data to the buffer."""
        if isinstance(data, int):
            self._tx_buffer += bytes([data])
        else:
            self._tx_buffer += data
    
    def endTransmission(self):
        """End transmission and return status."""
        return 0  # Success
    
    def requestFrom(self, address, quantity):
        """Request data from a device."""
        return b''


class MockSPI:
    """Mock SPI bus for testing."""
    def __init__(self, sck=13, miso=12, mosi=11, cs=5):
        self.sck = sck
        self.miso = miso
        self.mosi = mosi
        self.cs = cs
        self._tx_buffer = b''
    
    def begin(self):
        """Initialize SPI."""
        pass
    
    def transfer(self, data):
        """Transfer data over SPI."""
        if isinstance(data, int):
            return data
        return data


class MockUART:
    """Mock UART/Serial for testing."""
    def __init__(self, baudrate=9600, tx=1, rx=3):
        self.baudrate = baudrate
        self.tx = tx
        self.rx = rx
        self._tx_log = b''
        self._rx_buffer = b''
    
    def begin(self, baudrate):
        """Initialize UART with baudrate."""
        self.baudrate = baudrate
    
    def write(self, data):
        """Write data to the transmit buffer."""
        if isinstance(data, str):
            data = data.encode()
        self._tx_log += data
    
    def read(self, size=None):
        """Read data from the receive buffer."""
        if size is None:
            result = self._rx_buffer
            self._rx_buffer = b''
            return result
        result = self._rx_buffer[:size]
        self._rx_buffer = self._rx_buffer[size:]
        return result
    
    def readline(self):
        """Read a line from the receive buffer."""
        if b'\n' in self._rx_buffer:
            idx = self._rx_buffer.index(b'\n') + 1
            result = self._rx_buffer[:idx]
            self._rx_buffer = self._rx_buffer[idx:]
            return result
        return b''
    
    def available(self):
        """Return number of bytes available."""
        return len(self._rx_buffer)
    
    def inject_rx(self, data):
        """Inject data into the receive buffer."""
        if isinstance(data, str):
            data = data.encode()
        self._rx_buffer += data


class MockGPIO:
    """Mock GPIO for testing."""
    def __init__(self):
        self._pins = {}
    
    def setup(self, pin, mode):
        """Set pin mode."""
        self._pins[pin] = {'mode': mode, 'value': 0}
    
    def output(self, pin, value):
        """Set pin output value."""
        if pin in self._pins:
            self._pins[pin]['value'] = value
    
    def input(self, pin):
        """Read pin input value."""
        if pin in self._pins:
            return self._pins[pin]['value']
        return 0


class MockNeoPixel:
    """Mock NeoPixel/WS2812 for testing."""
    def __init__(self, pin, n, brightness=255):
        self.pin = pin
        self.n = n
        self.brightness = brightness
        self._pixels = [(0, 0, 0)] * n
    
    def setPixelColor(self, i, color):
        """Set pixel color."""
        if 0 <= i < self.n:
            self._pixels[i] = color
    
    def show(self):
        """Update LEDs."""
        pass


class MockWiFi:
    """Mock WiFi for testing."""
    def __init__(self):
        self._connected = False
        self._ssid = None
    
    def begin(self, ssid, password=None):
        """Connect to WiFi."""
        self._ssid = ssid
        self._connected = True
    
    def status(self):
        """Return connection status."""
        return 3 if self._connected else 0  # WL_CONNECTED = 3
    
    def connected(self):
        """Return True if connected."""
        return self._connected


class MockBLE:
    """Mock BLE for testing."""
    def __init__(self):
        self._connected = False
    
    def begin(self):
        """Initialize BLE."""
        pass
    
    def connected(self):
        """Return True if connected."""
        return self._connected


class MockPreferences:
    """Mock Preferences (EEPROM-like storage) for testing."""
    def __init__(self):
        self._data = {}
    
    def begin(self, namespace):
        """Begin preferences session."""
        pass
    
    def putInt(self, key, value):
        """Store an integer."""
        self._data[key] = value
    
    def getInt(self, key, default=0):
        """Retrieve an integer."""
        return self._data.get(key, default)
    
    def putString(self, key, value):
        """Store a string."""
        self._data[key] = value
    
    def getString(self, key, default=''):
        """Retrieve a string."""
        return self._data.get(key, default)


# Arduino-like constants
class ArduinoConstants:
    """Arduino constants for testing."""
    HIGH = 1
    LOW = 0
    
    INPUT = 0
    OUTPUT = 1
    INPUT_PULLUP = 2
    
    # Analog pins (for mapping)
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
    """Convert analog reading to voltage."""
    max_val = (1 << bits) - 1
    return (value / max_val) * ref


# Mock Particle/Cloud functions that are used in the Arduino code
Particle = MagicMock()
Particle.publish = MagicMock(return_value=True)


def digitalWrite(pin, value):
    """Mock digitalWrite for testing."""
    pass


def pinMode(pin, mode):
    """Mock pinMode for testing."""
    pass


analogRead_values = {}


def analogRead(pin):
    """Mock analogRead for testing."""
    return analogRead_values.get(pin, 0)


def set_analog_read_value(pin, value):
    """Set the mock analogRead value for a pin."""
    analogRead_values[pin] = value


def delay(ms):
    """Mock delay for testing."""
    pass


# Create a module-like namespace for the mocks
mock_arduino = MagicMock()
mock_arduino.Particle = Particle
mock_arduino.digitalWrite = digitalWrite
mock_arduino.pinMode = pinMode
mock_arduino.analogRead = analogRead
mock_arduino.delay = delay
mock_arduino.set_analog_read_value = set_analog_read_value


# Expose the mock objects
__all__ = [
    'MockI2C',
    'MockSPI',
    'MockUART',
    'MockGPIO',
    'MockNeoPixel',
    'MockWiFi',
    'MockBLE',
    'MockPreferences',
    'ArduinoConstants',
    'arduino_map',
    'arduino_constrain',
    'analog_to_voltage',
    'Particle',
    'digitalWrite',
    'pinMode',
    'analogRead',
    'delay',
    'set_analog_read_value',
    'mock_arduino'
]

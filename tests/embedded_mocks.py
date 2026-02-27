"""Mock libraries for embedded systems testing.

Provides mock implementations of common embedded protocols and peripherals
for testing Arduino/C++ code in Python.
"""


class MockI2C:
    """Mock I2C bus for testing I2C communication."""
    
    def __init__(self, sda=21, scl=22, frequency=100000):
        self.sda = sda
        self.scl = scl
        self.frequency = frequency
        self._devices = {}
        self._tx_buffer = b''
        self._rx_buffer = b''
    
    def begin(self, address=None):
        """Initialize I2C as master or slave."""
        self._address = address
    
    def beginTransmission(self, address):
        """Begin transmission to a slave device."""
        self._target_address = address
        self._tx_buffer = b''
    
    def write(self, data):
        """Write data to transmission buffer."""
        if isinstance(data, int):
            self._tx_buffer += bytes([data])
        elif isinstance(data, str):
            self._tx_buffer += data.encode()
        else:
            self._tx_buffer += data
        return len(data) if hasattr(data, '__len__') else 1
    
    def endTransmission(self):
        """End transmission and send data."""
        if self._target_address in self._devices:
            self._devices[self._target_address] += self._tx_buffer
        self._tx_buffer = b''
        return 0  # success
    
    def requestFrom(self, address, length):
        """Request data from a slave device."""
        if address in self._devices:
            data = self._devices[address][:length]
            self._devices[address] = self._devices[address][length:]
            return data
        return b''
    
    def available(self):
        """Check if data is available for reading."""
        return len(self._rx_buffer)
    
    def read(self):
        """Read a single byte."""
        if self._rx_buffer:
            byte = self._rx_buffer[0]
            self._rx_buffer = self._rx_buffer[1:]
            return byte
        return 0
    
    def add_device(self, address, initial_data=b''):
        """Add a mock slave device."""
        self._devices[address] = initial_data


class MockSPI:
    """Mock SPI bus for testing SPI communication."""
    
    def __init__(self, sck=13, miso=12, mosi=11, cs=10):
        self.sck = sck
        self.miso = miso
        self.mosi = mosi
        self.cs = cs
        self._mode = 0
        self._bitorder = 'MSBFIRST'
        self._clock_freq = 1000000
        self._tx_buffer = b''
        self._rx_buffer = b''
    
    def begin(self):
        """Initialize SPI."""
        pass
    
    def setMode(self, mode):
        """Set SPI mode (0-3)."""
        self._mode = mode
    
    def setBitOrder(self, bitorder):
        """Set bit order (MSBFIRST or LSBFIRST)."""
        self._bitorder = bitorder
    
    def setClockFreq(self, freq):
        """Set clock frequency."""
        self._clock_freq = freq
    
    def write(self, data):
        """Write data via SPI."""
        if isinstance(data, int):
            return data
        self._tx_buffer = data if isinstance(data, bytes) else data.encode()
        return data
    
    def transfer(self, data):
        """Send and receive data simultaneously."""
        if isinstance(data, int):
            return data
        return data
    
    def read(self):
        """Read data from SPI."""
        if self._rx_buffer:
            return self._rx_buffer[0]
        return 0


class MockUART:
    """Mock UART/Serial for testing serial communication."""
    
    def __init__(self, baudrate=9600, tx_pin=None, rx_pin=None):
        self.baudrate = baudrate
        self.tx_pin = tx_pin
        self.rx_pin = rx_pin
        self._tx_log = b''
        self._rx_buffer = b''
        self._buffer = b''
    
    def begin(self, baudrate=None):
        """Initialize UART with specified baudrate."""
        if baudrate:
            self.baudrate = baudrate
    
    def write(self, data):
        """Write data to UART."""
        if isinstance(data, str):
            data = data.encode()
        self._tx_log += data
        return len(data)
    
    def print(self, data):
        """Print data with no newline."""
        return self.write(str(data))
    
    def println(self, data=''):
        """Print data with newline."""
        return self.write(str(data) + '\n')
    
    def read(self, size=None):
        """Read data from UART."""
        if size is None:
            size = len(self._buffer)
        data = self._buffer[:size]
        self._buffer = self._buffer[size:]
        return data
    
    def readByte(self):
        """Read a single byte."""
        if self._buffer:
            byte = self._buffer[0]
            self._buffer = self._buffer[1:]
            return byte
        return -1
    
    def readline(self):
        """Read a line terminated by newline."""
        if b'\n' in self._buffer:
            idx = self._buffer.index(b'\n') + 1
            line = self._buffer[:idx]
            self._buffer = self._buffer[idx:]
            return line
        return b''
    
    def available(self):
        """Check number of bytes available for reading."""
        return len(self._buffer)
    
    def availableForWrite(self):
        """Check available buffer space for writing."""
        return 1024  # Simulate ample buffer space
    
    def flush(self):
        """Wait for transmission to complete."""
        pass
    
    def inject_rx(self, data):
        """Inject data into the receive buffer."""
        if isinstance(data, str):
            data = data.encode()
        self._buffer += data
    
    def clear_buffer(self):
        """Clear the receive buffer."""
        self._buffer = b''


class MockGPIO:
    """Mock GPIO for testing digital I/O."""
    
    def __init__(self):
        self._pins = {}
        self._mode = {}
    
    def pinMode(self, pin, mode):
        """Set pin mode (INPUT, OUTPUT, INPUT_PULLUP)."""
        self._mode[pin] = mode
    
    def digitalWrite(self, pin, value):
        """Write a value (HIGH/LOW) to a pin."""
        self._pins[pin] = value
    
    def digitalRead(self, pin):
        """Read the value from a pin."""
        return self._pins.get(pin, 0)
    
    def set_pin_value(self, pin, value):
        """Set pin value for testing."""
        self._pins[pin] = value


class MockNeoPixel:
    """Mock NeoPixel/WS2812 LED strip."""
    
    def __init__(self, pin, n, brightness=255):
        self.pin = pin
        self.n = n
        self.brightness = brightness
        self._pixels = [(0, 0, 0)] * n
        self._show_called = False
    
    def begin(self):
        """Initialize NeoPixel."""
        pass
    
    def setPixelColor(self, n, color):
        """Set color of a pixel (r, g, b)."""
        if 0 <= n < self.n:
            self._pixels[n] = color
    
    def setPixelColorRGB(self, n, r, g, b):
        """Set color of a pixel with RGB values."""
        if 0 <= n < self.n:
            self._pixels[n] = (r, g, b)
    
    def show(self):
        """Update LED strip with buffered colors."""
        self._show_called = True
    
    def getPixelColor(self, n):
        """Get color of a pixel."""
        if 0 <= n < self.n:
            return self._pixels[n]
        return (0, 0, 0)
    
    def clear(self):
        """Clear all pixels."""
        self._pixels = [(0, 0, 0)] * self.n


class MockWiFi:
    """Mock WiFi connection for testing."""
    
    def __init__(self):
        self._connected = False
        self._ssid = None
        self._ip = None
    
    def begin(self, ssid, password=None):
        """Connect to WiFi network."""
        self._ssid = ssid
        self._connected = True
        self._ip = '192.168.1.100'
        return True
    
    def status(self):
        """Get connection status."""
        return 'WL_CONNECTED' if self._connected else 'WL_DISCONNECTED'
    
    def isConnected(self):
        """Check if connected."""
        return self._connected
    
    def localIP(self):
        """Get local IP address."""
        return self._ip
    
    def ssid(self):
        """Get SSID of connected network."""
        return self._ssid


class MockBLE:
    """Mock Bluetooth Low Energy for testing."""
    
    def __init__(self):
        self._enabled = False
        self._connected = False
        self._tx_buffer = b''
    
    def begin(self):
        """Initialize BLE."""
        self._enabled = True
    
    def enableBroadcast(self):
        """Enable advertising."""
        pass
    
    def connect(self, address):
        """Connect to a device."""
        self._connected = True
    
    def write(self, data):
        """Write data via BLE."""
        self._tx_buffer = data if isinstance(data, bytes) else data.encode()
        return len(data)
    
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
    
    def begin(self, namespace, read_only=False):
        """Begin a preferences session."""
        self._namespace = namespace
    
    def putInt(self, key, value):
        """Store an integer."""
        self._data[key] = value
    
    def putString(self, key, value):
        """Store a string."""
        self._data[key] = value
    
    def putBool(self, key, value):
        """Store a boolean."""
        self._data[key] = bool(value)
    
    def getInt(self, key, default=0):
        """Retrieve an integer."""
        return self._data.get(key, default)
    
    def getString(self, key, default=''):
        """Retrieve a string."""
        return self._data.get(key, default)
    
    def getBool(self, key, default=False):
        """Retrieve a boolean."""
        return self._data.get(key, default)
    
    def end(self):
        """End preferences session."""
        pass


# Helper functions
def arduino_map(x, in_min, in_max, out_min, out_max):
    """Arduino map() function re-implementation."""
    return int((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)


def arduino_constrain(x, a, b):
    """Arduino constrain() function re-implementation."""
    return max(a, min(x, b))


def analog_to_voltage(value, bits=10, ref=3.3):
    """Convert ADC value to voltage."""
    max_value = 2 ** bits - 1
    return (value / max_value) * ref


# Constants
HIGH = 1
LOW = 0
INPUT = 0
OUTPUT = 1
INPUT_PULLUP = 2

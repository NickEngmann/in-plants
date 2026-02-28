"""Mock Arduino environment for testing re-implemented logic."""


class ArduinoConstants:
    """Provides Arduino-like constants for testing."""
    
    HIGH = 1
    LOW = 0
    
    INPUT = 0
    OUTPUT = 1
    
    def map(self, x, in_min, in_max, out_min, out_max):
        """Arduino map function."""
        return (x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min
    
    def constrain(self, x, a, b):
        """Arduino constrain function."""
        return max(a, min(x, b))


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
    """Mock I2C communication for testing."""
    
    def __init__(self, sda=21, scl=22, frequency=100000):
        self.sda = sda
        self.scl = scl
        self.frequency = frequency
        self._tx_buffer = b''
        self._rx_buffer = b''
        self.addresses = set()
    
    def begin(self, sda=None, scl=None):
        """Initialize I2C."""
        if sda is not None:
            self.sda = sda
        if scl is not None:
            self.scl = scl
    
    def beginTransmission(self, address):
        """Begin transmission to a device."""
        self._tx_buffer = b''
        self._target_address = address
        self.addresses.add(address)
    
    def write(self, data):
        """Write data to the transmission buffer."""
        if isinstance(data, int):
            self._tx_buffer += bytes([data])
        elif isinstance(data, bytes):
            self._tx_buffer += data
        elif isinstance(data, str):
            self._tx_buffer += data.encode()
        return len(data) if isinstance(data, (bytes, str)) else 1
    
    def endTransmission(self):
        """End transmission and send data."""
        return 0  # Success
    
    def requestFrom(self, address, quantity):
        """Request data from a device."""
        self._rx_buffer = b'\x00' * min(quantity, 32)
        return len(self._rx_buffer)
    
    def available(self):
        """Check if data is available for reading."""
        return len(self._rx_buffer)
    
    def read(self):
        """Read a byte from the receive buffer."""
        if self._rx_buffer:
            return self._rx_buffer[0]
        return 0


class MockSPI:
    """Mock SPI communication for testing."""
    
    def __init__(self, sck=13, miso=12, mosi=11, cs=5):
        self.sck = sck
        self.miso = miso
        self.mosi = mosi
        self.cs = cs
        self._tx_buffer = b''
        self._rx_buffer = b''
        self.enabled = True
    
    def begin(self):
        """Initialize SPI."""
        pass
    
    def setFrequency(self, freq):
        """Set SPI clock frequency."""
        self.frequency = freq
    
    def transfer(self, data):
        """Simulate SPI transfer (full duplex)."""
        if isinstance(data, int):
            data = bytes([data])
        self._tx_buffer += data
        # Echo back for simulation
        return data
    
    def write(self, data):
        """Write data via SPI."""
        if isinstance(data, int):
            data = bytes([data])
        self._tx_buffer += data
    
    def read(self):
        """Read data from SPI."""
        if self._rx_buffer:
            return self._rx_buffer[0]
        return 0


class MockUART:
    """Mock UART/Serial communication for testing."""
    
    def __init__(self, baudrate=9600, rx_size=256, tx_size=256):
        self.baudrate = baudrate
        self._tx_log = b''
        self._rx_buffer = b''
        self._rx_position = 0
    
    def begin(self, baudrate=None):
        """Initialize UART."""
        if baudrate is not None:
            self.baudrate = baudrate
    
    def write(self, data):
        """Write data to the transmission log."""
        if isinstance(data, str):
            data = data.encode()
        self._tx_log += data
        return len(data)
    
    def print(self, data):
        """Print data (same as write)."""
        return self.write(data)
    
    def println(self, data=''):
        """Print data with newline."""
        if isinstance(data, str):
            data = data.encode()
        self._tx_log += data + b'\n'
        return len(data) + 1
    
    def available(self):
        """Check if data is available for reading."""
        return len(self._rx_buffer) - self._rx_position
    
    def read(self):
        """Read a byte from the receive buffer."""
        if self._rx_position < len(self._rx_buffer):
            byte = self._rx_buffer[self._rx_position]
            self._rx_position += 1
            return byte
        return -1
    
    def readline(self):
        """Read a line from the receive buffer."""
        start = self._rx_position
        while self._rx_position < len(self._rx_buffer):
            if self._rx_buffer[self._rx_position] == ord('\n'):
                line = self._rx_buffer[start:self._rx_position + 1]
                self._rx_position += 1
                return line
            self._rx_position += 1
        if start < len(self._rx_buffer):
            line = self._rx_buffer[start:]
            self._rx_position = len(self._rx_buffer)
            return line
        return b''
    
    def inject_rx(self, data):
        """Inject data into the receive buffer."""
        if isinstance(data, str):
            data = data.encode()
        self._rx_buffer += data
    
    def flush(self):
        """Flush the transmission buffer."""
        pass


class MockGPIO:
    """Mock GPIO pin operations for testing."""
    
    pins = {}
    
    @classmethod
    def reset(cls):
        cls.pins = {}
    
    @classmethod
    def pinMode(cls, pin, mode):
        """Set pin mode."""
        cls.pins[pin] = {'mode': mode, 'value': 0}
    
    @classmethod
    def digitalWrite(cls, pin, value):
        """Set pin value."""
        if pin not in cls.pins:
            cls.pins[pin] = {'mode': 1, 'value': 0}
        cls.pins[pin]['value'] = value
    
    @classmethod
    def digitalRead(cls, pin):
        """Read pin value."""
        if pin not in cls.pins:
            return 0
        return cls.pins[pin]['value']
    
    @classmethod
    def analogRead(cls, pin):
        """Simulate analog read (0-1023 for 10-bit ADC)."""
        return 512  # Default mid-range value


class MockNeoPixel:
    """Mock NeoPixel LED strip for testing."""
    
    def __init__(self, pin, n, bpp=3):
        self.pin = pin
        self.n = n
        self.bpp = bpp
        self.pixels = [(0, 0, 0)] * n
        self.brightness = 255
    
    def begin(self):
        """Initialize NeoPixel."""
        pass
    
    def setPixelColor(self, n, r, g, b, w=0):
        """Set pixel color."""
        if n < self.n:
            if self.bpp == 4:
                self.pixels[n] = (r, g, b, w)
            else:
                self.pixels[n] = (r, g, b)
    
    def setBrightness(self, b):
        """Set overall brightness."""
        self.brightness = b
    
    def show(self):
        """Update LEDs with pixel data."""
        pass


class MockWiFi:
    """Mock WiFi connectivity for testing."""
    
    connected = False
    ssid = ''
    
    @classmethod
    def reset(cls):
        cls.connected = False
        cls.ssid = ''
    
    @classmethod
    def begin(cls, ssid, password):
        """Connect to WiFi."""
        cls.ssid = ssid
        cls.connected = True
    
    @classmethod
    def status(cls):
        """Get connection status."""
        return 'WL_CONNECTED' if cls.connected else 'WL_DISCONNECTED'
    
    @classmethod
    def localIP(cls):
        """Get local IP address."""
        return '192.168.1.100' if cls.connected else '0.0.0.0'


class MockBLE:
    """Mock Bluetooth Low Energy for testing."""
    
    enabled = False
    
    @classmethod
    def begin(cls):
        """Initialize BLE."""
        cls.enabled = True
    
    @classmethod
    def end(cls):
        """Disable BLE."""
        cls.enabled = False
    
    @classmethod
    def connected(cls):
        """Check if BLE is connected."""
        return False
    
    @classmethod
    def write(cls, data):
        """Write data via BLE."""
        pass


class MockPreferences:
    """Mock non-volatile storage for testing."""
    
    storage = {}
    
    @classmethod
    def reset(cls):
        cls.storage = {}
    
    @classmethod
    def begin(cls, name, read_only=False):
        """Begin preferences session."""
        if name not in cls.storage:
            cls.storage[name] = {}
    
    @classmethod
    def getInt(cls, key, default=0):
        """Get integer value."""
        name = cls._current_name
        if name in cls.storage and key in cls.storage[name]:
            return cls.storage[name][key]
        return default
    
    @classmethod
    def getUInt(cls, key, default=0):
        """Get unsigned integer value."""
        return cls.getInt(key, default)
    
    @classmethod
    def getString(cls, key, default=''):
        """Get string value."""
        name = cls._current_name
        if name in cls.storage and key in cls.storage[name]:
            return cls.storage[name][key]
        return default
    
    @classmethod
    def putInt(cls, key, value):
        """Store integer value."""
        name = cls._current_name
        if name not in cls.storage:
            cls.storage[name] = {}
        cls.storage[name][key] = value
    
    @classmethod
    def putUInt(cls, key, value):
        """Store unsigned integer value."""
        cls.putInt(key, value)
    
    @classmethod
    def putString(cls, key, value):
        """Store string value."""
        name = cls._current_name
        if name not in cls.storage:
            cls.storage[name] = {}
        cls.storage[name][key] = value
    
    @classmethod
    def end(cls):
        """End preferences session."""
        pass

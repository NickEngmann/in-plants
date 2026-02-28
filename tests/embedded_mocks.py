"""Mock libraries for Arduino project testing.

Provides mock implementations for common Arduino libraries and helpers
to enable testing of re-implemented algorithms in Python.
"""


def arduino_map(x, in_min, in_max, out_min, out_max):
    """Arduino map() function - re-maps a number from one range to another."""
    return int((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)


def arduino_constrain(x, a, b):
    """Arduino constrain() function - constrains a value to a range."""
    return max(a, min(x, b))


def analog_to_voltage(value, bits=10, ref=3.3):
    """Convert analog read value to voltage.
    
    Args:
        value: Raw analog reading (0 to 2^bits - 1)
        bits: ADC resolution (default 10 for 10-bit ADC)
        ref: Reference voltage in volts
    """
    max_value = 2 ** bits - 1
    return (value / max_value) * ref


class MockI2C:
    """Mock I2C bus for testing."""
    def __init__(self, sda=21, scl=22, frequency=100000):
        self.sda = sda
        self.scl = scl
        self.frequency = frequency
        self._devices = {}
        self._tx_buffer = b''
        self._rx_buffer = b''
    
    def scan(self):
        """Scan for I2C devices."""
        return list(self._devices.keys())
    
    def start(self):
        """Start I2C transmission."""
        pass
    
    def stop(self):
        """Stop I2C transmission."""
        pass
    
    def write(self, data):
        """Write data to I2C device."""
        if isinstance(data, int):
            self._tx_buffer = bytes([data])
        else:
            self._tx_buffer = data
    
    def read(self, length=1):
        """Read data from I2C device."""
        return self._rx_buffer[:length]


class MockSPI:
    """Mock SPI bus for testing."""
    def __init__(self, sck=18, miso=19, mosi=23, cs=5):
        self.sck = sck
        self.miso = miso
        self.mosi = mosi
        self.cs = cs
        self._tx_buffer = b''
        self._rx_buffer = b''
    
    def begin(self):
        """Initialize SPI."""
        pass
    
    def transfer(self, data):
        """Send and receive data simultaneously."""
        if isinstance(data, int):
            data = bytes([data])
        self._tx_buffer = data
        return self._rx_buffer if self._rx_buffer else bytes(len(data))
    
    def write(self, data):
        """Write data via SPI."""
        self._tx_buffer = data if isinstance(data, bytes) else bytes([data])


class MockUART:
    """Mock UART/Serial for testing."""
    def __init__(self, baudrate=115200, tx=1, rx=3):
        self.baudrate = baudrate
        self.tx = tx
        self.rx = rx
        self._tx_log = b''
        self._rx_buffer = b''
        self._buffer = b''
    
    def begin(self, baudrate=None):
        """Initialize UART with optional baudrate."""
        if baudrate:
            self.baudrate = baudrate
    
    def write(self, data):
        """Write data to UART."""
        if isinstance(data, str):
            data = data.encode()
        self._tx_log += data
        return len(data)
    
    def read(self, size=-1):
        """Read data from UART."""
        if size == -1:
            result = self._buffer
            self._buffer = b''
            return result
        result = self._buffer[:size]
        self._buffer = self._buffer[size:]
        return result
    
    def readline(self):
        """Read a line from UART."""
        if b'\n' in self._buffer:
            idx = self._buffer.index(b'\n') + 1
            result = self._buffer[:idx]
            self._buffer = self._buffer[idx:]
            return result
        return b''
    
    def readlines(self):
        """Read multiple lines from UART."""
        lines = self._buffer.split(b'\n')
        self._buffer = b''
        return [line + b'\n' for line in lines if line]
    
    def available(self):
        """Check if data is available to read."""
        return len(self._buffer)
    
    def flush(self):
        """Flush the buffer."""
        self._buffer = b''
    
    def inject_rx(self, data):
        """Inject data into the receive buffer."""
        if isinstance(data, str):
            data = data.encode()
        self._buffer += data


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
    
    def set_pin_value(self, pin, value):
        """Set pin value directly (for testing)."""
        if pin in self._pins:
            self._pins[pin]['value'] = value


class MockNeoPixel:
    """Mock NeoPixel/WS2812 LED for testing."""
    def __init__(self, pin, n, brightness=0.5):
        self.pin = pin
        self.n = n
        self.brightness = brightness
        self._pixels = [(0, 0, 0) for _ in range(n)]
    
    def begin(self):
        """Initialize NeoPixel."""
        pass
    
    def set_pixel_color(self, i, r, g, b):
        """Set pixel color."""
        if 0 <= i < self.n:
            self._pixels[i] = (r, g, b)
    
    def set_brightness(self, brightness):
        """Set overall brightness."""
        self.brightness = brightness
    
    def show(self):
        """Update LED strip."""
        pass
    
    def get_pixel(self, i):
        """Get pixel color."""
        if 0 <= i < self.n:
            return self._pixels[i]
        return (0, 0, 0)


class MockWiFi:
    """Mock WiFi connection for testing."""
    def __init__(self, connected=True):
        self.connected = connected
        self._ssid = ''
        self._password = ''
    
    def begin(self, ssid, password=None):
        """Connect to WiFi network."""
        self._ssid = ssid
        self._password = password
        self.connected = True
        return True
    
    def status(self):
        """Get connection status."""
        return 3 if self.connected else 0  # WL_CONNECTED = 3
    
    def disconnect(self):
        """Disconnect from WiFi."""
        self.connected = False
    
    def local_ip(self):
        """Get local IP address."""
        return '192.168.1.100' if self.connected else '0.0.0.0'


class MockBLE:
    """Mock Bluetooth Low Energy for testing."""
    def __init__(self, enabled=True):
        self.enabled = enabled
        self._devices = []
    
    def begin(self, name='ESP32'):
        """Initialize BLE."""
        self.enabled = True
    
    def set_name(self, name):
        """Set BLE device name."""
        pass
    
    def advertise_service(self, uuid):
        """Advertise a service."""
        pass
    
    def available(self):
        """Check for available BLE data."""
        return 0
    
    def read(self):
        """Read BLE data."""
        return b''
    
    def write(self, data):
        """Write BLE data."""
        pass


class MockPreferences:
    """Mock non-volatile storage for testing."""
    def __init__(self):
        self._data = {}
    
    def begin(self, namespace, read_only=False):
        """Begin preferences session."""
        pass
    
    def end(self):
        """End preferences session."""
        pass
    
    def getUInt(self, key, default=0):
        """Get unsigned int value."""
        return self._data.get(key, default)
    
    def getInt(self, key, default=0):
        """Get int value."""
        return self._data.get(key, default)
    
    def getFloat(self, key, default=0.0):
        """Get float value."""
        return self._data.get(key, default)
    
    def getString(self, key, default=''):
        """Get string value."""
        return self._data.get(key, default)
    
    def putUInt(self, key, value):
        """Put unsigned int value."""
        self._data[key] = value
    
    def putInt(self, key, value):
        """Put int value."""
        self._data[key] = value
    
    def putFloat(self, key, value):
        """Put float value."""
        self._data[key] = value
    
    def putString(self, key, value):
        """Put string value."""
        self._data[key] = value
    
    def remove(self, key):
        """Remove a key."""
        if key in self._data:
            del self._data[key]

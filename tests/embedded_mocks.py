"""Mock implementations for embedded hardware testing.

Provides mock classes for I2C, SPI, UART, GPIO, NeoPixel, WiFi, BLE, Preferences
and helper functions for Arduino-like operations.
"""


class MockI2C:
    """Mock I2C bus for testing."""
    def __init__(self, *args, **kwargs):
        self._tx_log = b""
        self._rx_log = b""
    
    def begin(self):
        pass
    
    def beginTransmission(self, addr):
        self._tx_log = b""
    
    def write(self, data):
        if isinstance(data, bytes):
            self._tx_log += data
        elif isinstance(data, int):
            self._tx_log += bytes([data])
        else:
            self._tx_log += str(data).encode()
    
    def endTransmission(self):
        return 0
    
    def requestFrom(self, addr, length):
        return 0
    
    def read(self):
        return 0
    
    def readBytes(self, length):
        return b""
    
    def readString(self):
        return ""


class MockSPI:
    """Mock SPI bus for testing."""
    def __init__(self, *args, **kwargs):
        self._tx_log = b""
        self._rx_log = b""
    
    def begin(self):
        pass
    
    def end(self):
        pass
    
    def setBitOrder(self, order):
        pass
    
    def setDataMode(self, mode):
        pass
    
    def setClockDivider(self, divider):
        pass
    
    def beginTransaction(self, settings):
        pass
    
    def endTransaction(self):
        pass
    
    def transfer(self, data):
        self._tx_log += data if isinstance(data, bytes) else bytes([data])
        return b""


class MockUART:
    """Mock UART for serial communication testing."""
    def __init__(self, baudrate=9600):
        self._tx_log = b""
        self._rx_buffer = b""
        self._baudrate = baudrate
    
    def begin(self, baudrate):
        self._baudrate = baudrate
    
    def write(self, data):
        if isinstance(data, bytes):
            self._tx_log += data
        elif isinstance(data, str):
            self._tx_log += data.encode()
        elif isinstance(data, int):
            self._tx_log += bytes([data])
    
    def available(self):
        return len(self._rx_buffer)
    
    def read(self):
        if self._rx_buffer:
            result = self._rx_buffer[0]
            self._rx_buffer = self._rx_buffer[1:]
            return result
        return -1
    
    def readline(self):
        if b"\n" in self._rx_buffer:
            line, self._rx_buffer = self._rx_buffer.split(b"\n", 1)
            return line + b"\n"
        result = self._rx_buffer
        self._rx_buffer = b""
        return result
    
    def inject_rx(self, data):
        """Inject data into receive buffer for testing."""
        self._rx_buffer += data


class MockGPIO:
    """Mock GPIO for pin control testing."""
    def __init__(self):
        self._pins = {}
    
    def pinMode(self, pin, mode):
        self._pins[pin] = {'mode': mode, 'value': None}
    
    def digitalWrite(self, pin, value):
        if pin in self._pins:
            self._pins[pin]['value'] = value
    
    def digitalRead(self, pin):
        if pin in self._pins and self._pins[pin]['value'] is not None:
            return self._pins[pin]['value']
        return 0
    
    def analogWrite(self, pin, value):
        if pin in self._pins:
            self._pins[pin]['value'] = value
    
    def analogRead(self, pin):
        return 0


class MockNeoPixel:
    """Mock NeoPixel for LED strip testing."""
    def __init__(self, num_pixels, pin, *args, **kwargs):
        self._pixels = [(0, 0, 0) for _ in range(num_pixels)]
        self._pin = pin
    
    def begin(self):
        pass
    
    def show(self):
        pass
    
    def setPixelColor(self, index, r, g, b):
        if 0 <= index < len(self._pixels):
            self._pixels[index] = (r, g, b)
    
    def fill(self, color=None):
        if color:
            self._pixels = [color for _ in self._pixels]
        else:
            self._pixels = [(0, 0, 0) for _ in self._pixels]
    
    def getPixelColor(self, index):
        if 0 <= index < len(self._pixels):
            return self._pixels[index]
        return (0, 0, 0)


class MockWiFi:
    """Mock WiFi for network testing."""
    def __init__(self):
        self._connected = False
        self._ip = "0.0.0.0"
    
    def begin(self):
        pass
    
    def connected(self):
        return self._connected
    
    def connect(self, ssid, password):
        self._connected = True
        self._ip = "192.168.1.100"
    
    def disconnect(self):
        self._connected = False
    
    def localIP(self):
        return self._ip


class MockBLE:
    """Mock BLE for Bluetooth testing."""
    def __init__(self):
        self._connected = False
    
    def begin(self):
        pass
    
    def connected(self):
        return self._connected
    
    def connect(self):
        self._connected = True
    
    def disconnect(self):
        self._connected = False


class MockPreferences:
    """Mock Preferences for storage testing."""
    def __init__(self):
        self._store = {}
    
    def begin(self, name, read_only=False):
        pass
    
    def end(self):
        pass
    
    def put(self, key, value):
        self._store[key] = value
    
    def get(self, key, default=None):
        return self._store.get(key, default)
    
    def remove(self, key):
        if key in self._store:
            del self._store[key]
    
    def keys(self):
        return list(self._store.keys())


def arduino_map(x, in_min, in_max, out_min, out_max):
    """Arduino map() function."""
    return int((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)


def arduino_constrain(x, a, b):
    """Arduino constrain() function."""
    return max(a, min(x, b))


def analog_to_voltage(analog_value, bits=10, ref=3.3):
    """Convert analog value to voltage."""
    max_val = 2 ** bits
    return (analog_value / max_val) * ref

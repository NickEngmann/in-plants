"""embedded_mocks.py — Mock classes for Arduino peripheral testing.

Provides mock implementations of I2C, SPI, UART, GPIO, NeoPixel, WiFi, BLE,
and Preferences for testing Arduino code logic in Python.
"""
import pytest

# Arduino constants
HIGH = 1
LOW = 0
INPUT = 0
OUTPUT = 1
INPUT_PULLUP = 2

# Analog pin constants
A0 = 14
A1 = 15
A2 = 16
A3 = 17
A4 = 18
A5 = 19


def arduino_map(value, from_low, from_high, to_low, to_high):
    """Map a value from one range to another (Arduino map function)."""
    return int((value - from_low) * (to_high - to_low) / (from_high - from_low) + to_low)


def arduino_constrain(value, low, high):
    """Constrain a value between low and high (Arduino constrain function)."""
    return max(low, min(value, high))


def analog_to_voltage(analog_value, bits=10, ref=3.3):
    """Convert analog value to voltage."""
    max_value = 2 ** bits - 1
    return (analog_value / max_value) * ref


class MockI2C:
    """Mock I2C interface for testing."""
    
    def __init__(self, wire=None):
        self._tx_data = []
        self._rx_data = []
        self._started = False
        
    def begin(self):
        self._started = True
        self._tx_data = []
        self._rx_data = []
        
    def beginTransmission(self, address):
        self._current_address = address
        self._tx_buffer = []
        
    def write(self, data):
        if isinstance(data, bytes):
            self._tx_buffer.extend(data)
        else:
            self._tx_buffer.append(data)
            
    def endTransmission(self):
        self._tx_data.append((self._current_address, bytes(self._tx_buffer)))
        self._tx_buffer = []
        return 0
        
    def requestFrom(self, address, quantity):
        self._rx_data = []
        
    def read(self):
        return self._rx_data.pop(0) if self._rx_data else 0
        
    def inject_rx(self, data):
        """Inject data into receive buffer for testing."""
        if isinstance(data, bytes):
            self._rx_data = list(data)
        else:
            self._rx_data = [data]


class MockSPI:
    """Mock SPI interface for testing."""
    
    def __init__(self):
        self._tx_data = []
        self._rx_data = []
        
    def begin(self):
        pass
        
    def end(self):
        pass
        
    def setClockDivider(self, divider):
        pass
        
    def setBitOrder(self, order):
        pass
        
    def setDataMode(self, mode):
        pass
        
    def beginTransaction(self, settings):
        pass
        
    def endTransaction(self):
        pass
        
    def transfer(self, data):
        self._tx_data.append(data)
        return data
        
    def write(self, data):
        self._tx_data.append(data)
        return data
        
    def inject_rx(self, data):
        """Inject data into receive buffer for testing."""
        self._rx_data = data if isinstance(data, list) else [data]


class MockUART:
    """Mock UART/Serial interface for testing."""
    
    def __init__(self, baudrate=9600):
        self._tx_log = b""
        self._rx_buffer = b""
        self._baudrate = baudrate
        
    def begin(self, baudrate):
        self._baudrate = baudrate
        self._tx_log = b""
        self._rx_buffer = b""
        
    def end(self):
        pass
        
    def write(self, data):
        if isinstance(data, str):
            data = data.encode('utf-8')
        elif isinstance(data, bytes):
            pass
        elif isinstance(data, int):
            data = bytes([data])
        else:
            data = str(data).encode('utf-8')
        self._tx_log += data
        return len(data)
        
    def print(self, data):
        self.write(data)
        self.write(b"\n")
        
    def println(self, data=""):
        self.write(data)
        self.write(b"\n")
        
    def available(self):
        return len(self._rx_buffer)
        
    def read(self):
        if self._rx_buffer:
            char = self._rx_buffer[0]
            self._rx_buffer = self._rx_buffer[1:]
            return char
        return -1
        
    def readline(self):
        if b'\n' in self._rx_buffer:
            line, self._rx_buffer = self._rx_buffer.split(b'\n', 1)
            return line + b'\n'
        result = self._rx_buffer
        self._rx_buffer = b""
        return result
        
    def flush(self):
        self._tx_log = b""
        
    def inject_rx(self, data):
        """Inject data into receive buffer for testing."""
        if isinstance(data, str):
            data = data.encode('utf-8')
        self._rx_buffer += data


class MockGPIO:
    """Mock GPIO interface for testing."""
    
    def __init__(self):
        self._pins = {}
        self._pin_modes = {}
        
    def pinMode(self, pin, mode):
        self._pin_modes[pin] = mode
        if pin not in self._pins:
            self._pins[pin] = 0
            
    def digitalWrite(self, pin, value):
        if pin not in self._pins:
            self._pins[pin] = 0
        self._pins[pin] = value
        
    def digitalRead(self, pin):
        return self._pins.get(pin, 0)
        
    def analogWrite(self, pin, value):
        if pin not in self._pins:
            self._pins[pin] = 0
        self._pins[pin] = value
        
    def analogRead(self, pin):
        return self._pins.get(pin, 0)
        
    def get_pin_state(self, pin):
        return self._pins.get(pin, 0)
        
    def get_pin_mode(self, pin):
        return self._pin_modes.get(pin, INPUT)


class MockNeoPixel:
    """Mock NeoPixel/LED strip interface for testing."""
    
    def __init__(self, num_pixels, pin, pixel_type="NEO_GRB + NEO_KHZ800"):
        self._num_pixels = num_pixels
        self._pixels = [(0, 0, 0) for _ in range(num_pixels)]
        self._brightness = 255
        self._started = False
        
    def begin(self):
        self._started = True
        
    def show(self):
        pass
        
    def setPixelColor(self, index, r, g, b):
        if 0 <= index < self._num_pixels:
            self._pixels[index] = (r, g, b)
            
    def setPixelColorHSV(self, index, hue, saturation, value):
        # Simplified HSV to RGB conversion
        if 0 <= index < self._num_pixels:
            self._pixels[index] = (value, value, value)
            
    def setBrightness(self, brightness):
        self._brightness = brightness
        
    def getPixelColor(self, index):
        if 0 <= index < self._num_pixels:
            return self._pixels[index]
        return (0, 0, 0)
        
    def clear(self):
        self._pixels = [(0, 0, 0) for _ in range(self._num_pixels)]


class MockWiFi:
    """Mock WiFi interface for testing."""
    
    def __init__(self):
        self._connected = False
        self._ssid = None
        self._ip = "0.0.0.0"
        self._rssi = 0
        
    def begin(self, ssid, password=None):
        self._ssid = ssid
        self._connected = True
        self._ip = "192.168.1.100"
        self._rssi = -50
        return self._connected
        
    def connected(self):
        return self._connected
        
    def disconnect(self):
        self._connected = False
        return True
        
    def hostname(self, name):
        pass
        
    def getIP(self):
        return self._ip
        
    def getRSSI(self):
        return self._rssi
        
    def beginAP(self, ssid):
        self._ssid = ssid
        self._connected = True
        return True
        
    def status(self):
        return "WL_CONNECTED" if self._connected else "WL_NO_SHIELD"


class MockBLE:
    """Mock BLE interface for testing."""
    
    def __init__(self):
        self._connected = False
        self._device_name = "Device"
        
    def begin(self, device_name):
        self._device_name = device_name
        return True
        
    def connected(self):
        return self._connected
        
    def disconnect(self):
        self._connected = False
        return True
        
    def hasValueWritten(self, characteristic):
        return False
        
    def readCharacteristic(self, characteristic):
        return b""
        
    def writeCharacteristic(self, characteristic, value):
        pass
        
    def central(self):
        return self._connected
        
    def peripheral(self):
        return True


class MockPreferences:
    """Mock Preferences/EEPROM interface for testing."""
    
    def __init__(self):
        self._data = {}
        self._started = False
        
    def begin(self, device_id, read_only=False):
        self._started = True
        self._read_only = read_only
        return True
        
    def end(self):
        self._started = False
        
    def putInt(self, key, value):
        if self._started and not self._read_only:
            self._data[key] = value
            
    def getInt(self, key, default=0):
        return self._data.get(key, default)
        
    def putFloat(self, key, value):
        if self._started and not self._read_only:
            self._data[key] = value
            
    def getFloat(self, key, default=0.0):
        return self._data.get(key, default)
        
    def putString(self, key, value):
        if self._started and not self._read_only:
            self._data[key] = value
            
    def getString(self, key, default=""):
        return self._data.get(key, default)
        
    def exists(self, key):
        return key in self._data
        
    def clear(self):
        self._data.clear()

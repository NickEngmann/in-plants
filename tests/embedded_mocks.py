"""embedded_mocks.py — Mock implementations for Arduino hardware interfaces.

These mocks allow testing Arduino code logic in Python without hardware.
"""

# Arduino constants
HIGH = 1
LOW = 0
INPUT = 0
OUTPUT = 1
INPUT_PULLUP = 2
INPUT_PULLDOWN = 3

# Analog pins (A0-A5)
A0 = 14
A1 = 15
A2 = 16
A3 = 17
A4 = 18
A5 = 19

# Digital pins
D0 = 0
D1 = 1
D2 = 2
D3 = 3
D4 = 4
D5 = 5
D6 = 6
D7 = 7
D8 = 8
D9 = 9
D10 = 10
D11 = 11
D12 = 12
D13 = 13


def arduino_map(value, from_low, from_high, to_low, to_high):
    """Map a value from one range to another (Arduino map function)."""
    return int((value - from_low) * (to_high - to_low) / (from_high - from_low) + to_low)


def arduino_constrain(value, min_val, max_val):
    """Constrain a value between min and max (Arduino constrain function)."""
    if value < min_val:
        return min_val
    if value > max_val:
        return max_val
    return value


def analog_to_voltage(analog_value, bits=10, ref=3.3):
    """Convert analog ADC value to voltage."""
    max_val = 2 ** bits - 1
    return (analog_value / max_val) * ref


class MockI2C:
    """Mock I2C interface for testing."""
    
    def __init__(self, wire=None):
        self._wire = wire
        self._tx_buffer = bytearray()
        self._rx_buffer = bytearray()
        self._devices = {}
    
    def begin(self):
        pass
    
    def beginTransmission(self, address):
        self._tx_buffer = bytearray()
    
    def write(self, data):
        if isinstance(data, int):
            self._tx_buffer.append(data)
        elif isinstance(data, bytes):
            self._tx_buffer.extend(data)
        elif isinstance(data, bytearray):
            self._tx_buffer.extend(data)
    
    def endTransmission(self):
        if self._tx_buffer:
            addr = self._tx_buffer[0] if len(self._tx_buffer) > 0 else 0
            self._devices[addr] = self._tx_buffer[1:]
        self._tx_buffer = bytearray()
    
    def requestFrom(self, address, quantity):
        if address in self._devices:
            self._rx_buffer = bytearray(self._devices[address])
        return len(self._rx_buffer)
    
    def read(self):
        if self._rx_buffer:
            return self._rx_buffer.pop(0)
        return 0
    
    def registerWrite(self, address, register, value):
        self.beginTransmission(address)
        self.write(register)
        self.write(value)
        self.endTransmission()
    
    def registerRead(self, address, register):
        self.beginTransmission(address)
        self.write(register)
        self.endTransmission()
        self.requestFrom(address, 1)
        return self.read()


class MockSPI:
    """Mock SPI interface for testing."""
    
    def __init__(self):
        self._tx_buffer = bytearray()
        self._rx_buffer = bytearray()
    
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
        if isinstance(data, int):
            self._tx_buffer.append(data)
            return data
        return data
    
    def write(self, data):
        if isinstance(data, int):
            self._tx_buffer.append(data)
            return data
        elif isinstance(data, bytes):
            self._tx_buffer.extend(data)
            return data
        return data
    
    def read(self):
        return 0


class MockUART:
    """Mock UART/Serial interface for testing."""
    
    def __init__(self, baudrate=115200):
        self._baudrate = baudrate
        self._tx_log = bytearray()
        self._rx_queue = []
    
    def begin(self, baudrate):
        self._baudrate = baudrate
    
    def end(self):
        pass
    
    def write(self, data):
        if isinstance(data, int):
            self._tx_log.append(data)
        elif isinstance(data, bytes):
            self._tx_log.extend(data)
        elif isinstance(data, str):
            self._tx_log.extend(data.encode())
        elif isinstance(data, bytearray):
            self._tx_log.extend(data)
    
    def print(self, data):
        self.write(data)
        self.write(b"\n")
    
    def println(self, data):
        self.write(data)
        self.write(b"\n")
    
    def available(self):
        return len(self._rx_queue)
    
    def read(self):
        if self._rx_queue:
            return self._rx_queue.pop(0)
        return -1
    
    def readline(self):
        if self._rx_queue:
            line = bytearray()
            while self._rx_queue:
                byte = self._rx_queue.pop(0)
                line.append(byte)
                if byte == ord('\n'):
                    break
            return bytes(line)
        return b""
    
    def flush(self):
        pass
    
    def inject_rx(self, data):
        """Inject data into receive queue for testing."""
        if isinstance(data, bytes):
            self._rx_queue.extend(list(data))
        elif isinstance(data, str):
            self._rx_queue.extend(list(data.encode()))


class MockGPIO:
    """Mock GPIO interface for testing."""
    
    def __init__(self):
        self._pins = {}
    
    def pinMode(self, pin, mode):
        self._pins[pin] = {'mode': mode, 'value': LOW}
    
    def digitalWrite(self, pin, value):
        if pin in self._pins:
            self._pins[pin]['value'] = value
    
    def digitalRead(self, pin):
        if pin in self._pins:
            return self._pins[pin]['value']
        return LOW
    
    def analogWrite(self, pin, value):
        if pin in self._pins:
            self._pins[pin]['value'] = value
    
    def analogRead(self, pin):
        if pin in self._pins:
            return self._pins[pin].get('analog_value', 0)
        return 0
    
    def get_pin_state(self, pin):
        if pin in self._pins:
            return self._pins[pin]
        return None


class MockNeoPixel:
    """Mock NeoPixel/LED strip interface for testing."""
    
    def __init__(self, num_pixels, pin):
        self._num_pixels = num_pixels
        self._pin = pin
        self._pixels = [(0, 0, 0) for _ in range(num_pixels)]
    
    def begin(self):
        pass
    
    def show(self):
        pass
    
    def setPixelColor(self, index, r, g, b):
        if 0 <= index < self._num_pixels:
            self._pixels[index] = (r, g, b)
    
    def setPixelColorHSV(self, index, hue, saturation, value):
        # Simplified conversion
        r = g = b = int(value * 255 / 256)
        self.setPixelColor(index, r, g, b)
    
    def fill(self, color=None):
        if color:
            self._pixels = [color for _ in range(self._num_pixels)]
        else:
            self._pixels = [(0, 0, 0) for _ in range(self._num_pixels)]
    
    def getPixelColor(self, index):
        if 0 <= index < self._num_pixels:
            return self._pixels[index]
        return (0, 0, 0)


class MockWiFi:
    """Mock WiFi interface for testing."""
    
    def __init__(self):
        self._connected = False
        self._ssid = None
        self._ip = None
    
    def begin(self, ssid, password=None):
        self._ssid = ssid
        self._connected = True
        self._ip = "192.168.1.100"
    
    def connected(self):
        return self._connected
    
    def disconnect(self):
        self._connected = False
    
    def IP(self):
        return self._ip if self._connected else None
    
    def hostname(self, name):
        pass


class MockBLE:
    """Mock BLE interface for testing."""
    
    def __init__(self):
        self._connected = False
        self._device_name = "Device"
    
    def begin(self, device_name):
        self._device_name = device_name
    
    def connected(self):
        return self._connected
    
    def disconnect(self):
        self._connected = False


class MockPreferences:
    """Mock Preferences/EEPROM interface for testing."""
    
    def __init__(self):
        self._data = {}
    
    def begin(self, section=None):
        pass
    
    def end(self):
        pass
    
    def put(self, key, value):
        self._data[key] = value
    
    def get(self, key, default=None):
        return self._data.get(key, default)
    
    def remove(self, key):
        if key in self._data:
            del self._data[key]
    
    def isKeyPresent(self, key):
        return key in self._data
    
    def getString(self, key, default=""):
        val = self._data.get(key)
        return val if val is not None else default
    
    def putString(self, key, value):
        self._data[key] = value

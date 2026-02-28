"""Mock libraries for embedded C testing."""


def arduino_map(x, in_min, in_max, out_min, out_max):
    """Re-implementation of Arduino's map() function."""
    return int((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)


def arduino_constrain(x, low, high):
    """Re-implementation of Arduino's constrain() function."""
    return max(low, min(x, high))


def analog_to_voltage(analog_value, bits=10, ref=3.3):
    """Convert analog reading to voltage."""
    max_value = (1 << bits) - 1
    return analog_value * (ref / max_value)


class MockI2C:
    """Mock I2C bus."""
    def __init__(self, sda=21, scl=22, frequency=100000):
        self.sda = sda
        self.scl = scl
        self.frequency = frequency
        self._tx_buffer = b""
        self._rx_buffer = b""
    
    def write(self, data):
        self._tx_buffer = data
    
    def read(self, n):
        return self._rx_buffer[:n]


class MockSPI:
    """Mock SPI bus."""
    def __init__(self, sck=18, miso=19, mosi=23, cs=5):
        self.sck = sck
        self.miso = miso
        self.mosi = mosi
        self.cs = cs
    
    def transfer(self, data):
        return data


class MockUART:
    """Mock UART serial port."""
    def __init__(self, baudrate=115200, rx_pin=3, tx_pin=1):
        self.baudrate = baudrate
        self.rx_pin = rx_pin
        self.tx_pin = tx_pin
        self._tx_log = b""
        self._rx_buffer = b""
    
    def write(self, data):
        self._tx_log += data
    
    def read(self, n=-1):
        if n < 0:
            result = self._rx_buffer
            self._rx_buffer = b""
            return result
        result = self._rx_buffer[:n]
        self._rx_buffer = self._rx_buffer[n:]
        return result
    
    def readline(self):
        if b"\n" in self._rx_buffer:
            idx = self._rx_buffer.index(b"\n") + 1
            result = self._rx_buffer[:idx]
            self._rx_buffer = self._rx_buffer[idx:]
            return result
        return b""
    
    def inject_rx(self, data):
        self._rx_buffer += data


class MockGPIO:
    """Mock GPIO pin."""
    def __init__(self, pin, mode="OUTPUT"):
        self.pin = pin
        self.mode = mode
        self.value = 0
    
    def high(self):
        self.value = 1
    
    def low(self):
        self.value = 0
    
    def read(self):
        return self.value


class MockNeoPixel:
    """Mock NeoPixel LED strip."""
    def __init__(self, pin, n, brightness=0.5):
        self.pin = pin
        self.n = n
        self.brightness = brightness
        self.pixels = [(0, 0, 0)] * n
    
    def set_pixel(self, i, r, g, b):
        if 0 <= i < self.n:
            self.pixels[i] = (r, g, b)
    
    def show(self):
        pass


class MockWiFi:
    """Mock WiFi connection."""
    def __init__(self):
        self.connected = False
        self.ssid = None
    
    def connect(self, ssid, password):
        self.ssid = ssid
        self.connected = True
    
    def disconnect(self):
        self.connected = False


class MockBLE:
    """Mock BLE connection."""
    def __init__(self):
        self.connected = False
    
    def connect(self):
        self.connected = True
    
    def disconnect(self):
        self.connected = False


class MockPreferences:
    """Mock non-volatile storage."""
    def __init__(self):
        self._data = {}
    
    def put(self, key, value):
        self._data[key] = value
    
    def get(self, key, default=None):
        return self._data.get(key, default)


class MockSSD1306:
    """Mock SSD1306 OLED display."""
    def __init__(self, width=128, height=64):
        self.width = width
        self.height = height
        self.buffer = [[0] * width for _ in range(height)]
    
    def pixel(self, x, y, color=1):
        if 0 <= x < self.width and 0 <= y < self.height:
            self.buffer[y][x] = color


class MockHT16K33:
    """Mock HT16K33 LED driver."""
    def __init__(self, address=0x70):
        self.address = address
        self.leds = [0] * 16
    
    def set_led(self, pin, state):
        if 0 <= pin < 16:
            self.leds[pin] = 1 if state else 0


class MockRotaryEncoder:
    """Mock rotary encoder."""
    def __init__(self, pin_a=2, pin_b=3):
        self.pin_a = pin_a
        self.pin_b = pin_b
        self.position = 0
    
    def update(self):
        pass


class MockADC:
    """Mock ADC channel."""
    def __init__(self, pin, bits=12):
        self.pin = pin
        self.bits = bits
        self.value = 0
    
    def read(self):
        return self.value


class MockPWM:
    """Mock PWM channel."""
    def __init__(self, pin, frequency=50):
        self.pin = pin
        self.frequency = frequency
        self.duty_cycle = 0
    
    def write(self, value):
        self.duty_cycle = value


class MockTemperatureSensor:
    """Mock temperature sensor."""
    def __init__(self, pin=0):
        self.pin = pin
        self.temperature = 25.0
    
    def read_temperature(self):
        return self.temperature


class MockAccelerometer:
    """Mock accelerometer."""
    def __init__(self):
        self.x = 0
        self.y = 0
        self.z = 1.0  # 1G default
    
    def read_acceleration(self):
        return self.x, self.y, self.z

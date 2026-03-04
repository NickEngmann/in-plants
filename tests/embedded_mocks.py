"""embedded_mocks.py — Reusable hardware mocks for Arduino/Particle testing.

This module provides mock classes for testing embedded hardware code without
requiring physical hardware. These mocks simulate hardware behavior for testing.
"""
from unittest.mock import MagicMock, Mock
import sys

# Add tests directory to path for imports
sys.path.insert(0, 'tests')


class MockI2C:
    """Mock I2C bus for testing."""
    def __init__(self):
        self.addresses = {}
        self.tx_log = []
        self.rx_log = []
    
    def begin(self):
        pass
    
    def beginTransmission(self, address):
        self.tx_log.append(address)
    
    def write(self, data):
        pass
    
    def endTransmission(self):
        pass
    
    def requestFrom(self, address, quantity):
        return b'\x00' * quantity
    
    def read(self):
        return 0


class MockSPI:
    """Mock SPI bus for testing."""
    def __init__(self):
        self.tx_log = []
        self.rx_log = []
    
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
        return data
    
    def write(self, data):
        self.tx_log.append(data)
    
    def read(self):
        return 0


class MockUART:
    """Mock UART/Serial for testing."""
    def __init__(self):
        self.tx_log = []
        self.rx_log = []
        self.baud_rate = 9600
    
    def begin(self, baud_rate=9600):
        self.baud_rate = baud_rate
    
    def end(self):
        pass
    
    def available(self):
        return 0
    
    def read(self):
        return -1
    
    def readStringUntil(self, delimiter):
        return ""
    
    def write(self, data):
        self.tx_log.append(data)
    
    def print(self, data):
        self.tx_log.append(str(data))
    
    def println(self, data=""):
        self.tx_log.append(str(data) + "\n")
    
    def flush(self):
        pass
    
    def hasInjectResponse(self):
        return True
    
    def inject_response(self, response):
        """Inject a response for simulating hardware replies."""
        self.rx_log.append(response)


class MockGPIO:
    """Mock GPIO pins for testing."""
    def __init__(self):
        self.pin_states = {}
        self.pin_modes = {}
        self.digital_log = []
        self.analog_log = []
    
    def pinMode(self, pin, mode):
        self.pin_modes[pin] = mode
    
    def digitalWrite(self, pin, value):
        self.pin_states[pin] = value
        self.digital_log.append((pin, value))
    
    def digitalRead(self, pin):
        return self.pin_states.get(pin, 0)
    
    def analogWrite(self, pin, value):
        self.analog_log.append((pin, value))
    
    def analogRead(self, pin):
        return 0


class MockNeoPixel:
    """Mock NeoPixel LED strip for testing."""
    def __init__(self, num_pixels=1):
        self.num_pixels = num_pixels
        self.pixels = [(0, 0, 0)] * num_pixels
        self.brightness = 255
    
    def begin(self):
        pass
    
    def show(self):
        pass
    
    def setPixelColor(self, index, r, g, b):
        if 0 <= index < self.num_pixels:
            self.pixels[index] = (r, g, b)
    
    def setBrightness(self, brightness):
        self.brightness = brightness
    
    def getPixelColor(self, index):
        if 0 <= index < self.num_pixels:
            return self.pixels[index]
        return (0, 0, 0)


class MockSSD1306:
    """Mock SSD1306 OLED display for testing."""
    def __init__(self, width=128, height=64):
        self.width = width
        self.height = height
        self.buffer = [[0] * width for _ in range(height)]
        self.display_log = []
    
    def begin(self, reset=None):
        pass
    
    def clear(self):
        self.buffer = [[0] * self.width for _ in range(self.height)]
    
    def display(self):
        self.display_log.append("display")
    
    def fill(self, value):
        self.buffer = [[value] * self.width for _ in range(self.height)]
    
    def setCursor(self, x, y):
        pass
    
    def setTextSize(self, size):
        pass
    
    def setTextColor(self, color):
        pass
    
    def print(self, text):
        self.display_log.append(text)
    
    def drawPixel(self, x, y, color):
        if 0 <= y < self.height and 0 <= x < self.width:
            self.buffer[y][x] = color
    
    def drawLine(self, x0, y0, x1, y1, color):
        self.display_log.append(f"line {x0},{y0} to {x1},{y1}")
    
    def drawRect(self, x, y, w, h, color):
        self.display_log.append(f"rect {x},{y} {w}x{h}")
    
    def fillRect(self, x, y, w, h, color):
        self.display_log.append(f"fill {x},{y} {w}x{h}")
    
    def drawCircle(self, x, y, r, color):
        self.display_log.append(f"circle {x},{y} r={r}")
    
    def drawCircleHelper(self, x, y, r, cornername, color):
        self.display_log.append(f"circle helper {x},{y} r={r}")
    
    def fillCircle(self, x, y, r, color):
        self.display_log.append(f"fill circle {x},{y} r={r}")
    
    def drawTriangle(self, x0, y0, x1, y1, x2, y2, color):
        self.display_log.append(f"triangle {x0},{y0} {x1},{y1} {x2},{y2}")
    
    def fillTriangle(self, x0, y0, x1, y1, x2, y2, color):
        self.display_log.append(f"fill triangle {x0},{y0} {x1},{y1} {x2},{y2}")
    
    def drawRoundRect(self, x, y, w, h, r, color):
        self.display_log.append(f"round rect {x},{y} {w}x{h} r={r}")
    
    def fillRoundRect(self, x, y, w, h, r, color):
        self.display_log.append(f"fill round rect {x},{y} {w}x{h} r={r}")
    
    def drawBitmap(self, x, y, bitmap, w, h, color):
        self.display_log.append(f"bitmap {x},{y} {w}x{h}")
    
    def invertDisplay(self, i):
        self.display_log.append(f"invert {i}")
    
    def setContrast(self, contrast):
        self.display_log.append(f"contrast {contrast}")
    
    def sleep(self):
        self.display_log.append("sleep")
    
    def stopsleep(self):
        self.display_log.append("stopsleep")


class MockHT16K33:
    """Mock HT16K33 LED matrix driver for testing."""
    def __init__(self, address=0x70):
        self.address = address
        self.matrix = [[0] * 8 for _ in range(8)]
        self.brightness = 0
        self.display_log = []
    
    def begin(self):
        pass
    
    def setBrightness(self, brightness):
        self.brightness = brightness
    
    def clear(self):
        self.matrix = [[0] * 8 for _ in range(8)]
    
    def display(self):
        self.display_log.append("display")
    
    def drawPixel(self, x, y, on=True):
        if 0 <= x < 8 and 0 <= y < 8:
            self.matrix[y][x] = 1 if on else 0
            self.display_log.append(f"pixel {x},{y}")


class MockRotaryEncoder:
    """Mock rotary encoder for testing."""
    def __init__(self):
        self.position = 0
        self.rotation_log = []
    
    def read(self):
        return self.position
    
    def step(self):
        return 0
    
    def update(self):
        pass


class MockADC:
    """Mock ADC for testing."""
    def __init__(self):
        self.readings = {}
        self.read_log = []
    
    def begin(self):
        pass
    
    def end(self):
        pass
    
    def read(self, pin):
        self.read_log.append(pin)
        return self.readings.get(pin, 0)
    
    def setReference(self, reference):
        pass
    
    def setResolution(self, resolution):
        pass


class MockPWM:
    """Mock PWM for testing."""
    def __init__(self):
        self.duty_cycles = {}
        self.pwm_log = []
    
    def begin(self, pin):
        pass
    
    def write(self, pin, duty):
        self.duty_cycles[pin] = duty
        self.pwm_log.append((pin, duty))
    
    def writeMicroseconds(self, pin, microseconds):
        self.pwm_log.append((pin, microseconds, "micros"))
    
    def setPeriodHz(self, pin, hz):
        self.pwm_log.append((pin, hz, "hz"))
    
    def setPeriodMicroseconds(self, pin, us):
        self.pwm_log.append((pin, us, "us"))


class MockWiFi:
    """Mock WiFi for testing."""
    def __init__(self):
        self.connected = False
        self.ssid = ""
        self.ip = "0.0.0.0"
        self.mac = "00:00:00:00:00:00"
        self.signal = -100
        self.log = []
    
    def begin(self):
        self.log.append("begin")
    
    def connect(self, ssid, password):
        self.log.append(f"connect {ssid}")
    
    def disconnect(self):
        self.log.append("disconnect")
    
    def end(self):
        self.log.append("end")
    
    def status(self):
        return 4 if self.connected else 0
    
    def connected(self):
        return self.connected
    
    def hostname(self, name):
        self.log.append(f"hostname {name}")
    
    def setDNS(self, dns1, dns2=None):
        self.log.append(f"setDNS {dns1}")
    
    def setClientID(self, client_id):
        self.log.append(f"setClientID {client_id}")
    
    def keepAlive(self, interval):
        self.log.append(f"keepAlive {interval}")
    
    def publish(self, topic, payload, qos=0, retained=False):
        self.log.append(f"publish {topic}: {payload}")
        return True
    
    def subscribe(self, topic, qos=0):
        self.log.append(f"subscribe {topic}")
        return True
    
    def loop(self):
        pass
    
    def client(self):
        return None


class MockBLE:
    """Mock BLE for testing."""
    def __init__(self):
        self.connected = False
        self.log = []
    
    def begin(self):
        self.log.append("begin")
    
    def end(self):
        self.log.append("end")
    
    def connect(self):
        self.connected = True
        self.log.append("connect")
    
    def disconnect(self):
        self.connected = False
        self.log.append("disconnect")
    
    def connected(self):
        return self.connected
    
    def broadcast(self, data):
        self.log.append(f"broadcast {data}")
    
    def scan(self):
        self.log.append("scan")


class MockPreferences:
    """Mock preferences storage for testing."""
    def __init__(self):
        self.storage = {}
        self.log = []
    
    def begin(self, namespace, read_only=False):
        self.log.append(f"begin {namespace}")
    
    def end(self):
        self.log.append("end")
    
    def putString(self, key, value):
        self.storage[key] = str(value)
        self.log.append(f"putString {key}")
    
    def getString(self, key, default=""):
        self.log.append(f"getString {key}")
        return self.storage.get(key, default)
    
    def putInt(self, key, value):
        self.storage[key] = int(value)
        self.log.append(f"putInt {key}")
    
    def getInt(self, key, default=0):
        self.log.append(f"getInt {key}")
        return self.storage.get(key, default)
    
    def putFloat(self, key, value):
        self.storage[key] = float(value)
        self.log.append(f"putFloat {key}")
    
    def getFloat(self, key, default=0.0):
        self.log.append(f"getFloat {key}")
        return self.storage.get(key, default)
    
    def remove(self, key):
        self.storage.pop(key, None)
        self.log.append(f"remove {key}")
    
    def clear(self):
        self.storage.clear()
        self.log.append("clear")
    
    def keys(self):
        self.log.append("keys")
        return list(self.storage.keys())


class MockSPIFFS:
    """Mock SPIFFS filesystem for testing."""
    def __init__(self):
        self.files = {}
        self.log = []
    
    def begin(self):
        self.log.append("begin")
        return True
    
    def end(self):
        self.log.append("end")
    
    def open(self, filename, mode="r"):
        self.log.append(f"open {filename} {mode}")
        if filename in self.files:
            return MockFile(self.files[filename])
        return None
    
    def remove(self, filename):
        self.files.pop(filename, None)
        self.log.append(f"remove {filename}")
    
    def rename(self, old_name, new_name):
        if old_name in self.files:
            self.files[new_name] = self.files.pop(old_name)
        self.log.append(f"rename {old_name} -> {new_name}")
    
    def list(self, path="/"):
        self.log.append(f"list {path}")
        return list(self.files.keys())
    
    def exists(self, filename):
        self.log.append(f"exists {filename}")
        return filename in self.files


class MockTemperatureSensor:
    """Mock temperature sensor for testing."""
    def __init__(self):
        self.temperature = 25.0
        self.log = []
    
    def begin(self):
        self.log.append("begin")
    
    def readTemperature(self):
        self.log.append("readTemperature")
        return self.temperature
    
    def setTemperature(self, temp):
        self.temperature = temp
        self.log.append(f"setTemperature {temp}")


class MockAccelerometer:
    """Mock accelerometer for testing."""
    def __init__(self):
        self.x = 0
        self.y = 0
        self.z = 0
        self.log = []
    
    def begin(self):
        self.log.append("begin")
    
    def readAcceleration(self, x, y, z):
        self.log.append("readAcceleration")
        x[0] = self.x
        y[0] = self.y
        z[0] = self.z
    
    def readAccelerationX(self):
        self.log.append("readAccelerationX")
        return self.x
    
    def readAccelerationY(self):
        self.log.append("readAccelerationY")
        return self.y
    
    def readAccelerationZ(self):
        self.log.append("readAccelerationZ")
        return self.z
    
    def setRange(self, range):
        self.log.append(f"setRange {range}")


class MockStepperMotor:
    """Mock stepper motor for testing.
    
    Tracks position, step_log, and released state.
    """
    def __init__(self):
        self.position = 0
        self.step_log = []
        self.released = False
        self.log = []
    
    def begin(self):
        self.log.append("begin")
    
    def release(self):
        self.released = True
        self.log.append("release")
    
    def releaseAll(self):
        self.release()
    
    def run(self, speed):
        self.released = False
        self.log.append(f"run {speed}")
    
    def runToPosition(self, position):
        self.log.append(f"runToPosition {position}")
        self.position = position
    
    def runToNewPosition(self, position):
        self.log.append(f"runToNewPosition {position}")
        self.position = position
    
    def step(self, steps, speed, direction):
        self.log.append(f"step {steps} speed={speed} dir={direction}")
        self.step_log.append((steps, speed, direction))
        self.position += steps * direction
    
    def currentPosition(self):
        self.log.append("currentPosition")
        return self.position
    
    def speed(self):
        self.log.append("speed")
        return 0
    
    def distanceToGo(self):
        self.log.append("distanceToGo")
        return 0


class MockDCMotor:
    """Mock DC motor for testing.
    
    Tracks speed, direction, and run_log.
    """
    def __init__(self):
        self.speed = 0
        self.direction = 0
        self.run_log = []
        self.log = []
    
    def begin(self):
        self.log.append("begin")
    
    def run(self, direction, speed):
        self.log.append(f"run dir={direction} speed={speed}")
        self.direction = direction
        self.speed = speed
        self.run_log.append((direction, speed))
    
    def brake(self):
        self.log.append("brake")
        self.speed = 0
    
    def release(self):
        self.log.append("release")
        self.speed = 0
    
    def currentSpeed(self):
        self.log.append("currentSpeed")
        return self.speed


class MockSerialPort:
    """Mock serial port for testing.
    
    Tracks tx_log and has inject_response() for simulating hardware replies.
    """
    def __init__(self):
        self.tx_log = []
        self.rx_log = []
        self.baud_rate = 9600
        self.log = []
    
    def begin(self, baud_rate=9600):
        self.baud_rate = baud_rate
        self.log.append(f"begin {baud_rate}")
    
    def end(self):
        self.log.append("end")
    
    def available(self):
        return len(self.rx_log)
    
    def read(self):
        if self.rx_log:
            return self.rx_log.pop(0)
        return -1
    
    def readStringUntil(self, delimiter):
        if self.rx_log:
            data = self.rx_log.pop(0)
            return data
        return ""
    
    def write(self, data):
        self.tx_log.append(data)
        self.log.append(f"write {data}")
    
    def print(self, data):
        self.tx_log.append(str(data))
        self.log.append(f"print {data}")
    
    def println(self, data=""):
        self.tx_log.append(str(data) + "\n")
        self.log.append(f"println {data}")
    
    def flush(self):
        self.log.append("flush")
    
    def inject_response(self, response):
        """Inject a response for simulating hardware replies."""
        self.rx_log.append(response)
        self.log.append(f"inject_response {response}")


class MockFile:
    """Mock file object for SPIFFS testing."""
    def __init__(self, content=""):
        self.content = content
        self.position = 0
        self.log = []
    
    def read(self):
        self.log.append("read")
        return self.content
    
    def readStringUntil(self, delimiter):
        self.log.append(f"readStringUntil {delimiter}")
        return self.content
    
    def write(self, data):
        self.log.append(f"write {data}")
    
    def close(self):
        self.log.append("close")
    
    def available(self):
        self.log.append("available")
        return len(self.content) - self.position
    
    def peek(self):
        self.log.append("peek")
        return self.content[self.position] if self.position < len(self.content) else -1
    
    def seek(self, pos):
        self.log.append(f"seek {pos}")
        self.position = pos
    
    def position(self):
        self.log.append("position")
        return self.position


# Arduino helper functions
def arduino_map(x, in_min, in_max, out_min, out_max):
    """Arduino map() function."""
    return int((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)


def arduino_constrain(x, a, b):
    """Arduino constrain() function."""
    return max(a, min(x, b))


def analog_to_voltage(analog_value, vref=3.3, resolution=4095):
    """Convert analog value to voltage."""
    return (analog_value / resolution) * vref

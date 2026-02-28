"""embedded_mocks.py — Mocks for Arduino/C++ embedded systems testing.

This module provides Python re-implementations and mocks for common embedded
systems components including I2C, SPI, UART, GPIO, WiFi, BLE, and NeoPixel.
"""
import io
import time
from unittest.mock import MagicMock, patch
from typing import Dict, List, Optional, Tuple, Any


class MockGPIO:
    """Mock GPIO pin operations."""
    
    def __init__(self):
        self.pins: Dict[int, int] = {}
        self.mode: Dict[int, int] = {}
    
    def pinMode(self, pin: int, mode: int):
        """Set pin mode (INPUT, OUTPUT, INPUT_PULLUP)."""
        self.mode[pin] = mode
    
    def digitalWrite(self, pin: int, value: int):
        """Set pin value (HIGH/LOW)."""
        self.pins[pin] = value
    
    def digitalRead(self, pin: int) -> int:
        """Read pin value."""
        return self.pins.get(pin, 0)
    
    def analogWrite(self, pin: int, value: int):
        """PWM write (simulated)."""
        self.pins[pin] = value
    
    def analogRead(self, pin: int) -> int:
        """Analog read (simulated 10-bit ADC)."""
        return self.pins.get(pin, 0)


class MockI2C:
    """Mock I2C bus operations."""
    
    def __init__(self, sda: int = 4, scl: int = 5, frequency: int = 100000):
        self.sda = sda
        self.scl = scl
        self.frequency = frequency
        self.devices: Dict[int, Dict[int, int]] = {}
        self._tx_buffer: bytes = b""
        self._rx_buffer: bytes = b""
        self.started = False
    
    def begin(self):
        """Initialize I2C."""
        self.started = True
    
    def beginTransmission(self, address: int):
        """Start transmission to a device."""
        self._tx_buffer = b""
        self._address = address
    
    def write(self, data: int):
        """Write data to transmission buffer."""
        if isinstance(data, int):
            self._tx_buffer += bytes([data])
        else:
            self._tx_buffer += data
    
    def endTransmission(self) -> int:
        """End transmission and store data."""
        if self._address not in self.devices:
            self.devices[self._address] = {}
        for i, byte in enumerate(self._tx_buffer):
            self.devices[self._address][i] = byte
        return 0
    
    def requestFrom(self, address: int, quantity: int) -> int:
        """Request data from a device."""
        self._rx_buffer = b""
        if address in self.devices:
            for i in range(min(quantity, len(self.devices[address]))):
                self._rx_buffer += bytes([self.devices[address].get(i, 0)])
        return len(self._rx_buffer)
    
    def available(self) -> int:
        """Return number of bytes available for reading."""
        return len(self._rx_buffer)
    
    def read(self) -> int:
        """Read one byte from receive buffer."""
        if self._rx_buffer:
            return self._rx_buffer[0]
        return 0


class MockSPI:
    """Mock SPI bus operations."""
    
    def __init__(self, sck: int = 13, miso: int = 12, mosi: int = 11, ss: int = 10):
        self.sck = sck
        self.miso = miso
        self.mosi = mosi
        self.ss = ss
        self._tx_buffer: bytes = b""
        self._rx_buffer: bytes = b""
        self.enabled = False
    
    def begin(self):
        """Initialize SPI."""
        self.enabled = True
    
    def transfer(self, data: int) -> int:
        """Simulate SPI transfer (full duplex)."""
        return data
    
    def write(self, data: bytes):
        """Write data."""
        self._tx_buffer = data
    
    def read(self) -> bytes:
        """Read data."""
        return self._rx_buffer


class MockUART:
    """Mock UART/serial communication."""
    
    def __init__(self, baudrate: int = 9600, rx_size: int = 256, tx_size: int = 256):
        self.baudrate = baudrate
        self._tx_log: bytes = b""
        self._rx_buffer: bytes = b""
        self._rx_pos = 0
        self._line_buffer: bytes = b""
    
    def begin(self, baudrate: int) -> bool:
        """Initialize serial at given baudrate."""
        self.baudrate = baudrate
        return True
    
    def write(self, data: bytes):
        """Write data to TX log."""
        if isinstance(data, str):
            data = data.encode()
        self._tx_log += data
    
    def print(self, data: str):
        """Print string to TX log."""
        self._tx_log += data.encode()
    
    def println(self, data: str):
        """Print string with newline to TX log."""
        self._tx_log += data.encode() + b"\n"
    
    def available(self) -> int:
        """Return number of bytes available for reading."""
        return len(self._rx_buffer) - self._rx_pos
    
    def read(self) -> int:
        """Read one byte."""
        if self._rx_pos < len(self._rx_buffer):
            byte = self._rx_buffer[self._rx_pos]
            self._rx_pos += 1
            return byte
        return -1
    
    def readBytes(self, buffer: bytearray, size: int) -> int:
        """Read bytes into buffer."""
        count = 0
        while count < size and self._rx_pos < len(self._rx_buffer):
            buffer[count] = self._rx_buffer[self._rx_pos]
            self._rx_pos += 1
            count += 1
        return count
    
    def readline(self) -> bytes:
        """Read a line (until newline)."""
        while self._rx_pos < len(self._rx_buffer):
            byte = self._rx_buffer[self._rx_pos]
            self._rx_pos += 1
            self._line_buffer += bytes([byte])
            if byte == ord('\n'):
                line = self._line_buffer
                self._line_buffer = b""
                return line
        return b""
    
    def inject_rx(self, data: bytes):
        """Inject data into RX buffer (for testing)."""
        if isinstance(data, str):
            data = data.encode()
        self._rx_buffer += data
    
    def flush(self):
        """Flush buffers."""
        self._line_buffer = b""


class MockNeoPixel:
    """Mock NeoPixel/WS2812 LED strip."""
    
    def __init__(self, num_pixels: int, pin: int = 6, brightness: int = 255):
        self.num_pixels = num_pixels
        self.pin = pin
        self.brightness = brightness
        self.pixels: List[Tuple[int, int, int]] = [(0, 0, 0)] * num_pixels
    
    def begin(self):
        """Initialize NeoPixel."""
        pass
    
    def setPixelColor(self, n: int, r: int, g: int, b: int):
        """Set pixel color."""
        if 0 <= n < self.num_pixels:
            self.pixels[n] = (r, g, b)
    
    def setPixelColor(self, n: int, color: int):
        """Set pixel color from RGB combination."""
        if 0 <= n < self.num_pixels:
            self.pixels[n] = (
                (color >> 16) & 0xFF,
                (color >> 8) & 0xFF,
                color & 0xFF
            )
    
    def show(self):
        """Update LED strip."""
        pass
    
    def Color(self, r: int, g: int, b: int) -> int:
        """Combine RGB values into single color."""
        return (r << 16) | (g << 8) | b


class MockWiFi:
    """Mock WiFi connectivity."""
    
    def __init__(self):
        self.connected = False
        self.ssid = ""
        self.ip = "192.168.1.100"
        self._tx_buffer: bytes = b""
    
    def begin(self, ssid: str, passkey: str = "") -> bool:
        """Connect to WiFi network."""
        self.ssid = ssid
        self.connected = True
        return True
    
    def status(self) -> int:
        """Return connection status."""
        return 3 if self.connected else 0
    
    def localIP(self) -> str:
        """Return local IP address."""
        return self.ip
    
    def printIP(self):
        """Print IP address."""
        pass
    
    def disconnect(self):
        """Disconnect from network."""
        self.connected = False


class MockBLE:
    """Mock Bluetooth Low Energy."""
    
    def __init__(self):
        self.connected = False
        self.name = ""
    
    def begin(self, name: str):
        """Initialize BLE."""
        self.name = name
        self.connected = True
    
    def available(self) -> int:
        """Return available bytes."""
        return 0
    
    def read(self) -> int:
        """Read one byte."""
        return -1
    
    def write(self, data: bytes):
        """Write data."""
        pass


class MockPreferences:
    """Mock non-volatile storage."""
    
    def __init__(self):
        self.data: Dict[str, Any] = {}
        self._namespace = ""
    
    def begin(self, namespace: str, read_only: bool = False) -> bool:
        """Begin preferences session."""
        self._namespace = namespace
        return True
    
    def end(self):
        """End preferences session."""
        pass
    
    def getUInt(self, key: str, default: int = 0) -> int:
        """Get unsigned int value."""
        return self.data.get(key, default)
    
    def getInt(self, key: str, default: int = 0) -> int:
        """Get int value."""
        return self.data.get(key, default)
    
    def getString(self, key: str, default: str = "") -> str:
        """Get string value."""
        return self.data.get(key, default)
    
    def putUInt(self, key: str, value: int):
        """Put unsigned int value."""
        self.data[key] = value
    
    def putInt(self, key: str, value: int):
        """Put int value."""
        self.data[key] = value
    
    def putString(self, key: str, value: str):
        """Put string value."""
        self.data[key] = value
    
    def remove(self, key: str):
        """Remove key."""
        if key in self.data:
            del self.data[key]


def arduino_map(x: int, in_min: int, in_max: int, out_min: int, out_max: int) -> int:
    """Arduino map() function re-implementation."""
    return int((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)


def arduino_constrain(x: float, a: float, b: float) -> float:
    """Arduino constrain() function re-implementation."""
    return max(a, min(x, b))


def analog_to_voltage(value: int, bits: int = 10, ref: float = 3.3) -> float:
    """Convert ADC raw value to voltage."""
    max_value = (1 << bits) - 1
    return (value / max_value) * ref


serial = MagicMock()
serial.Serial = MagicMock
serial.tools = MagicMock()
serial.tools.list_ports = MagicMock()

pyfirmata = MagicMock()
pyfirmata2 = MagicMock()

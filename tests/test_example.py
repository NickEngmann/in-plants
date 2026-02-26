"""test_example.py — Starter template for Arduino project tests.

Arduino .ino/.cpp files CANNOT be imported in Python. Instead:
1. READ the source files to understand the algorithms
2. RE-IMPLEMENT the logic in Python in this test file
3. Test the Python re-implementation with pytest

The `arduino` fixture provides constants (HIGH, LOW, A0-A5) and helpers
(map_value, constrain). Also see embedded_mocks.py for I2C/SPI/UART mocks.
DO NOT modify conftest.py.
"""
import pytest


def test_arduino_map():
    """Test Arduino map() function re-implementation."""
    def arduino_map(x, in_min, in_max, out_min, out_max):
        return (x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min
    
    assert arduino_map(0, 0, 1023, 0, 255) == 0
    assert arduino_map(512, 0, 1023, 0, 255) == 127
    assert arduino_map(1023, 0, 1023, 0, 255) == 255


def test_arduino_constrain():
    """Test Arduino constrain() function."""
    def arduino_constrain(x, a, b):
        return max(a, min(x, b))
    
    assert arduino_constrain(150, 0, 100) == 100
    assert arduino_constrain(-10, 0, 100) == 0
    assert arduino_constrain(50, 0, 100) == 50


def test_analog_voltage_conversion():
    """Test ADC raw value to voltage conversion."""
    def analog_to_voltage(value, bits=10, ref=3.3):
        max_value = (1 << bits) - 1
        return value * ref / max_value
    
    assert abs(analog_to_voltage(512, bits=10, ref=3.3) - 1.65) < 0.01
    assert abs(analog_to_voltage(0, bits=10) - 0.0) < 0.01
    assert abs(analog_to_voltage(1023, bits=10, ref=3.3) - 3.3) < 0.01


def test_serial_protocol_example():
    """Example: test a serial command protocol."""
    class MockUART:
        def __init__(self, baudrate=115200):
            self.baudrate = baudrate
            self._tx_log = b""
            self._rx_buffer = b""
        
        def write(self, data):
            self._tx_log += data
        
        def inject_rx(self, data):
            self._rx_buffer += data
        
        def readline(self):
            if b"\n" in self._rx_buffer:
                line, self._rx_buffer = self._rx_buffer.split(b"\n", 1)
                return line + b"\n"
            return b""
    
    uart = MockUART(baudrate=115200)
    # Simulate sending a command
    uart.write(b"AT+CMD\r\n")
    assert uart._tx_log == b"AT+CMD\r\n"
    # Simulate receiving a response
    uart.inject_rx(b"OK\r\n")
    assert uart.readline() == b"OK\r\n"


# TODO: Read the .ino source files and re-implement key algorithms below:
# def test_state_machine():
#     """Re-implement the state machine from the Arduino source."""
#     pass

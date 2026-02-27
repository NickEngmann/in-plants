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
from embedded_mocks import (
    MockI2C, MockSPI, MockUART, MockGPIO, MockNeoPixel,
    MockWiFi, MockBLE, MockPreferences,
    arduino_map, arduino_constrain, analog_to_voltage,
)


def test_arduino_map():
    """Test Arduino map() function re-implementation."""
    assert arduino_map(0, 0, 1023, 0, 255) == 0
    assert arduino_map(512, 0, 1023, 0, 255) == 127
    assert arduino_map(1023, 0, 1023, 0, 255) == 255


def test_arduino_constrain():
    """Test Arduino constrain() function."""
    assert arduino_constrain(150, 0, 100) == 100
    assert arduino_constrain(-10, 0, 100) == 0
    assert arduino_constrain(50, 0, 100) == 50


def test_analog_voltage_conversion():
    """Test ADC raw value to voltage conversion."""
    assert abs(analog_to_voltage(512, bits=10, ref=3.3) - 1.65) < 0.01
    assert abs(analog_to_voltage(0, bits=10) - 0.0) < 0.01
    assert abs(analog_to_voltage(1023, bits=10, ref=3.3) - 3.3) < 0.01


def test_serial_protocol_example():
    """Example: test a serial command protocol."""
    uart = MockUART(baudrate=115200)
    # Simulate sending a command
    uart.write(b"AT+CMD\r\n")
    assert uart._tx_log == b"AT+CMD\r\n"
    # Simulate receiving a response
    uart.inject_rx(b"OK\r\n")
    assert uart.readline() == b"OK\r\n"


def calculate_moisture_percentage(analog_value, min_val=300, max_val=850):
    """Calculate moisture percentage from analog sensor reading.
    
    From inplants-argon.ino:
    - min_moisture_analog = 300 (dry)
    - max_moisture_analog = 850 (wet)
    
    Returns:
        Moisture percentage (100 = wet, 0 = dry)
    """
    if analog_value <= min_val:
        return 100
    elif analog_value >= max_val:
        return 0
    else:
        return 100 - ((analog_value - min_val) * 100) // (max_val - min_val)


def test_moisture_percentage_wet_sensor():
    """Test moisture percentage for wet sensor (low analog value).
    
    When analog reading is at minimum (300), moisture should be 100%.
    """
    assert calculate_moisture_percentage(300) == 100
    assert calculate_moisture_percentage(400) == 82


def test_moisture_percentage_dry_sensor():
    """Test moisture percentage for dry sensor (high analog value).
    
    When analog reading is at maximum (850), moisture should be 0%.
    """
    assert calculate_moisture_percentage(850) == 0
    assert calculate_moisture_percentage(700) == 28


def test_moisture_percentage_mid_range():
    """Test moisture percentage for mid-range values."""
    # Mid-point: (300 + 850) / 2 = 575 should give ~50%
    assert calculate_moisture_percentage(575) == 50


def test_moisture_percentage_clamping():
    """Test that values outside range are properly clamped."""
    # Below minimum should clamp to 100%
    assert calculate_moisture_percentage(200) == 100
    # Above maximum should clamp to 0%
    assert calculate_moisture_percentage(1000) == 0


def test_watering_threshold_logic():
    """Test the watering threshold logic from loop().
    
    From the code: if (moisture_percentage < 50) triggers watering.
    This test verifies the threshold calculation.
    """
    # Below 50% - should trigger watering
    assert calculate_moisture_percentage(700) < 50  # 27% < 50%
    # Above 50% - should not trigger watering
    assert calculate_moisture_percentage(575) >= 50  # 50% >= 50%


def test_sensor_calibration():
    """Test sensor calibration with different min/max values.
    
    The sensor can be calibrated with different min/max values
    based on the specific soil and sensor characteristics.
    """
    # Custom calibration: dry=200, wet=700
    assert calculate_moisture_percentage(200, 200, 700) == 100
    assert calculate_moisture_percentage(700, 200, 700) == 0
    assert calculate_moisture_percentage(450, 200, 700) == 50

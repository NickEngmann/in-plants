"""test_example.py — Tests for Arduino moisture sensor project."""

"""Tests for the in-plants Arduino project.

This project publishes plant moisture data to the Particle cloud.
The tests verify the moisture calculation logic by re-implementing
the core algorithms in Python.
"""

import pytest
from embedded_mocks import (
    ArduinoConstants,
    digitalWrite,
    delay,
    analogRead,
    Particle
)

# Constants from the Arduino code
BOARD_LED = "D7"
MOISTURE_PIN = "A1"
ANALOG_MAX = 4095
BATT = 1


# Constants from the Arduino code
BOARD_LED = "D7"
MOISTURE_PIN = "A1"
ANALOG_MAX = 4095


def calculate_moisture_percentage(moisture_analog):
    """Re-implement the moisture percentage calculation from Arduino code.
    
    From the .ino file:
    float moisture_percentage = (100 - ( (moisture_analog/4095.00) * 100 ) );
    
    This calculates moisture percentage from analog reading.
    Higher analog values = lower moisture (sensor reads higher when dry)
    """
    return 100 - ((moisture_analog / ANALOG_MAX) * 100)


def test_moisture_percentage_calculation_dry():
    """Test moisture calculation for dry soil (high analog value)."""
    # Dry soil should give high analog reading (~4000)
    analog_dry = 4000
    percentage = calculate_moisture_percentage(analog_dry)
    # Should be low moisture percentage
    assert percentage < 25


def test_moisture_percentage_calculation_wet():
    """Test moisture calculation for wet soil (low analog value)."""
    # Wet soil should give low analog reading (~1000)
    analog_wet = 1000
    percentage = calculate_moisture_percentage(analog_wet)
    # Should be high moisture percentage
    assert percentage > 75


def test_moisture_percentage_calculation_medium():
    """Test moisture calculation for medium moisture (mid-range analog value)."""
    # Medium moisture ~2048 (half of max)
    analog_medium = 2048
    percentage = calculate_moisture_percentage(analog_medium)
    # Should be around 50%
    assert 45 < percentage < 55


def test_moisture_percentage_boundary_zero():
    """Test moisture calculation for zero analog reading (max moisture)."""
    percentage = calculate_moisture_percentage(0)
    assert percentage == 100.0


def test_moisture_percentage_boundary_max():
    """Test moisture calculation for max analog reading (dry)."""
    percentage = calculate_moisture_percentage(ANALOG_MAX)
    assert percentage == 0.0


def test_constrain_function():
    """Test the constrain function works correctly."""
    arduino = ArduinoConstants()
    
    # Test constraining within range
    assert arduino.constrain(50, 0, 100) == 50
    
    # Test constraining below minimum
    assert arduino.constrain(-10, 0, 100) == 0
    
    # Test constraining above maximum
    assert arduino.constrain(150, 0, 100) == 100


def test_mapf_function():
    """Test the floating point map function."""
    arduino = ArduinoConstants()
    
    # Test mapping 0-1024 to 0-100
    assert arduino.mapf(0, 0, 1024, 0, 100) == 0.0
    assert arduino.mapf(1024, 0, 1024, 0, 100) == 100.0
    assert arduino.mapf(512, 0, 1024, 0, 100) == 50.0


def test_particle_publish_mock():
    """Test that Particle.publish mock works without errors."""
    # This should not raise any errors
    Particle.publish("test_topic", "test_data", 60, False)


def test_digital_write_mock():
    """Test that digitalWrite mock works without errors."""
    # This should not raise any errors
    digitalWrite(BOARD_LED, "HIGH")
    digitalWrite(BOARD_LED, "LOW")


def test_delay_mock():
    """Test that delay mock works without errors."""
    # This should not raise any errors
    delay(1000)


def test_analog_read_default():
    """Test that analogRead returns a default value."""
    value = analogRead(MOISTURE_PIN)
    # Default mock value should be 2048 (mid-range)
    assert value == 2048


def test_moisture_calculation_consistency():
    """Test that moisture calculation is consistent for same inputs."""
    test_value = 3000
    result1 = calculate_moisture_percentage(test_value)
    result2 = calculate_moisture_percentage(test_value)
    assert result1 == result2


def test_moisture_percentage_range():
    """Test that moisture percentage is always between 0 and 100."""
    for analog_value in [0, 1000, 2048, 3000, 4095]:
        percentage = calculate_moisture_percentage(analog_value)
        assert 0 <= percentage <= 100


def test_voltage_calculation_when_batt_enabled():
    """Test voltage calculation when BATT > 1 (from loop function)."""
    # From the .ino: if(BATT > 1){ float voltage = analogRead(BATT) * 0.0011224; }
    # Since BATT = 1 in our mock, this condition is false
    # But we can test the voltage calculation formula
    analog_batt = 2048
    voltage = analog_batt * 0.0011224
    assert 2.0 < voltage < 2.5

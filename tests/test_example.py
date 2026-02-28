"""test_example.py — Tests for Arduino moisture sensor project."""

import pytest


class ArduinoConstants:
    """Arduino-like constants for testing."""
    pass


def moisture_percentage(moisture_analog):
    """Re-implement the moisture percentage calculation from Arduino code.
    
    From the .ino file:
    float moisture_percentage = (100 - ( (moisture_analog/4095.00) * 100 ) );
    """
    return 100 - ((moisture_analog / 4095.00) * 100)


def test_moisture_percentage_zero_analog():
    """When analog reading is 0 (maximum moisture), percentage should be 100%."""
    assert moisture_percentage(0) == 100.0


def test_moisture_percentage_full_analog():
    """When analog reading is 4095 (maximum dryness), percentage should be 0%."""
    assert moisture_percentage(4095) == 0.0


def test_moisture_percentage_mid_range():
    """Test mid-range analog reading."""
    # 2047 is roughly half of 4095
    # percentage = 100 - (2047/4095 * 100) = 100 - 50 = 50
    result = moisture_percentage(2047)
    assert abs(result - 50.0) < 0.1


def test_moisture_percentage_boundary_values():
    """Test boundary values for moisture calculation."""
    # Very wet (near 0)
    assert moisture_percentage(100) > 97
    
    # Very dry (near 4095)
    assert moisture_percentage(4000) < 3


# TODO: Read the .ino source files and re-implement key algorithms below:
# def test_state_machine():
#     """Re-implement the state machine from the Arduino source."""
#     pass

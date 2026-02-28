"""test_example.py — Starter template for Arduino project tests.

Arduino .ino/.cpp files CANNOT be imported in Python. Instead:
1. READ the source files to understand the algorithms
2. RE-IMPLEMENT those algorithms in Python in your test file
3. Write pytest tests that verify the Python re-implementation

The arduino fixture provides constants (HIGH/LOW/INPUT/OUTPUT) and helpers
(map_value, constrain) matching Arduino's built-in functions.
"""
import pytest


@pytest.fixture
def arduino_constants():
    """Provides Arduino-like constants and helpers for testing re-implemented logic."""
    class ArduinoConstants:
        HIGH = 1
        LOW = 0
        INPUT = 0
        OUTPUT = 1
        
        @staticmethod
        def map_value(x, in_min, in_max, out_min, out_max):
            """Re-implementation of Arduino's map() function."""
            return int((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)
        
        @staticmethod
        def constrain(x, a, b):
            """Re-implementation of Arduino's constrain() function."""
            return max(a, min(x, b))
    
    return ArduinoConstants()


# Example test showing how to use the arduino fixture
def test_map_value_example(arduino_constants):
    """Test the map_value helper from the arduino fixture."""
    # Map 512 from 0-1023 range to 0-255 range
    assert arduino_constants.map_value(512, 0, 1023, 0, 255) == 127


def test_constrain_example(arduino_constants):
    """Test the constrain helper from the arduino fixture."""
    # Constrain 150 to 0-100 range
    assert arduino_constants.constrain(150, 0, 100) == 100
    # Constrain -10 to 0-100 range
    assert arduino_constants.constrain(-10, 0, 100) == 0
    # Constrain 50 to 0-100 range
    assert arduino_constants.constrain(50, 0, 100) == 50


# TODO: Read the .ino source files and re-implement key algorithms below:
# def test_state_machine():
#     """Re-implement the state machine from the Arduino source."""
#     pass

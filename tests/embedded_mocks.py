"""Mock Arduino environment for testing moisture sensor logic."""

import math


# Analog pin constants
A0 = 14
A1 = 15
A2 = 16
A3 = 17


class ArduinoConstants:
    """Arduino-like constants for testing."""
    HIGH = 1
    LOW = 0
    
    def map_value(self, x, in_min, in_max, out_min, out_max):
        """Arduino's map() function implementation."""
        return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


def digital_read(pin):
    """Mock digitalRead function."""
    return 0


def analog_read(pin):
    """Mock analogRead function."""
    return 0


def map_value(x, in_min, in_max, out_min, out_max):
    """Arduino's map() function."""
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

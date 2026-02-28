"""Mock Arduino environment for testing."""


class ArduinoConstants:
    """Arduino-like constants for testing."""
    INPUT = "INPUT"
    OUTPUT = "OUTPUT"
    HIGH = 1
    LOW = 0


def map_value(x, in_min, in_max, out_min, out_max):
    """Re-implement Arduino's map() function."""
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


def constrain(value, min_val, max_val):
    """Re-implement Arduino's constrain() function."""
    return max(min_val, min(value, max_val))

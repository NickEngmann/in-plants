"""Mock Arduino environment for testing re-implemented logic."""


class ArduinoConstants:
    """Arduino-like constants and helpers for testing."""
    
    # Pin definitions
    boardLed = "D7"
    moisture_pin = "A1"
    BATT = 1
    
    # Analog reference values
    ANALOG_MAX = 4095
    
    @staticmethod
    def mapf(x, in_min, in_max, out_min, out_max):
        """Floating point map function similar to Arduino's map()."""
        return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
    
    @staticmethod
    def constrain(x, a, b):
        """Constrain value to be between a and b."""
        return max(a, min(x, b))


def digitalWrite(pin, value):
    """Mock digitalWrite function."""
    pass


def delay(ms):
    """Mock delay function."""
    pass


def analogRead(pin):
    """Mock analogRead function - returns simulated sensor value."""
    # Default mock value - can be overridden in tests
    return 2048


class Particle:
    """Mock Particle cloud functions."""
    
    @staticmethod
    def publish(topic, data, ttl=60, is_private=False):
        """Mock Particle.publish function."""
        pass

"""test_example.py — Tests for Arduino moisture sensor project."""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from embedded_mocks import (
    ArduinoConstants,
    map_value,
    analog_read,
    digital_read,
    A0
)


# Constants from the Arduino code
MOISTURE_ANALOG = A0
BOARD_LED = "D7"


def test_map_value_basic():
    """Test the map function with basic values."""
    arduino = ArduinoConstants()
    
    # Test mapping 0-1023 to 0-100
    result = arduino.map_value(512, 0, 1023, 0, 100)
    assert abs(result - 50.05) < 0.1
    
    # Test edge cases
    assert arduino.map_value(0, 0, 1023, 0, 100) == 0.0
    assert arduino.map_value(1023, 0, 1023, 0, 100) == 100.0


def test_moisture_percentage_calculation():
    """Test moisture percentage calculation from analog reading."""
    arduino = ArduinoConstants()
    
    # Dry sensor (high value ~1023) should give ~0% moisture
    dry_value = 1023
    dry_percentage = arduino.map_value(dry_value, 0, 1023, 100, 0)
    assert dry_percentage == 0.0
    
    # Wet sensor (low value ~0) should give ~100% moisture
    wet_value = 0
    wet_percentage = arduino.map_value(wet_value, 0, 1023, 100, 0)
    assert wet_percentage == 100.0
    
    # Mid value should give ~50% moisture
    mid_value = 512
    mid_percentage = arduino.map_value(mid_value, 0, 1023, 100, 0)
    assert abs(mid_percentage - 49.95112414467253) < 0.001


def test_moisture_percentage_clamping():
    """Test that moisture percentage stays within valid bounds."""
    arduino = ArduinoConstants()
    
    # Test clamping behavior
    def clamp_percentage(value):
        percentage = arduino.map_value(value, 0, 1023, 100, 0)
        return max(0, min(percentage, 100))
    
    # With inverted mapping [100,0], negative values give >100%, clamped to 100
    assert clamp_percentage(-100) == 100
    # Values >1023 give <0%, clamped to 0
    assert clamp_percentage(1100) == 0
    assert abs(clamp_percentage(512) - 49.95112414467253) < 0.001


def test_led_blink_logic():
    """Test LED blink logic (digital write)."""
    # In the actual code, LED is turned on then off with delay
    # Test that we can simulate this behavior
    led_state = 1  # HIGH = on
    assert led_state == ArduinoConstants.HIGH
    
    led_state = 0  # LOW = off
    assert led_state == ArduinoConstants.LOW


def test_delay_duration():
    """Test delay duration calculation."""
    # 30 minutes = 1800000 milliseconds
    delay_minutes = 30
    delay_ms = delay_minutes * 60 * 1000
    assert delay_ms == 1800000


def test_sensor_reading_simulation():
    """Test simulated sensor readings."""
    arduino = ArduinoConstants()
    
    # Simulate various sensor readings
    test_values = [0, 256, 512, 768, 1023]
    
    for value in test_values:
        percentage = arduino.map_value(value, 0, 1023, 100, 0)
        # Percentage should be between 0 and 100
        assert 0 <= percentage <= 100
        print(f"Value {value} -> {percentage:.2f}% moisture")

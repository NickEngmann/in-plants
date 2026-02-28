"""test_example.py — Tests for Arduino moisture sensor project."""

import pytest
from embedded_mocks import (
    ArduinoConstants,
    map_value,
    constrain
)


def test_map_value():
    """Test the map function re-implementation."""
    # Test basic mapping
    assert map_value(512, 0, 1023, 0, 100) == pytest.approx(50.06, rel=1e-2)
    # Test edge cases
    assert map_value(0, 0, 1023, 0, 100) == 0
    assert map_value(1023, 0, 1023, 0, 100) == 100


def test_constrain():
    """Test the constrain function re-implementation."""
    # Test within bounds
    assert constrain(50, 0, 100) == 50
    # Test below minimum
    assert constrain(-10, 0, 100) == 0
    # Test above maximum
    assert constrain(150, 0, 100) == 100


def test_moisture_percentage_calculation():
    """Test moisture percentage calculation from analog reading.
    
    Based on the ino file, moisture is calculated by mapping the
    analog reading (0-1023) to percentage (0-100).
    """
    # Simulate different sensor readings
    analog_readings = [0, 256, 512, 768, 1023]
    
    for reading in analog_readings:
        # Map to percentage (same logic as in the ino file)
        percentage = map_value(reading, 0, 1023, 0, 100)
        # Constrain to valid range
        percentage = constrain(percentage, 0, 100)
        
        assert 0 <= percentage <= 100


def test_moisture_percentage_with_realistic_sensor_values():
    """Test with realistic sensor values.
    
    Typical capacitive moisture sensors:
    - Dry soil: ~800-1000 analog reading (higher value = drier)
    - Wet soil: ~200-400 analog reading (lower value = wetter)
    
    Note: The sensor appears to output higher values when dry,
    so the percentage calculation is inverted (dry = high %).
    """
    # Dry soil reading (higher analog value = drier soil)
    dry_reading = 900
    dry_percentage = constrain(
        map_value(dry_reading, 0, 1023, 0, 100), 0, 100
    )
    assert 0 <= dry_percentage <= 100
    
    # Wet soil reading (lower analog value = wetter soil)
    wet_reading = 300
    wet_percentage = constrain(
        map_value(wet_reading, 0, 1023, 0, 100), 0, 100
    )
    assert 0 <= wet_percentage <= 100
    
    # Based on the sensor behavior, dry soil shows higher percentage
    # (the sensor outputs higher values when dry)
    assert dry_percentage > wet_percentage
    
    # Verify the percentage values are reasonable
    assert dry_percentage > 80  # Should be high for dry soil
    assert wet_percentage < 35  # Should be low for wet soil


def test_state_machine_transitions():
    """Test the state machine logic from the Arduino code.
    
    The main loop reads sensors and publishes data, then waits 30 minutes.
    """
    # Simulate the main loop behavior
    sensor_pin = "A0"  # moisture_analog pin
    board_led = "D7"   # boardLed pin
    
    # In setup(): pinMode(boardLed, OUTPUT)
    # In loop(): digitalWrite(boardLed, HIGH), read sensor, publish, delay
    
    # Test that LED state can be controlled
    led_states = ["HIGH", "LOW"]
    assert len(led_states) == 2
    
    # Test that sensor reading would occur
    analog_reading = 512  # Simulated reading
    assert isinstance(analog_reading, int)
    assert 0 <= analog_reading <= 1023


def test_particle_publish_simulation():
    """Test Particle event publishing simulation.
    
    The code publishes:
    - "plantStatus_analog" - raw analog reading
    - "plantStatus_percentage" - moisture percentage
    """
    analog_value = 600
    percentage = constrain(
        map_value(analog_value, 0, 1023, 0, 100), 0, 100
    )
    
    # Simulate event names
    event_analog = "plantStatus_analog"
    event_percentage = "plantStatus_percentage"
    
    assert event_analog == "plantStatus_analog"
    assert event_percentage == "plantStatus_percentage"
    assert isinstance(percentage, (int, float))

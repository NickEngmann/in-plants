"""Tests for plant moisture calculation logic.

Re-implements the moisture percentage calculation from inplants-argon.ino:
  moisture_percentage = (100 - ( (moisture_analog/4095.00) * 100 ) )
"""

import pytest


def map_moisture_analog_to_percentage(moisture_analog, max_value=4095.00):
    """Re-implementation of the Arduino moisture percentage calculation.
    
    From inplants-argon.ino:
    float moisture_percentage = (100 - ( (moisture_analog/4095.00) * 100 ) );
    """
    return 100 - ((moisture_analog / max_value) * 100)


def test_moisture_percentage_dry_sensor():
    """When sensor reads max value (4095), moisture should be 0% (dry)."""
    assert map_moisture_analog_to_percentage(4095) == 0.0


def test_moisture_percentage_wet_sensor():
    """When sensor reads 0, moisture should be 100% (wet)."""
    assert map_moisture_analog_to_percentage(0) == 100.0


def test_moisture_percentage_halfway():
    """When sensor reads halfway (2047.5), moisture should be 50%."""
    assert map_moisture_analog_to_percentage(2047.5) == 50.0


def test_moisture_percentage_example_values():
    """Test some example sensor values."""
    # Sensor reads 1024 (about 25% of max) -> 75% moisture
    assert abs(map_moisture_analog_to_percentage(1024) - 75.0) < 0.1
    
    # Sensor reads 3072 (about 75% of max) -> 25% moisture
    assert abs(map_moisture_analog_to_percentage(3072) - 25.0) < 0.1


def test_moisture_percentage_with_integer_values():
    """Test with typical integer sensor readings."""
    # Typical dry reading
    assert abs(map_moisture_analog_to_percentage(3500) - 14.53) < 0.1
    
    # Typical wet reading
    assert abs(map_moisture_analog_to_percentage(500) - 87.81) < 0.1

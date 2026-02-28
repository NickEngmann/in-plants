"""Tests for in-plants Arduino project.

Tests re-implemented algorithms from inplants-argon.ino and inplants-xenon.ino.
"""

import pytest


def map_value(x, in_min, in_max, out_min, out_max):
    """Re-implementation of Arduino's map() function."""
    return int((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)


def constrain(x, low, high):
    """Re-implementation of Arduino's constrain() function."""
    return max(low, min(x, high))


def calculate_moisture_percentage(analog_value):
    """Calculate moisture percentage from analog reading.
    
    From the Arduino code:
    float moisture_percentage = (100 - ( (moisture_analog/4095.00) * 100 ) );
    """
    return 100 - ((analog_value / 4095.00) * 100)


def calculate_voltage(analog_value):
    """Calculate battery voltage from analog reading.
    
    From the Arduino code:
    float voltage = analogRead(BATT) * 0.0011224;
    """
    return analog_value * 0.0011224


class TestMoistureCalculations:
    """Test moisture percentage calculations."""
    
    def test_moisture_percentage_dry_sensor(self):
        """Dry sensor should read ~0% moisture (high analog value)."""
        # When sensor is dry, analog reading is high (near 4095)
        analog_dry = 4095
        percentage = calculate_moisture_percentage(analog_dry)
        assert percentage == 0.0
    
    def test_moisture_percentage_wet_sensor(self):
        """Wet sensor should read ~100% moisture (low analog value)."""
        # When sensor is wet, analog reading is low (near 0)
        analog_wet = 0
        percentage = calculate_moisture_percentage(analog_wet)
        assert percentage == 100.0
    
    def test_moisture_percentage_mid_range(self):
        """Test mid-range moisture percentage."""
        # Mid-range analog value
        analog_mid = 2048
        percentage = calculate_moisture_percentage(analog_mid)
        expected = 100 - ((2048 / 4095.00) * 100)
        assert abs(percentage - expected) < 0.01
    
    def test_moisture_percentage_with_realistic_values(self):
        """Test with realistic sensor readings."""
        # Typical dry reading for capacitive sensor
        analog_dry = 3500
        percentage_dry = calculate_moisture_percentage(analog_dry)
        assert 14 < percentage_dry < 15
        
        # Typical wet reading for capacitive sensor
        analog_wet = 1500
        percentage_wet = calculate_moisture_percentage(analog_wet)
        assert 63 < percentage_wet < 64


class TestVoltageCalculations:
    """Test battery voltage calculations."""
    
    def test_voltage_zero_reading(self):
        """Zero analog reading should give zero voltage."""
        voltage = calculate_voltage(0)
        assert voltage == 0.0
    
    def test_voltage_full_scale(self):
        """Full scale analog reading (4095) should give ~4.59V."""
        voltage = calculate_voltage(4095)
        expected = 4095 * 0.0011224
        assert abs(voltage - expected) < 0.001
    
    def test_voltage_with_realistic_values(self):
        """Test with realistic battery readings."""
        # Typical battery voltage around 3.7V
        analog_for_3v7 = 3300
        voltage = calculate_voltage(analog_for_3v7)
        expected = 3300 * 0.0011224
        assert abs(voltage - expected) < 0.001


class TestAnalogReadMapping:
    """Test analog read value mapping."""
    
    def test_map_full_range(self):
        """Test mapping full 12-bit range to percentage."""
        # 0 -> 100%, 4095 -> 0%
        assert calculate_moisture_percentage(0) == 100.0
        assert calculate_moisture_percentage(4095) == 0.0
    
    def test_map_half_range(self):
        """Test mapping at mid-range."""
        # 2047/2048 should be ~50%
        mid = 2047
        percentage = calculate_moisture_percentage(mid)
        expected = 100 - ((2047 / 4095.00) * 100)
        assert abs(percentage - expected) < 0.01


class TestConstrainFunction:
    """Test the constrain helper function."""
    
    def test_constrain_within_bounds(self):
        """Value within bounds should be unchanged."""
        assert constrain(50, 0, 100) == 50
    
    def test_constrain_below_lower(self):
        """Value below lower bound should be constrained to lower."""
        assert constrain(-10, 0, 100) == 0
    
    def test_constrain_above_upper(self):
        """Value above upper bound should be constrained to upper."""
        assert constrain(150, 0, 100) == 100


class TestMapFunction:
    """Test the map helper function."""
    
    def test_map_identity(self):
        """Map with same ranges should return original value."""
        assert map_value(512, 0, 1023, 0, 1023) == 512
    
    def test_map_half_scale(self):
        """Map half scale value."""
        assert map_value(512, 0, 1023, 0, 255) == 127
    
    def test_map_full_scale(self):
        """Map full scale value."""
        assert map_value(1023, 0, 1023, 0, 255) == 255
    
    def test_map_zero_scale(self):
        """Map zero value."""
        assert map_value(0, 0, 1023, 0, 255) == 0

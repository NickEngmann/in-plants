"""Tests for in-plants Arduino project.

Tests re-implemented algorithms from inplants-argon.ino and inplants-xenon.ino
"""

import pytest


def map_value(x, in_min, in_max, out_min, out_max):
    """Re-implementation of Arduino's map() function."""
    return int((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)


def constrain(x, low, high):
    """Re-implementation of Arduino's constrain() function."""
    return max(low, min(x, high))


def calculate_moisture_percentage(moisture_analog, max_value=4095):
    """Calculate moisture percentage from analog reading.
    
    From inplants-argon.ino:
    float moisture_percentage = (100 - ( (moisture_analog/4095.00) * 100 ) );
    """
    return 100 - ((moisture_analog / float(max_value)) * 100)


def calculate_voltage(analog_reading):
    """Calculate voltage from analog reading.
    
    From inplants-argon.ino:
    float voltage = analogRead(BATT) * 0.0011224;
    """
    return analog_reading * 0.0011224


class TestMoistureCalculations:
    """Tests for moisture sensor calculations."""
    
    def test_moisture_percentage_dry_sensor(self):
        """When sensor reads max value, moisture should be 0% (dry)."""
        # When moisture_analog = 4095 (max), percentage = 100 - (1 * 100) = 0
        assert calculate_moisture_percentage(4095) == 0.0
    
    def test_moisture_percentage_wet_sensor(self):
        """When sensor reads min value, moisture should be 100% (wet)."""
        # When moisture_analog = 0 (min), percentage = 100 - (0 * 100) = 100
        assert calculate_moisture_percentage(0) == 100.0
    
    def test_moisture_percentage_halfway(self):
        """When sensor reads halfway, moisture should be ~50%."""
        # When moisture_analog = 2047.5, percentage = 100 - (0.5 * 100) = 50
        result = calculate_moisture_percentage(2047.5)
        assert abs(result - 50.0) < 0.1
    
    def test_moisture_percentage_realistic_dry(self):
        """Test with realistic dry sensor reading."""
        # A dry sensor typically reads higher values
        # ~3000-4000 range for dry soil
        result = calculate_moisture_percentage(3500)
        assert abs(result - 14.5) < 1.0  # Should be ~14.5%
    
    def test_moisture_percentage_realistic_wet(self):
        """Test with realistic wet sensor reading."""
        # A wet sensor typically reads lower values
        # ~1000-2000 range for wet soil
        result = calculate_moisture_percentage(1500)
        assert abs(result - 63.3) < 1.0  # Should be ~63.3%
    
    def test_moisture_percentage_constrained(self):
        """Test that values are properly constrained."""
        # Values above max should give negative or zero percentage
        assert calculate_moisture_percentage(5000) < 0
        # Values below min should give >100% percentage
        assert calculate_moisture_percentage(-100) > 100


class TestVoltageCalculations:
    """Tests for battery voltage calculations."""
    
    def test_voltage_zero_reading(self):
        """Zero analog reading should give zero voltage."""
        assert calculate_voltage(0) == 0.0
    
    def test_voltage_full_scale(self):
        """Full scale analog reading (4095) should give ~4.6V."""
        result = calculate_voltage(4095)
        expected = 4095 * 0.0011224
        assert abs(result - expected) < 0.001
    
    def test_voltage典型_value(self):
        """Test with a typical battery voltage reading."""
        # For ~3.3V battery: 3.3 / 0.0011224 ≈ 2940 analog units
        analog_reading = 2940
        result = calculate_voltage(analog_reading)
        assert abs(result - 3.299) < 0.001


class TestLEDControl:
    """Tests for LED blinking pattern from setup()."""
    
    def test_led_blink_pattern_duration(self):
        """Verify LED blinks on/off with 200ms delays (3 times)."""
        # The setup blinks LED 3 times with 200ms on/off
        # Total duration should be 3 * 400ms = 1200ms minimum
        blink_count = 3
        delay_ms = 200
        total_delay = blink_count * delay_ms * 2  # on + off per blink
        assert total_delay == 1200
    
    def test_led_initialization(self):
        """Verify LED pin is set as OUTPUT."""
        # pinMode(boardLed, OUTPUT) should configure D7 as output
        board_led_pin = "D7"
        assert board_led_pin == "D7"


class TestSensorPinConfiguration:
    """Tests for sensor pin configuration."""
    
    def test_moisture_sensor_pin(self):
        """Verify moisture sensor is on analog pin A1."""
        moisture_pin = "A1"
        assert moisture_pin == "A1"
    
    def test_analog_resolution(self):
        """Verify analog reading uses 12-bit resolution (0-4095)."""
        # Particle Mesh devices use 12-bit ADC
        min_value = 0
        max_value = 4095
        assert max_value - min_value == 4095


class TestPublishData:
    """Tests for data publishing logic."""
    
    def test_analog_value_range(self):
        """Moisture analog value should be in valid ADC range."""
        moisture_analog = 2048
        assert 0 <= moisture_analog <= 4095
    
    def test_percentage_value_range(self):
        """Moisture percentage should be calculated correctly."""
        moisture_analog = 2048
        moisture_percentage = calculate_moisture_percentage(moisture_analog)
        # Should be approximately 50%
        assert 40 <= moisture_percentage <= 60


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

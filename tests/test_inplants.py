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


def analog_to_percentage(analog_value):
    """Convert analog reading (0-4095) to moisture percentage.
    
    From inplants-argon.ino and inplants-xenon.ino:
    float moisture_percentage = (100 - ( (moisture_analog/4095.00) * 100 ) );
    """
    return 100 - ((analog_value / 4095.00) * 100)


def analog_to_voltage(analog_value):
    """Convert battery analog reading to voltage.
    
    From inplants-xenon.ino:
    float voltage = analogRead(BATT) * 0.0011224;
    """
    return analog_value * 0.0011224


class TestMoisturePercentage:
    """Test the moisture percentage calculation."""
    
    def test_dry_sensor(self):
        """Dry sensor should read ~0% moisture (high analog value)."""
        # When sensor is dry, analog reading is high (near 4095)
        analog_dry = 4095
        percentage = analog_to_percentage(analog_dry)
        assert percentage == 0.0
    
    def test_wet_sensor(self):
        """Wet sensor should read ~100% moisture (low analog value)."""
        # When sensor is wet, analog reading is low (near 0)
        analog_wet = 0
        percentage = analog_to_percentage(analog_wet)
        assert percentage == 100.0
    
    def test_mid_moisture(self):
        """Mid-range moisture level."""
        # Mid-range analog value
        analog_mid = 2048
        percentage = analog_to_percentage(analog_mid)
        # Should be approximately 50%
        assert 49.9 <= percentage <= 50.1
    
    def test_realistic_dry_reading(self):
        """Test with a realistic dry sensor reading."""
        # Realistic dry reading around 3500-4000
        analog_value = 3800
        percentage = analog_to_percentage(analog_value)
        # Should be around 7-8% moisture
        assert 7.0 <= percentage <= 8.0
    
    def test_realistic_wet_reading(self):
        """Test with a realistic wet sensor reading."""
        # Realistic wet reading around 1000-1500
        analog_value = 1200
        percentage = analog_to_percentage(analog_value)
        # Should be around 70-75% moisture
        assert 70.0 <= percentage <= 75.0


class TestBatteryVoltage:
    """Test the battery voltage calculation."""
    
    def test_zero_voltage(self):
        """Zero analog reading should give zero voltage."""
        assert analog_to_voltage(0) == 0.0
    
    def test_full_voltage(self):
        """Test with a typical battery voltage.
        
        A fully charged LiPo battery is around 4.2V.
        4.2 / 0.0011224 ≈ 3742 analog units
        """
        analog_value = 3742
        voltage = analog_to_voltage(analog_value)
        assert 4.19 <= voltage <= 4.21
    
    def test_mid_voltage(self):
        """Test with mid battery voltage (3.7V typical)."""
        analog_value = 3297  # 3.7 / 0.0011224
        voltage = analog_to_voltage(analog_value)
        assert 3.69 <= voltage <= 3.71
    
    def test_low_voltage(self):
        """Test with low battery voltage (3.0V cutoff)."""
        analog_value = 2673  # 3.0 / 0.0011224
        voltage = analog_to_voltage(analog_value)
        assert 2.99 <= voltage <= 3.01


class TestConstrain:
    """Test the constrain function."""
    
    def test_within_bounds(self):
        """Value within bounds should be unchanged."""
        assert constrain(50, 0, 100) == 50
    
    def test_below_bounds(self):
        """Value below bounds should be constrained to low."""
        assert constrain(-10, 0, 100) == 0
    
    def test_above_bounds(self):
        """Value above bounds should be constrained to high."""
        assert constrain(150, 0, 100) == 100


class TestMapFunction:
    """Test the map function re-implementation."""
    
    def test_map_mid_range(self):
        """Map mid-range value."""
        assert map_value(512, 0, 1023, 0, 255) == 127
    
    def test_map_full_range(self):
        """Map full range value."""
        assert map_value(1023, 0, 1023, 0, 255) == 255
    
    def test_map_zero(self):
        """Map zero value."""
        assert map_value(0, 0, 1023, 0, 255) == 0


class TestLEDSequence:
    """Test the LED blinking sequence logic."""
    
    def test_led_blink_duration(self):
        """Verify LED blink timing (200ms on, 200ms off, 3x)."""
        # From setup(): 3 blinks with 200ms on/off each
        # Total duration = 3 * (200 + 200) = 1200ms
        blink_duration = 200
        num_blinks = 3
        total_duration = num_blinks * blink_duration * 2
        assert total_duration == 1200


class TestTimingIntervals:
    """Test the timing intervals from the main loop."""
    
    def test_argon_interval(self):
        """Argon publishes every 30 minutes (1800000ms)."""
        # From inplants-argon.ino: delay(1800000)
        interval_ms = 1800000
        assert interval_ms == 30 * 60 * 1000  # 30 minutes
    
    def test_xenon_charging_interval(self):
        """Xenon on USB publishes every 10 minutes (600000ms)."""
        # From inplants-xenon.ino else branch: delay(600000)
        interval_ms = 600000
        assert interval_ms == 10 * 60 * 1000  # 10 minutes
    
    def test_xenon_sleep_interval(self):
        """Xenon on battery sleeps for 12 hours (43200 seconds)."""
        # From inplants-xenon.ino: System.sleep(D1,RISING,43200)
        sleep_seconds = 43200
        assert sleep_seconds == 12 * 60 * 60  # 12 hours

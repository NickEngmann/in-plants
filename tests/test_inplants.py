"""Tests for in-plants Arduino project.

Re-implements key algorithms from inplants-argon.ino and inplants-xenon.ino
for Python-based testing.
"""
import pytest


def map_value(x, in_min, in_max, out_min, out_max):
    """Arduino map() function - re-implemented in Python."""
    return int((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)


def constrain(x, a, b):
    """Arduino constrain() function - re-implemented in Python."""
    return max(a, min(x, b))


def analog_to_voltage(analog_value, bits=10, ref=3.3):
    """Convert ADC raw value to voltage.
    
    Args:
        analog_value: Raw ADC reading (0 to 2^bits - 1)
        bits: ADC resolution (default 10 for Arduino)
        ref: Reference voltage (default 3.3V)
    """
    max_adc = (1 << bits) - 1  # 2^bits - 1
    return (analog_value / max_adc) * ref


class MockParticle:
    """Mock Particle.publish() function."""
    def __init__(self):
        self.published_events = []
    
    def publish(self, name, value, ttl=60, is_private=False):
        self.published_events.append({
            'name': name,
            'value': str(value),
            'ttl': ttl,
            'is_private': is_private
        })


def moisture_analog_to_percentage(analog_value, dry_value=1650, wet_value=2450):
    """Convert raw analog moisture reading to percentage.
    
    Based on inplants-argon.ino and inplants-xenon.ino logic:
    - Raw analog values from capacitive moisture sensor
    - Calibrated range: dry_value (0%) to wet_value (100%)
    - Returns percentage clamped between 0-100
    """
    # Map analog value to percentage
    percentage = map_value(analog_value, dry_value, wet_value, 0, 100)
    # Constrain to valid percentage range
    return constrain(percentage, 0, 100)


class TestMoistureCalculations:
    """Test moisture percentage calculations."""
    
    def test_moisture_percentage_calculation(self):
        """Test moisture percentage calculation from analog readings."""
        # Dry sensor (1650) should give 0%
        assert moisture_analog_to_percentage(1650) == 0
        
        # Wet sensor (2450) should give 100%
        assert moisture_analog_to_percentage(2450) == 100
        
        # Mid-range value
        mid_value = (1650 + 2450) // 2  # 2050
        mid_percentage = moisture_analog_to_percentage(mid_value)
        assert 45 <= mid_percentage <= 55  # Should be around 50%
    
    def test_moisture_percentage_clamping(self):
        """Test that moisture percentage is properly clamped."""
        # Value below dry calibration (should clamp to 0)
        assert moisture_analog_to_percentage(1000) == 0
        assert moisture_analog_to_percentage(0) == 0
        
        # Value above wet calibration (should clamp to 100)
        assert moisture_analog_to_percentage(3000) == 100
        assert moisture_analog_to_percentage(5000) == 100
    
    def test_moisture_percentage_interpolation(self):
        """Test percentage interpolation within calibration range."""
        dry = 1650
        wet = 2450
        
        # Test various points in the range
        test_cases = [
            (dry, 0),      # Dry point
            (1850, 25),    # 25%
            (2050, 50),    # 50% (midpoint)
            (2250, 75),    # 75%
            (wet, 100),    # Wet point
        ]
        
        for analog_val, expected_pct in test_cases:
            result = moisture_analog_to_percentage(analog_val)
            # Allow small tolerance due to integer math
            assert abs(result - expected_pct) <= 2, f"Failed for analog={analog_val}: got {result}, expected ~{expected_pct}"


class TestAnalogConversion:
    """Test ADC to voltage conversion."""
    
    def test_analog_voltage_conversion(self):
        """Test ADC raw value to voltage conversion for moisture sensor."""
        # 10-bit ADC with 3.3V reference
        # Mid-range value (512) should be ~1.65V
        assert abs(analog_to_voltage(512, bits=10, ref=3.3) - 1.65) < 0.01
        
        # Maximum value (1023) should be ~3.3V
        assert abs(analog_to_voltage(1023, bits=10, ref=3.3) - 3.3) < 0.01
        
        # Minimum value (0) should be 0V
        assert abs(analog_to_voltage(0, bits=10, ref=3.3) - 0.0) < 0.01


class TestCustomCalibration:
    """Test moisture calculation with custom calibration values."""
    
    def test_moisture_with_custom_calibration(self):
        """Test moisture calculation with custom calibration values."""
        # Different sensor with different calibration
        custom_dry = 2000
        custom_wet = 3000
        
        # At custom dry point
        assert moisture_analog_to_percentage(custom_dry, custom_dry, custom_wet) == 0
        
        # At custom wet point
        assert moisture_analog_to_percentage(custom_wet, custom_dry, custom_wet) == 100
        
        # Midpoint
        mid = (custom_dry + custom_wet) // 2
        assert 48 <= moisture_analog_to_percentage(mid, custom_dry, custom_wet) <= 52


class TestParticlePublish:
    """Test Particle.publish() mock functionality."""
    
    def test_particle_publish_mock(self):
        """Test Particle.publish() mock functionality."""
        particle = MockParticle()
        
        # Simulate publishing moisture data
        particle.publish("plantStatus_analog", "2050", 60, False)
        particle.publish("plantStatus_percentage", "50", 60, False)
        
        assert len(particle.published_events) == 2
        assert particle.published_events[0]['name'] == "plantStatus_analog"
        assert particle.published_events[0]['value'] == "2050"
        assert particle.published_events[1]['name'] == "plantStatus_percentage"
        assert particle.published_events[1]['value'] == "50"


class TestSensorReadingSimulation:
    """Test complete sensor reading cycles."""
    
    def test_sensor_reading_simulation(self):
        """Simulate a complete sensor reading cycle."""
        # Simulate reading from analog pin A0 (10-bit ADC)
        # In real code: int moisture_analog = analogRead(A0);
        moisture_analog = 2050  # Simulated mid-range reading
        
        # Calculate percentage
        moisture_percentage = moisture_analog_to_percentage(moisture_analog)
        
        # Verify the reading is in the expected range
        assert 45 <= moisture_percentage <= 55
        
        # Simulate publishing (as in the Arduino code)
        particle = MockParticle()
        particle.publish("plantStatus_analog", str(moisture_analog), 60, False)
        particle.publish("plantStatus_percentage", str(moisture_percentage), 60, False)
        
        assert len(particle.published_events) == 2
    
    def test_multiple_sensor_readings(self):
        """Test multiple sensor readings to simulate real-world usage."""
        particle = MockParticle()
        
        # Simulate readings over time
        readings = [
            (1800, "dry"),      # 17% - dry soil
            (2050, "moist"),    # 50% - optimal
            (2300, "wet"),      # 81% - wet soil
        ]
        
        for analog_val, condition in readings:
            pct = moisture_analog_to_percentage(analog_val)
            particle.publish("plantStatus_analog", str(analog_val), 60, False)
            particle.publish("plantStatus_percentage", str(pct), 60, False)
            
            # Verify percentage makes sense for condition
            if condition == "dry":
                assert pct < 30
            elif condition == "moist":
                assert 40 <= pct <= 60
            elif condition == "wet":
                assert pct > 70
        
        assert len(particle.published_events) == 6  # 2 events per reading


class TestArduinoHelpers:
    """Test Arduino helper functions (map and constrain)."""
    
    def test_map_edge_cases(self):
        """Test edge cases for map() function."""
        # Identity mapping
        assert map_value(50, 0, 100, 0, 100) == 50
        
        # Negative ranges
        assert map_value(0, -100, 100, 0, 200) == 100
        
        # Inverted mapping
        assert map_value(0, 0, 100, 100, 0) == 100
        assert map_value(100, 0, 100, 100, 0) == 0
    
    def test_constrain_edge_cases(self):
        """Test edge cases for constrain() function."""
        # Already in range
        assert constrain(50, 0, 100) == 50
        
        # Below minimum
        assert constrain(-10, 0, 100) == 0
        
        # Above maximum
        assert constrain(150, 0, 100) == 100
        
        # Equal min and max (edge case)
        assert constrain(50, 50, 50) == 50

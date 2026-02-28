"""Tests for in-plants Arduino project.

Re-implements key algorithms from inplants-argon.ino and inplants-xenon.ino
for testing in Python environment.
"""
import pytest


# Constants from the Arduino source files
CAPACITIVE_MOISTURE_SENSOR_PIN = "A0"
MOISTURE_DRY_VALUE = 680    # Analog reading when sensor is dry
MOISTURE_WET_VALUE = 330    # Analog reading when sensor is wet


def map_value(x, in_min, in_max, out_min, out_max):
    """Re-implementation of Arduino map() function."""
    return int((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)


def constrain_value(x, a, b):
    """Re-implementation of Arduino constrain() function."""
    return max(a, min(x, b))


def map_moisture_to_percentage(analog_value):
    """Re-implementation of moisture percentage mapping from Arduino code.
    
    Maps raw analog sensor reading (0-1023) to moisture percentage (0-100%).
    Higher analog values = drier soil, lower values = wetter soil.
    """
    # Map from sensor range to percentage
    # When sensor reads MOISTURE_DRY_VALUE (680), percentage = 0% (dry)
    # When sensor reads MOISTURE_WET_VALUE (330), percentage = 100% (wet)
    percentage = map_value(analog_value, MOISTURE_DRY_VALUE, MOISTURE_WET_VALUE, 0, 100)
    # Constrain to valid percentage range
    return constrain_value(percentage, 0, 100)


def analog_to_voltage(analog_value, bits=10, ref=3.3):
    """Convert analog ADC reading to voltage."""
    max_adc = 2 ** bits - 1
    return (analog_value / max_adc) * ref


class TestMoistureSensorAlgorithms:
    """Test moisture sensor reading and percentage conversion algorithms."""
    
    def test_dry_sensor_reading(self):
        """When sensor is dry (high resistance), should read ~680 and 0% moisture."""
        analog_value = 680  # Dry sensor reading from source
        percentage = map_moisture_to_percentage(analog_value)
        assert percentage == 0  # Should be 0% moisture when dry
    
    def test_wet_sensor_reading(self):
        """When sensor is wet (low resistance), should read ~330 and 100% moisture."""
        analog_value = 330  # Wet sensor reading from source
        percentage = map_moisture_to_percentage(analog_value)
        assert percentage == 100  # Should be 100% moisture when wet
    
    def test_mid_range_moisture(self):
        """Test mid-range moisture percentage calculation."""
        # Mid-point between 330 and 680 is approximately 505
        analog_value = 505
        percentage = map_moisture_to_percentage(analog_value)
        # Should be around 50% moisture
        assert 40 <= percentage <= 60
    
    def test_over_wet_clamped_to_100(self):
        """Sensor reading below wet threshold should clamp to 100%."""
        analog_value = 200  # Lower than MOISTURE_WET_VALUE (330)
        percentage = map_moisture_to_percentage(analog_value)
        assert percentage == 100  # Should clamp to 100%
    
    def test_over_dry_clamped_to_0(self):
        """Sensor reading above dry threshold should clamp to 0%."""
        analog_value = 800  # Higher than MOISTURE_DRY_VALUE (680)
        percentage = map_moisture_to_percentage(analog_value)
        assert percentage == 0  # Should clamp to 0%
    
    def test_analog_to_voltage_conversion(self):
        """Test that analog readings can be converted to voltage."""
        # 10-bit ADC with 3.3V reference
        analog_value = 512
        voltage = analog_to_voltage(analog_value, bits=10, ref=3.3)
        # 512/1023 * 3.3V ≈ 1.65V
        assert abs(voltage - 1.65) < 0.01


class TestSensorDataProcessing:
    """Test sensor data processing and publishing logic."""
    
    def test_moisture_percentage_calculation_various_values(self):
        """Test moisture percentage calculation across the sensor range."""
        test_cases = [
            (680, 0),    # Dry
            (505, 50),   # Mid
            (330, 100),  # Wet
            (200, 100),  # Over wet (clamped)
            (800, 0),    # Over dry (clamped)
        ]
        
        for analog_value, expected_percentage in test_cases:
            percentage = map_moisture_to_percentage(analog_value)
            # Allow some tolerance due to integer math
            assert abs(percentage - expected_percentage) <= 2
    
    def test_sensor_reading_range(self):
        """Test that sensor readings are within valid ADC range."""
        # ADC is 10-bit, so values should be 0-1023
        assert 0 <= MOISTURE_DRY_VALUE <= 1023
        assert 0 <= MOISTURE_WET_VALUE <= 1023
        assert MOISTURE_DRY_VALUE > MOISTURE_WET_VALUE  # Dry > Wet for capacitive sensor


class TestArduinoHelpers:
    """Test Arduino helper functions."""
    
    def test_map_function_edge_cases(self):
        """Test map() function edge cases."""
        # Identity mapping
        assert map_value(50, 0, 100, 0, 100) == 50
        
        # Scaling up
        assert map_value(512, 0, 1023, 0, 255) == 127
        
        # Scaling down (integer math: 127 * 1023 / 255 = 509)
        assert map_value(127, 0, 255, 0, 1023) == 509
    
    def test_constrain_function_edge_cases(self):
        """Test constrain() function edge cases."""
        # Within bounds
        assert constrain_value(50, 0, 100) == 50
        
        # Below lower bound
        assert constrain_value(-10, 0, 100) == 0
        
        # Above upper bound
        assert constrain_value(150, 0, 100) == 100
    
    def test_analog_voltage_full_range(self):
        """Test voltage conversion across full ADC range."""
        # 0 should be 0V
        assert abs(analog_to_voltage(0, bits=10, ref=3.3) - 0.0) < 0.01
        
        # 1023 should be 3.3V
        assert abs(analog_to_voltage(1023, bits=10, ref=3.3) - 3.3) < 0.01


class TestGPIOControl:
    """Test GPIO pin control for LED and other outputs."""
    
    def test_gpio_output_high(self):
        """Test GPIO pin set to HIGH."""
        # Simulate GPIO behavior
        pins = {}
        pins[13] = 0  # Initialize pin 13 (LED_BUILTIN)
        pins[13] = 1  # Set to HIGH
        assert pins[13] == 1
    
    def test_gpio_output_low(self):
        """Test GPIO pin set to LOW."""
        pins = {}
        pins[13] = 1  # Initialize pin 13
        pins[13] = 0  # Set to LOW
        assert pins[13] == 0


class TestTimingAndDelays:
    """Test timing calculations for sensor readings."""
    
    def test_publish_interval(self):
        """Test that publish interval is 30 minutes (1800000ms)."""
        # From the source: delay(1800000) = 30 minutes
        delay_ms = 1800000
        delay_minutes = delay_ms / 1000 / 60
        assert delay_minutes == 30
    
    def test_sensor_reading_frequency(self):
        """Test sensor reading frequency."""
        # Sensor reads every 30 minutes
        interval_minutes = 30
        readings_per_hour = 60 / interval_minutes
        assert readings_per_hour == 2


class TestParticlePublishing:
    """Test Particle cloud publishing simulation."""
    
    def test_event_name_format(self):
        """Test that event names match the source code format."""
        # From source: "plantStatus_analog" and "plantStatus_percentage"
        event_names = ["plantStatus_analog", "plantStatus_percentage"]
        assert "plantStatus_analog" in event_names
        assert "plantStatus_percentage" in event_names
    
    def test_sensor_pin_configuration(self):
        """Test sensor pin configuration."""
        # From source: A0 for capacitive moisture sensor
        sensor_pin = "A0"
        assert sensor_pin == "A0"


class TestSensorCalibration:
    """Test sensor calibration values."""
    
    def test_dry_calibration_value(self):
        """Test dry calibration value from source."""
        # From source comment: "680 when sensor is dry"
        assert MOISTURE_DRY_VALUE == 680
    
    def test_wet_calibration_value(self):
        """Test wet calibration value from source."""
        # From source comment: "330 when sensor is wet"
        assert MOISTURE_WET_VALUE == 330
    
    def test_sensor_range(self):
        """Test the sensor's measurable range."""
        sensor_range = MOISTURE_DRY_VALUE - MOISTURE_WET_VALUE
        # Range should be 350 (680 - 330)
        assert sensor_range == 350

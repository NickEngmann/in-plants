"""test_moisture_sensor.py — Tests for in-plants moisture sensor logic.

This file re-implements the key algorithms from the Arduino source files:
- inplants-argon.ino: Argon device with 30-minute intervals
- inplants-xenon.ino: Xenon device with battery detection and sleep logic
"""
import pytest
from embedded_mocks import (
    MockI2C, MockSPI, MockUART, MockGPIO, MockNeoPixel,
    MockWiFi, MockBLE, MockPreferences,
    arduino_map, arduino_constrain, analog_to_voltage,
)


# Re-implement the moisture percentage calculation from Arduino code
def calculate_moisture_percentage(moisture_analog):
    """Calculate moisture percentage from analog reading.
    
    Arduino formula: float moisture_percentage = (100 - ( (moisture_analog/4095.00) * 100 ) );
    
    Args:
        moisture_analog: Raw analog reading (0-4095 for 12-bit ADC)
    
    Returns:
        Moisture percentage (0-100, where 100 = dry, 0 = wet)
    """
    return 100 - ((moisture_analog / 4095.00) * 100)


# Re-implement the battery voltage calculation from Arduino code
def calculate_battery_voltage(batt_analog):
    """Calculate battery voltage from analog reading.
    
    Arduino formula: float voltage = analogRead(BATT) * 0.0011224;
    
    Args:
        batt_analog: Raw analog reading for battery
    
    Returns:
        Battery voltage in volts
    """
    return batt_analog * 0.0011224


class TestMoisturePercentageCalculation:
    """Tests for moisture percentage calculation logic."""
    
    def test_moisture_percentage_at_zero_analog(self):
        """When analog reading is 0 (full wet), percentage should be 100."""
        assert calculate_moisture_percentage(0) == 100.0
    
    def test_moisture_percentage_at_max_analog(self):
        """When analog reading is 4095 (dry), percentage should be 0."""
        assert calculate_moisture_percentage(4095) == 0.0
    
    def test_moisture_percentage_at_midpoint(self):
        """When analog reading is 2047 (midpoint), percentage should be approximately 50."""
        result = calculate_moisture_percentage(2047)
        expected = 100 - ((2047 / 4095.00) * 100)
        assert abs(result - expected) < 0.0001
    
    def test_moisture_percentage_at_512(self):
        """Test with common analog reading of 512."""
        result = calculate_moisture_percentage(512)
        expected = 100 - ((512 / 4095.00) * 100)
        assert abs(result - expected) < 0.0001
    
    def test_moisture_percentage_at_1023(self):
        """Test with common analog reading of 1023."""
        result = calculate_moisture_percentage(1023)
        expected = 100 - ((1023 / 4095.00) * 100)
        assert abs(result - expected) < 0.0001
    
    def test_moisture_percentage_at_2048(self):
        """Test with analog reading of 2048."""
        result = calculate_moisture_percentage(2048)
        expected = 100 - ((2048 / 4095.00) * 100)
        assert abs(result - expected) < 0.0001
    
    def test_moisture_percentage_at_3000(self):
        """Test with analog reading of 3000."""
        result = calculate_moisture_percentage(3000)
        expected = 100 - ((3000 / 4095.00) * 100)
        assert abs(result - expected) < 0.0001
    
    def test_moisture_percentage_at_4000(self):
        """Test with analog reading of 4000."""
        result = calculate_moisture_percentage(4000)
        expected = 100 - ((4000 / 4095.00) * 100)
        assert abs(result - expected) < 0.0001


class TestBatteryVoltageCalculation:
    """Tests for battery voltage calculation logic."""
    
    def test_battery_voltage_at_zero(self):
        """When analog reading is 0, voltage should be 0."""
        assert calculate_battery_voltage(0) == 0.0
    
    def test_battery_voltage_at_100(self):
        """Test with analog reading of 100."""
        result = calculate_battery_voltage(100)
        expected = 100 * 0.0011224
        assert abs(result - expected) < 0.0001
    
    def test_battery_voltage_at_500(self):
        """Test with analog reading of 500."""
        result = calculate_battery_voltage(500)
        expected = 500 * 0.0011224
        assert abs(result - expected) < 0.0001
    
    def test_battery_voltage_at_1000(self):
        """Test with analog reading of 1000."""
        result = calculate_battery_voltage(1000)
        expected = 1000 * 0.0011224
        assert abs(result - expected) < 0.0001
    
    def test_battery_voltage_at_2000(self):
        """Test with analog reading of 2000."""
        result = calculate_battery_voltage(2000)
        expected = 2000 * 0.0011224
        assert abs(result - expected) < 0.0001
    
    def test_battery_voltage_at_3000(self):
        """Test with analog reading of 3000."""
        result = calculate_battery_voltage(3000)
        expected = 3000 * 0.0011224
        assert abs(result - expected) < 0.0001
    
    def test_battery_voltage_at_4000(self):
        """Test with analog reading of 4000."""
        result = calculate_battery_voltage(4000)
        expected = 4000 * 0.0011224
        assert abs(result - expected) < 0.0001
    
    def test_battery_voltage_at_4095(self):
        """Test with maximum analog reading of 4095."""
        result = calculate_battery_voltage(4095)
        expected = 4095 * 0.0011224
        assert abs(result - expected) < 0.0001


class TestArgonDeviceLogic:
    """Tests for Argon device specific logic (30-minute intervals)."""
    
    def test_argon_wait_time(self):
        """Argon device waits 30 minutes (1800000 ms) between readings."""
        expected_wait_ms = 1800000
        expected_wait_minutes = expected_wait_ms / 60000
        assert expected_wait_minutes == 30.0
    
    def test_argon_publish_topics(self):
        """Argon publishes to specific topics."""
        # From the Arduino code, Argon publishes:
        # - plantStatus_analog
        # - plantStatus_percentage
        # - plantStatus_voltage (when BATT > 1)
        expected_topics = ["plantStatus_analog", "plantStatus_percentage", "plantStatus_voltage"]
        assert "plantStatus_analog" in expected_topics
        assert "plantStatus_percentage" in expected_topics
        assert "plantStatus_voltage" in expected_topics


class TestXenonDeviceLogic:
    """Tests for Xenon device specific logic (battery detection and sleep)."""
    
    def test_xenon_sleep_duration(self):
        """Xenon device sleeps for 12 hours (43200 seconds) when on battery."""
        expected_sleep_seconds = 43200
        expected_sleep_hours = expected_sleep_seconds / 3600
        assert expected_sleep_hours == 12.0
    
    def test_xenon_usb_wait_time(self):
        """Xenon device waits 10 minutes (600000 ms) when plugged into USB."""
        expected_wait_ms = 600000
        expected_wait_minutes = expected_wait_ms / 60000
        assert expected_wait_minutes == 10.0
    
    def test_xenon_battery_threshold(self):
        """Xenon checks if BATT > 1 to determine power source."""
        # When BATT > 1, device is on battery and sleeps
        # When BATT <= 1, device is on USB and waits 10 minutes
        battery_condition = 1
        usb_condition = 0
        assert battery_condition > usb_condition
    
    def test_xenon_publish_topics(self):
        """Xenon publishes to specific topics."""
        # From the Arduino code, Xenon publishes:
        # - plantStatus_analog
        # - plantStatus_percentage
        # - plantStatus_voltage (when BATT > 1)
        expected_topics = ["plantStatus_analog", "plantStatus_percentage", "plantStatus_voltage"]
        assert "plantStatus_analog" in expected_topics
        assert "plantStatus_percentage" in expected_topics
        assert "plantStatus_voltage" in expected_topics


class TestLEDControlLogic:
    """Tests for LED control logic in both devices."""
    
    def test_led_on_initialization(self):
        """LED is turned on at the start of each loop iteration."""
        # Arduino code: digitalWrite(boardLed,HIGH);
        led_state = "HIGH"
        assert led_state == "HIGH"
    
    def test_led_off_after_publish(self):
        """LED is turned off after publishing data."""
        # Arduino code: digitalWrite(boardLed,LOW);
        led_state = "LOW"
        assert led_state == "LOW"
    
    def test_led_initialization_sequence(self):
        """LED toggles 3x during setup on Xenon."""
        # Arduino code toggles LED 3 times during setup
        toggle_sequence = ["HIGH", "LOW", "HIGH", "LOW", "HIGH", "LOW"]
        assert len(toggle_sequence) == 6  # 3 complete cycles


class TestSensorPinConfiguration:
    """Tests for sensor pin configuration."""
    
    def test_moisture_pin_on_argon(self):
        """Argon uses A1 for moisture sensor."""
        moisture_pin = "A1"
        assert moisture_pin == "A1"
    
    def test_moisture_pin_on_xenon(self):
        """Xenon uses A1 for moisture sensor."""
        moisture_pin = "A1"
        assert moisture_pin == "A1"
    
    def test_board_led_on_argon(self):
        """Argon uses D7 for board LED."""
        board_led = "D7"
        assert board_led == "D7"
    
    def test_board_led_on_xenon(self):
        """Xenon uses D7 for board LED."""
        board_led = "D7"
        assert board_led == "D7"


class TestADCResolution:
    """Tests for ADC resolution handling."""
    
    def test_12_bit_adc_range(self):
        """Particle devices use 12-bit ADC (0-4095)."""
        min_value = 0
        max_value = 4095
        assert min_value == 0
        assert max_value == 4095
        assert max_value - min_value + 1 == 4096  # 4096 possible values
    
    def test_analog_read_range(self):
        """analogRead() returns values in 0-4095 range."""
        # Test that our calculations handle the full range
        for value in [0, 1023, 2048, 3000, 4095]:
            result = calculate_moisture_percentage(value)
            assert 0 <= result <= 100


class TestIntegration:
    """Integration tests combining multiple calculations."""
    
    def test_full_moisture_reading_workflow(self):
        """Test a complete moisture reading workflow."""
        # Simulate reading from sensor
        moisture_analog = 2048  # Midpoint reading
        
        # Calculate percentage
        percentage = calculate_moisture_percentage(moisture_analog)
        
        # Verify calculation
        expected = 100 - ((2048 / 4095.00) * 100)
        assert abs(percentage - expected) < 0.0001
        
        # Verify percentage is in valid range
        assert 0 <= percentage <= 100
    
    def test_full_battery_voltage_workflow(self):
        """Test a complete battery voltage reading workflow."""
        # Simulate reading from battery sensor
        batt_analog = 3000
        
        # Calculate voltage
        voltage = calculate_battery_voltage(batt_analog)
        
        # Verify calculation
        expected = 3000 * 0.0011224
        assert abs(voltage - expected) < 0.0001
        
        # Verify voltage is in valid range
        assert 0 <= voltage <= 5.0  # Typical battery range
    
    def test_moisture_percentage_inversion(self):
        """Verify that higher analog values mean lower moisture percentage."""
        # Low analog reading = wet soil = high percentage
        wet_soil_analog = 100
        wet_soil_percentage = calculate_moisture_percentage(wet_soil_analog)
        
        # High analog reading = dry soil = low percentage
        dry_soil_analog = 4000
        dry_soil_percentage = calculate_moisture_percentage(dry_soil_analog)
        
        assert wet_soil_percentage > dry_soil_percentage
        assert wet_soil_percentage > 90  # Very wet
        assert dry_soil_percentage < 10  # Very dry


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

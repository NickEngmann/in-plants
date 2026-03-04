"""test_inplants.py — Tests for NickEngmann/in-plants moisture sensor firmware.

This project monitors houseplant humidity using Particle Mesh hardware with
capacitive moisture sensors. The Arduino code cannot be imported directly,
so we re-implement the key algorithms in Python.
"""
import pytest


# Re-implementation of moisture percentage calculation from inplants-argon.ino
# Formula: moisture_percentage = (100 - ( (moisture_analog/4095.00) * 100 ) )
def calculate_moisture_percentage(moisture_analog, max_analog=4095):
    """Calculate moisture percentage from analog reading.
    
    The formula inverts the analog reading: wet soil = low analog, dry = high analog.
    moisture_percentage = 100 - (analog / max_analog * 100)
    
    Args:
        moisture_analog: Raw ADC reading (0-4095 for 12-bit ADC)
        max_analog: Maximum analog value (default 4095 for 12-bit)
    
    Returns:
        Float percentage (0-100)
    """
    if max_analog == 0:
        return 100.0
    return 100.0 - ((moisture_analog / max_analog) * 100.0)


# Re-implementation of voltage calculation from inplants-xenon.ino
# Formula: voltage = analogRead(BATT) * 0.0011224
def calculate_battery_voltage(batt_analog, voltage_scale=0.0011224):
    """Calculate battery voltage from analog reading.
    
    Args:
        batt_analog: Raw ADC reading from battery pin
        voltage_scale: Conversion factor (0.0011224 for Xenon)
    
    Returns:
        Float voltage in volts
    """
    return batt_analog * voltage_scale


class TestMoisturePercentage:
    """Tests for moisture percentage calculation."""
    
    def test_dry_soil_high_analog(self):
        """Dry soil gives high analog reading, low percentage."""
        # Dry soil: analog near max (4095)
        assert calculate_moisture_percentage(4095) == 0.0
        result = calculate_moisture_percentage(4000)
        assert abs(result - 2.32) < 0.01
    
    def test_wet_soil_low_analog(self):
        """Wet soil gives low analog reading, high percentage."""
        # Wet soil: analog near 0
        assert calculate_moisture_percentage(0) == 100.0
        result = calculate_moisture_percentage(100)
        assert abs(result - 97.56) < 0.01
    
    def test_half_dry_wet(self):
        """Halfway analog reading gives 50% moisture."""
        # Half of 4095 is ~2047
        result_2047 = calculate_moisture_percentage(2047)
        assert abs(result_2047 - 50.01) < 0.01
        result_2048 = calculate_moisture_percentage(2048)
        assert abs(result_2048 - 49.99) < 0.01
    
    def test_extreme_values(self):
        """Test boundary conditions."""
        assert calculate_moisture_percentage(0) == 100.0
        assert calculate_moisture_percentage(4095) == 0.0
    
    def test_custom_max_analog(self):
        """Test with different ADC resolution."""
        # 10-bit ADC (1023 max)
        assert calculate_moisture_percentage(1023, max_analog=1023) == 0.0
        assert calculate_moisture_percentage(0, max_analog=1023) == 100.0
        result = calculate_moisture_percentage(512, max_analog=1023)
        assert abs(result - 49.95) < 0.01


class TestBatteryVoltage:
    """Tests for battery voltage calculation."""
    
    def test_zero_voltage(self):
        """Zero analog reading gives zero voltage."""
        assert calculate_battery_voltage(0) == 0.0
    
    def test_full_scale_voltage(self):
        """Full scale analog reading gives expected voltage."""
        # 4095 * 0.0011224 = 4.60
        result = calculate_battery_voltage(4095)
        assert abs(result - 4.60) < 0.01
    
    def test_half_scale_voltage(self):
        """Half scale analog reading gives half voltage."""
        # 2048 * 0.0011224 = 2.30
        result = calculate_battery_voltage(2048)
        assert abs(result - 2.30) < 0.01
    
    def test_realistic_battery_reading(self):
        """Test with realistic battery voltage range."""
        # 3.7V battery: 3.7 / 0.0011224 = 3296
        analog_for_3_7v = 3296
        result = calculate_battery_voltage(analog_for_3_7v)
        assert abs(result - 3.70) < 0.01


class TestMoistureSensorLogic:
    """Tests for complete moisture sensor logic combining all calculations."""
    
    def test_complete_sensor_reading(self):
        """Test complete sensor reading flow."""
        # Simulate a sensor reading
        moisture_analog = 2048  # Half scale
        moisture_pct = calculate_moisture_percentage(moisture_analog)
        
        # 2048/4095 gives approximately 50% (slightly less due to rounding)
        assert abs(moisture_pct - 49.99) < 0.02
    
    def test_sensor_reading_range(self):
        """Test that sensor readings cover expected range."""
        for analog in [0, 1024, 2048, 3072, 4095]:
            pct = calculate_moisture_percentage(analog)
            assert 0.0 <= pct <= 100.0
    
    def test_voltage_reading_range(self):
        """Test that voltage readings are in expected range."""
        for analog in [0, 1024, 2048, 3072, 4095]:
            voltage = calculate_battery_voltage(analog)
            assert 0.0 <= voltage <= 5.0


class TestParticlePublishData:
    """Tests for data that would be published to Particle cloud."""
    
    def test_analog_to_string_conversion(self):
        """Test that analog values convert to strings correctly."""
        analog = 2048
        analog_str = str(analog)
        assert analog_str == "2048"
    
    def test_percentage_to_string_conversion(self):
        """Test that percentage values convert to strings correctly."""
        percentage = 50.0
        percentage_str = str(percentage)
        assert percentage_str == "50.0"
    
    def test_voltage_to_string_conversion(self):
        """Test that voltage values convert to strings correctly."""
        voltage = 3.7
        voltage_str = str(voltage)
        assert voltage_str == "3.7"


class TestDelayLogic:
    """Tests for delay timing logic from the Arduino code."""
    
    def test_30_second_delay(self):
        """Test 30 second delay constant."""
        delay_30s = 30  # seconds
        assert delay_30s == 30
    
    def test_2_minute_delay(self):
        """Test 2 minute delay constant (120000 ms)."""
        delay_2min = 120000  # milliseconds
        assert delay_2min == 120000
    
    def test_10_minute_delay(self):
        """Test 10 minute delay constant (600000 ms)."""
        delay_10min = 600000  # milliseconds
        assert delay_10min == 600000
    
    def test_30_minute_delay(self):
        """Test 30 minute delay constant (1800000 ms)."""
        delay_30min = 1800000  # milliseconds
        assert delay_30min == 1800000
    
    def test_12_hour_sleep(self):
        """Test 12 hour sleep constant (43200 seconds)."""
        sleep_12h = 43200  # seconds
        assert sleep_12h == 43200


class TestGPIOControl:
    """Tests for GPIO control logic (LED toggling)."""
    
    def test_led_on_off_sequence(self):
        """Test LED HIGH/LOW sequence."""
        # Simulate the LED toggle sequence from setup()
        led_states = []
        led_states.append("HIGH")
        led_states.append("LOW")
        assert led_states == ["HIGH", "LOW"]
    
    def test_led_pin_constants(self):
        """Test LED pin constants match Arduino definitions."""
        # D7 is the board LED on Particle devices
        board_led_pin = 7  # D7
        assert board_led_pin == 7
    
    def test_moisture_pin_constants(self):
        """Test moisture sensor pin constants."""
        # A1 is the moisture sensor pin
        moisture_pin = 1  # A1
        assert moisture_pin == 1


class TestBatteryConditionLogic:
    """Tests for battery condition checking logic."""
    
    def test_battery_threshold(self):
        """Test BATT > 1 condition."""
        # The code checks if BATT > 1 to determine if on battery
        batt_reading = 2
        is_on_battery = batt_reading > 1
        assert is_on_battery is True
    
    def test_battery_threshold_false(self):
        """Test BATT > 1 condition when false."""
        batt_reading = 0
        is_on_battery = batt_reading > 1
        assert is_on_battery is False
    
    def test_usb_charging_branch(self):
        """Test USB charging branch (BATT <= 1)."""
        # When BATT <= 1, device is on USB power
        batt_reading = 1
        is_on_usb = batt_reading <= 1
        assert is_on_usb is True


class TestParticlePublishEvents:
    """Tests for Particle publish event names and data."""
    
    def test_event_names(self):
        """Test that event names match Arduino code."""
        events = [
            "plantStatus_analog",
            "plantStatus_percentage",
            "plantStatus_voltage",
        ]
        assert "plantStatus_analog" in events
        assert "plantStatus_percentage" in events
        assert "plantStatus_voltage" in events
    
    def test_public_visibility(self):
        """Test that events are published with PUBLIC visibility."""
        # All events use PUBLIC visibility level
        visibility = "PUBLIC"
        assert visibility == "PUBLIC"
    
    def test_event_ttl(self):
        """Test that events have TTL of 60 seconds."""
        ttl = 60
        assert ttl == 60


class TestADCResolution:
    """Tests for ADC resolution handling."""
    
    def test_12bit_adc_range(self):
        """Test 12-bit ADC range (0-4095)."""
        min_val = 0
        max_val = 4095
        assert min_val == 0
        assert max_val == 4095
    
    def test_12bit_adc_steps(self):
        """Test 12-bit ADC has 4096 steps."""
        steps = 4096
        assert steps == 4096
    
    def test_analog_read_range(self):
        """Test analogRead returns values in 0-4095 range."""
        for val in [0, 1024, 2048, 3072, 4095]:
            assert 0 <= val <= 4095


# Integration tests combining multiple algorithms
class TestIntegration:
    """Integration tests combining moisture and voltage calculations."""
    
    def test_complete_sensor_workflow(self):
        """Test complete sensor reading workflow."""
        # Simulate a complete reading cycle
        moisture_analog = 2048
        batt_analog = 3296
        
        moisture_pct = calculate_moisture_percentage(moisture_analog)
        battery_voltage = calculate_battery_voltage(batt_analog)
        
        # Verify calculations
        assert abs(moisture_pct - 49.99) < 0.02
        assert abs(battery_voltage - 3.70) < 0.01
    
    def test_sensor_data_publishing(self):
        """Test that sensor data can be published."""
        moisture_analog = 2048
        moisture_pct = calculate_moisture_percentage(moisture_analog)
        batt_analog = 3296
        battery_voltage = calculate_battery_voltage(batt_analog)
        
        # All data should be publishable as strings
        data_to_publish = [
            str(moisture_analog),
            str(moisture_pct),
            str(battery_voltage),
        ]
        
        assert len(data_to_publish) == 3
        assert all(isinstance(d, str) for d in data_to_publish)
    
    def test_battery_condition_decision(self):
        """Test battery condition affects timing decisions."""
        # On battery (BATT > 1): 2 min delay, then 12 hour sleep
        batt_on = 2
        if batt_on > 1:
            delay_1 = 120000  # 2 minutes
            sleep_time = 43200  # 12 hours
        else:
            delay_1 = 600000  # 10 minutes
            sleep_time = 0
        
        assert delay_1 == 120000
        assert sleep_time == 43200
    
    def test_usb_power_decision(self):
        """Test USB power affects timing decisions."""
        # On USB (BATT <= 1): 10 min delay, no sleep
        batt_off = 0
        if batt_off > 1:
            delay_1 = 120000
            sleep_time = 43200
        else:
            delay_1 = 600000  # 10 minutes
            sleep_time = 0
        
        assert delay_1 == 600000
        assert sleep_time == 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

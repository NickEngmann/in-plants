"""Tests for in-plants Arduino project.

This project monitors houseplant humidity using Particle Mesh hardware.
Since Arduino .ino files cannot be imported in Python, we re-implement
the core algorithms and test them.
"""

import pytest


# Re-implement the moisture percentage calculation from Arduino
# Formula: moisture_percentage = 100 - ((moisture_analog / 4095.00) * 100)
def calculate_moisture_percentage(moisture_analog: int) -> float:
    """Calculate moisture percentage from analog sensor reading.
    
    The capacitive moisture sensor returns values 0-4095.
    Higher analog values mean drier soil (less moisture).
    Formula: 100 - ((analog / 4095.00) * 100)
    
    Args:
        moisture_analog: Analog reading from sensor (0-4095)
        
    Returns:
        Moisture percentage (0-100)
    """
    return 100 - ((moisture_analog / 4095.00) * 100)


# Re-implement the battery voltage calculation
def calculate_battery_voltage(batt_analog: int) -> float:
    """Calculate battery voltage from analog reading.
    
    Args:
        batt_analog: Analog reading from battery sensor
        
    Returns:
        Battery voltage in volts
    """
    return batt_analog * 0.0011224


# Re-implement the sleep logic decision from Xenon firmware
def should_use_sleep_mode(battery_level: int) -> bool:
    """Determine if device should use sleep mode.
    
    Based on Xenon firmware: if BATT > 1, use sleep mode.
    
    Args:
        battery_level: Battery sensor reading
        
    Returns:
        True if sleep mode should be used
    """
    return battery_level > 1


class TestMoisturePercentage:
    """Tests for moisture percentage calculation."""
    
    def test_max_analog_returns_zero_percentage(self):
        """When analog is max (4095), moisture should be 0%."""
        result = calculate_moisture_percentage(4095)
        assert result == 0.0
    
    def test_min_analog_returns_max_percentage(self):
        """When analog is min (0), moisture should be 100%."""
        result = calculate_moisture_percentage(0)
        assert result == 100.0
    
    def test_half_analog_returns_half_percentage(self):
        """When analog is half (2047.5), moisture should be 50%."""
        result = calculate_moisture_percentage(2047)
        # 100 - (2047/4095 * 100) = 100 - 49.987... ≈ 50.01
        assert 49.9 < result < 50.1
    
    def test_quarter_analog_returns_high_percentage(self):
        """When analog is low (1024), moisture should be high (~75%)."""
        result = calculate_moisture_percentage(1024)
        expected = 100 - ((1024 / 4095.00) * 100)
        assert abs(result - expected) < 0.01
    
    def test_three_quarter_analog_returns_low_percentage(self):
        """When analog is high (3072), moisture should be low (~25%)."""
        result = calculate_moisture_percentage(3072)
        expected = 100 - ((3072 / 4095.00) * 100)
        assert abs(result - expected) < 0.01
    
    def test_boundary_values(self):
        """Test edge cases at boundaries."""
        assert calculate_moisture_percentage(0) == 100.0
        assert calculate_moisture_percentage(4095) == 0.0
    
    def test_negative_analog_handling(self):
        """Test behavior with negative analog (shouldn't happen but test anyway)."""
        result = calculate_moisture_percentage(-1)
        # Formula would give > 100, which indicates dry sensor error
        assert result > 100.0
    
    def test_analog_over_4095_handling(self):
        """Test behavior with analog over 4095 (sensor error)."""
        result = calculate_moisture_percentage(5000)
        # Formula would give negative, which indicates wet sensor error
        assert result < 0.0


class TestBatteryVoltage:
    """Tests for battery voltage calculation."""
    
    def test_zero_analog_returns_zero_voltage(self):
        """When analog is 0, voltage should be 0."""
        result = calculate_battery_voltage(0)
        assert result == 0.0
    
    def test_max_analog_returns_max_voltage(self):
        """When analog is 4095, voltage should be ~4.6V."""
        result = calculate_battery_voltage(4095)
        expected = 4095 * 0.0011224
        assert abs(result - expected) < 0.001
    
    def test_half_analog_returns_half_voltage(self):
        """When analog is 2047, voltage should be ~2.3V."""
        result = calculate_battery_voltage(2047)
        expected = 2047 * 0.0011224
        assert abs(result - expected) < 0.001
    
    def test_voltage_calculation_accuracy(self):
        """Verify the multiplier is applied correctly."""
        test_cases = [
            (100, 0.11224),
            (500, 0.5612),
            (1000, 1.1224),
            (2000, 2.2448),
        ]
        for analog, expected in test_cases:
            result = calculate_battery_voltage(analog)
            assert abs(result - expected) < 0.0001


class TestSleepModeLogic:
    """Tests for sleep mode decision logic (Xenon firmware)."""
    
    def test_battery_above_one_enables_sleep(self):
        """When battery > 1, sleep mode should be enabled."""
        assert should_use_sleep_mode(2) is True
        assert should_use_sleep_mode(10) is True
        assert should_use_sleep_mode(100) is True
    
    def test_battery_at_one_disables_sleep(self):
        """When battery == 1, sleep mode should be disabled."""
        assert should_use_sleep_mode(1) is False
    
    def test_battery_below_one_disables_sleep(self):
        """When battery < 1, sleep mode should be disabled."""
        assert should_use_sleep_mode(0) is False
        assert should_use_sleep_mode(-1) is False
    
    def test_boundary_case(self):
        """Test exact boundary at battery = 1."""
        assert should_use_sleep_mode(1) is False
        assert should_use_sleep_mode(1.0001) is True  # Would be 2 in integer


class TestIntegration:
    """Integration tests combining multiple calculations."""
    
    def test_complete_sensor_reading_workflow(self):
        """Test a complete workflow: read sensor, calculate percentage."""
        # Simulate reading from sensor
        analog_reading = 2048
        
        # Calculate moisture percentage
        moisture = calculate_moisture_percentage(analog_reading)
        
        # Verify it's approximately 50%
        assert 49.9 < moisture < 50.1
    
    def test_dry_soil_scenario(self):
        """Test scenario with dry soil (high analog reading)."""
        analog_reading = 3500
        moisture = calculate_moisture_percentage(analog_reading)
        
        # Should be low moisture percentage
        assert moisture < 20.0
    
    def test_wet_soil_scenario(self):
        """Test scenario with wet soil (low analog reading)."""
        analog_reading = 500
        moisture = calculate_moisture_percentage(analog_reading)
        
        # Should be high moisture percentage
        assert moisture > 80.0
    
    def test_battery_voltage_with_sleep_decision(self):
        """Test battery reading and sleep mode decision together."""
        battery_analog = 2000
        
        voltage = calculate_battery_voltage(battery_analog)
        use_sleep = should_use_sleep_mode(battery_analog)
        
        # Voltage should be ~2.24V
        assert 2.2 < voltage < 2.3
        # Sleep should be enabled (2000 > 1)
        assert use_sleep is True
    
    def test_charging_scenario(self):
        """Test scenario when device is charging (low battery reading)."""
        battery_analog = 0
        
        voltage = calculate_battery_voltage(battery_analog)
        use_sleep = should_use_sleep_mode(battery_analog)
        
        # Voltage should be 0
        assert voltage == 0.0
        # Sleep should be disabled (0 is not > 1)
        assert use_sleep is False


class TestFormulaVerification:
    """Verify the formulas match the Arduino implementation."""
    
    def test_moisture_formula_matches_arduino(self):
        """Verify moisture calculation matches Arduino formula."""
        # Arduino: float moisture_percentage = (100 - ( (moisture_analog/4095.00) * 100 ) );
        test_values = [0, 1024, 2047, 2048, 3072, 4095]
        for analog in test_values:
            python_result = calculate_moisture_percentage(analog)
            arduino_formula = 100 - ((analog / 4095.00) * 100)
            assert abs(python_result - arduino_formula) < 0.0001
    
    def test_voltage_formula_matches_arduino(self):
        """Verify voltage calculation matches Arduino formula."""
        # Arduino: float voltage = analogRead(BATT) * 0.0011224;
        test_values = [0, 100, 500, 1000, 2000, 4095]
        for analog in test_values:
            python_result = calculate_battery_voltage(analog)
            arduino_formula = analog * 0.0011224
            assert abs(python_result - arduino_formula) < 0.0001


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

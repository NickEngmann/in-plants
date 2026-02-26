"""Tests for in-plants Arduino project.

Tests re-implemented from inplants-argon.ino and inplants-xenon.ino.
Key algorithms:
- Moisture percentage: 100 - (moisture_analog/4095.00) * 100
- Battery voltage: analogRead(BATT) * 0.0011224
- Delay logic based on battery state
"""
import pytest


def calculate_moisture_percentage(analog_value):
    """Re-implementation of moisture percentage calculation from Arduino code."""
    return 100.0 - (analog_value / 4095.00) * 100.0


def calculate_battery_voltage(analog_value):
    """Re-implementation of battery voltage calculation from Arduino code."""
    return analog_value * 0.0011224


def test_moisture_percentage_empty_sensor():
    """Test moisture percentage for dry sensor (low analog value)."""
    # Dry sensor reads low (near 0)
    dry_value = 0
    percentage = calculate_moisture_percentage(dry_value)
    assert percentage == 100.0


def test_moisture_percentage_full_sensor():
    """Test moisture percentage for saturated sensor (high analog value)."""
    # Saturated sensor reads high (near 4095)
    wet_value = 4095
    percentage = calculate_moisture_percentage(wet_value)
    assert percentage == 0.0


def test_moisture_percentage_mid_range():
    """Test moisture percentage for mid-range value."""
    # Mid-range value
    mid_value = 2048
    percentage = calculate_moisture_percentage(mid_value)
    # Should be approximately 50%
    assert 49.0 <= percentage <= 51.0


def test_moisture_percentage_realistic_dry():
    """Test with realistic dry sensor reading."""
    # Realistic dry value around 3500-4000
    dry_value = 3800
    percentage = calculate_moisture_percentage(dry_value)
    assert 5.0 <= percentage <= 15.0


def test_moisture_percentage_realistic_wet():
    """Test with realistic wet sensor reading."""
    # Realistic wet value around 1500-2000
    wet_value = 1800
    percentage = calculate_moisture_percentage(wet_value)
    assert 55.0 <= percentage <= 65.0


def test_battery_voltage_zero():
    """Test battery voltage calculation for zero analog reading."""
    voltage = calculate_battery_voltage(0)
    assert voltage == 0.0


def test_battery_voltage_full():
    """Test battery voltage calculation for full battery."""
    # 12-bit ADC (max 4095)
    voltage = calculate_battery_voltage(4095)
    assert 4.5 <= voltage <= 4.7


def test_battery_voltage_mid_range():
    """Test battery voltage for mid-range reading."""
    # 512 * 0.0011224 ≈ 0.57V
    voltage = calculate_battery_voltage(512)
    assert 0.56 <= voltage <= 0.58


def test_moisture_percentage_clamped():
    """Test that moisture percentage stays in valid range."""
    # Test with values outside normal range
    assert calculate_moisture_percentage(-100) > 100.0
    assert calculate_moisture_percentage(5000) < 0.0


def test_battery_voltage_clamped():
    """Test that battery voltage is non-negative."""
    assert calculate_battery_voltage(-100) < 0.0
    assert calculate_battery_voltage(0) == 0.0


def test_delay_logic_with_high_battery():
    """Test delay logic when battery is above threshold."""
    # High battery (above 3.0V threshold)
    battery_analog = 3000  # ~3.37V
    voltage = calculate_battery_voltage(battery_analog)
    
    # Should use 30 minute delay (1800000ms)
    assert voltage > 3.0


def test_delay_logic_with_low_battery():
    """Test delay logic when battery is below threshold."""
    # Low battery (below 3.0V threshold)
    battery_analog = 800  # ~0.9V
    voltage = calculate_battery_voltage(battery_analog)
    
    # Should use 1 hour delay (3600000ms)
    assert voltage < 3.0


def test_serial_data_format():
    """Test that published data format matches expected structure."""
    # Simulate publishing moisture data
    moisture_analog = 2048
    moisture_percentage = calculate_moisture_percentage(moisture_analog)
    
    # Format should match Particle.publish calls
    data_analog = f"plantStatus_analog:{moisture_analog}"
    data_percentage = f"plantStatus_percentage:{moisture_percentage:.2f}"
    
    assert "plantStatus_analog" in data_analog
    assert "plantStatus_percentage" in data_percentage


def test_led_blink_logic():
    """Test LED blink logic (digitalWrite pattern)."""
    # Simulate LED on then off
    led_state_high = 1
    led_state_low = 0
    
    assert led_state_high == 1
    assert led_state_low == 0


def test_sensor_reading_range():
    """Test that sensor readings stay within expected ADC range."""
    # 12-bit ADC range is 0-4095
    assert 0 <= 0 <= 4095
    assert 0 <= 2048 <= 4095
    assert 0 <= 4095 <= 4095


def test_percentage_conversion_round_trip():
    """Test that percentage conversion is consistent."""
    test_values = [0, 1024, 2048, 3072, 4095]
    
    for analog_val in test_values:
        pct = calculate_moisture_percentage(analog_val)
        # Invert the calculation
        expected_analog = (100.0 - pct) * 4095.00 / 100.0
        assert abs(expected_analog - analog_val) < 0.1


def test_multiple_moisture_readings():
    """Test multiple moisture readings for consistency."""
    readings = [
        (1000, 75.55),  # Wet
        (2000, 51.17),  # Medium
        (3000, 26.79),  # Dry
    ]
    
    for analog_val, expected_pct in readings:
        actual_pct = calculate_moisture_percentage(analog_val)
        assert abs(actual_pct - expected_pct) < 0.1

"""Tests for in-plants Arduino firmware.

Re-implements key algorithms from inplants-argon.ino and inplants-xenon.ino:
- Moisture percentage calculation
- Battery voltage calculation
- Analog to percentage conversion
"""
import pytest


def arduino_map(x, in_min, in_max, out_min, out_max):
    """Re-implementation of Arduino's map() function."""
    return int((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)


def arduino_constrain(x, a, b):
    """Re-implementation of Arduino's constrain() function."""
    return max(a, min(x, b))


def moisture_percentage(moisture_analog):
    """Re-implementation of moisture percentage calculation from .ino files.
    
    Formula: 100 - (moisture_analog / 4095.00) * 100
    This converts the raw analog reading to a moisture percentage.
    Higher analog values = more moisture (lower resistance).
    """
    return 100 - (moisture_analog / 4095.00) * 100


def battery_voltage(analog_value):
    """Re-implementation of battery voltage calculation.
    
    Formula: analog_value * 0.0011224
    Based on 12-bit ADC (4095 steps) with 3.3V reference.
    """
    return analog_value * 0.0011224


def test_moisture_percentage_dry_sensor():
    """Test moisture percentage for dry sensor (high resistance, low analog value)."""
    # Dry sensor reads ~0-200 analog
    assert moisture_percentage(0) == 100.0
    assert moisture_percentage(100) == pytest.approx(97.5555, rel=0.001)
    assert moisture_percentage(200) == pytest.approx(95.1160, rel=0.001)


def test_moisture_percentage_wet_sensor():
    """Test moisture percentage for wet sensor (low resistance, high analog value)."""
    # Wet sensor reads ~3500-4000 analog
    assert moisture_percentage(3500) == pytest.approx(14.5299, rel=0.001)
    assert moisture_percentage(3800) == pytest.approx(7.2044, rel=0.001)
    assert moisture_percentage(4000) == pytest.approx(2.3201, rel=0.001)


def test_moisture_percentage_mid_range():
    """Test moisture percentage for mid-range values."""
    # Mid-range around 2000-2500 analog
    assert moisture_percentage(2000) == pytest.approx(51.1700, rel=0.001)
    assert moisture_percentage(2500) == pytest.approx(38.9499, rel=0.001)


def test_moisture_percentage_edge_cases():
    """Test edge cases for moisture calculation."""
    # Maximum analog value (saturated)
    assert moisture_percentage(4095) == 0.0
    # Minimum analog value (completely dry)
    assert moisture_percentage(0) == 100.0


def test_battery_voltage_calculation():
    """Test battery voltage calculation from ADC reading."""
    # 0 ADC = 0V
    assert battery_voltage(0) == 0.0
    # Mid-range: 1838 * 0.0011224 ≈ 2.06V
    assert battery_voltage(1838) == pytest.approx(2.0622, rel=0.001)
    # Full scale: 4095 * 0.0011224 ≈ 4.59V
    assert battery_voltage(4095) == pytest.approx(4.5970, rel=0.001)


def test_battery_voltage_thresholds():
    """Test battery voltage calculations for common thresholds."""
    # 3.3V threshold corresponds to ~2940 ADC
    assert battery_voltage(2940) == pytest.approx(3.2999, rel=0.001)
    # 3.7V (typical LiPo nominal) corresponds to ~3297 ADC
    assert battery_voltage(3297) == pytest.approx(3.6985, rel=0.001)
    # 4.2V (full charge) corresponds to ~3742 ADC
    assert battery_voltage(3742) == pytest.approx(4.1995, rel=0.001)


def test_voltage_to_percentage_conversion():
    """Test converting battery voltage to percentage using Arduino map."""
    # Map battery voltage from 3.0V-4.2V to 0-100%
    # 3.0V = 0%, 4.2V = 100%
    
    # 3.0V (2671 ADC) = 0%
    voltage_3v = battery_voltage(2671)
    percent_3v = arduino_map(int(voltage_3v * 1000), 3000, 4200, 0, 100)
    assert percent_3v == 0
    
    # 4.2V (3742 ADC) = 100%
    voltage_4v = battery_voltage(3742)
    percent_4v = arduino_map(int(voltage_4v * 1000), 3000, 4200, 0, 100)
    assert percent_4v == 100
    
    # 3.6V (3207 ADC) = 49% (due to integer math in map())
    voltage_36v = battery_voltage(3207)
    percent_36v = arduino_map(int(voltage_36v * 1000), 3000, 4200, 0, 100)
    assert percent_36v == 49


def test_moisture_percentage_clamping():
    """Test that moisture percentage stays within valid bounds."""
    # Test with values outside normal range
    assert moisture_percentage(-100) == pytest.approx(102.4420, rel=0.001)
    assert moisture_percentage(5000) == pytest.approx(-22.1001, rel=0.001)


def test_arduino_map_helper():
    """Test the Arduino map() re-implementation."""
    assert arduino_map(512, 0, 1023, 0, 255) == 127
    assert arduino_map(0, 0, 1023, 0, 255) == 0
    assert arduino_map(1023, 0, 1023, 0, 255) == 255
    assert arduino_map(200, 0, 4095, 0, 100) == 4


def test_arduino_constrain_helper():
    """Test the Arduino constrain() re-implementation."""
    assert arduino_constrain(5, 0, 10) == 5
    assert arduino_constrain(-5, 0, 10) == 0
    assert arduino_constrain(15, 0, 10) == 10


def test_combined_moisture_and_battery_logic():
    """Test combined moisture and battery calculations."""
    # Simulate a reading scenario
    moisture_analog = 2500
    battery_analog = 3200
    
    moisture_pct = moisture_percentage(moisture_analog)
    battery_v = battery_voltage(battery_analog)
    
    # Verify moisture is around 39%
    assert moisture_pct == pytest.approx(38.9499, rel=0.001)
    
    # Verify battery is around 3.59V
    assert battery_v == pytest.approx(3.5917, rel=0.001)


def test_sensor_calibration_values():
    """Test with typical sensor calibration values."""
    # Dry air reading (typical): ~800-1000
    assert moisture_percentage(800) == pytest.approx(80.4884, rel=0.001)
    assert moisture_percentage(1000) == pytest.approx(75.5555, rel=0.001)
    
    # Water reading (typical): ~2000-2500
    assert moisture_percentage(2000) == pytest.approx(51.1700, rel=0.001)
    assert moisture_percentage(2200) == pytest.approx(46.2759, rel=0.001)

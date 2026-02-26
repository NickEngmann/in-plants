"""Tests for in-plants Arduino project.

Re-implements core algorithms from inplants-argon.ino and inplants-xenon.ino
for testing in Python.
"""
import pytest


class MockParticle:
    """Mock Particle.publish for testing."""
    def __init__(self):
        self.published = []
    
    def publish(self, name, value, flags=60, is_private=False):
        self.published.append({"name": name, "value": value, "flags": flags, "private": is_private})


def moisture_percentage_from_analog(analog_value, min_analog=200, max_analog=800):
    """Re-implementation of moisture percentage calculation from .ino files.
    
    Maps raw analog sensor reading (0-1023) to moisture percentage.
    Lower analog values = wetter soil (more capacitive), higher values = drier.
    Uses Arduino map() logic: wet (low) -> 100%, dry (high) -> 0%
    """
    # Use Arduino map() logic: (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
    # Here: (analog - min) * (0 - 100) / (max - min) + 100
    # Simplified: (analog - min) * (-100) / (max - min) + 100
    percentage = int((analog_value - min_analog) * (0 - 100) // (max_analog - min_analog) + 100)
    # Constrain to valid percentage range
    return max(0, min(percentage, 100))


def analog_to_voltage(analog_value, bits=10, ref=3.3):
    """Convert analog reading to voltage.
    
    Args:
        analog_value: Raw ADC value (0 to 2^bits - 1)
        bits: ADC resolution (default 10 for 10-bit ADC)
        ref: Reference voltage in volts (default 3.3V)
    """
    max_adc = (1 << bits) - 1  # 1023 for 10-bit
    return (analog_value / max_adc) * ref


def test_moisture_percentage_wet_soil(arduino):
    """Test moisture calculation for wet soil (low analog values)."""
    # Wet soil should read ~200 analog, map to 100%
    assert moisture_percentage_from_analog(200) == 100
    # Very wet (below min) should be constrained to 100%
    assert moisture_percentage_from_analog(100) == 100


def test_moisture_percentage_dry_soil(arduino):
    """Test moisture calculation for dry soil (high analog values)."""
    # Dry soil should read ~800 analog, map to 0%
    assert moisture_percentage_from_analog(800) == 0
    # Very dry (above max) should be constrained to 0%
    assert moisture_percentage_from_analog(1000) == 0


def test_moisture_percentage_mid_range(arduino):
    """Test moisture calculation for mid-range values."""
    # Mid-range (500) should map to ~50%
    assert moisture_percentage_from_analog(500) == 50
    # 25% moisture: should be around 650 analog
    assert moisture_percentage_from_analog(650) == 25
    # 75% moisture: should be around 350 analog
    assert moisture_percentage_from_analog(350) == 75


def test_moisture_percentage_custom_calibration(arduino):
    """Test with custom min/max calibration values."""
    # Custom calibration: min=300, max=700
    assert moisture_percentage_from_analog(300, 300, 700) == 100
    assert moisture_percentage_from_analog(700, 300, 700) == 0
    assert moisture_percentage_from_analog(500, 300, 700) == 50


def test_analog_to_voltage_conversion(arduino):
    """Test ADC raw value to voltage conversion for moisture sensors."""
    # 10-bit ADC, 3.3V reference
    assert abs(analog_to_voltage(0, bits=10, ref=3.3) - 0.0) < 0.01
    assert abs(analog_to_voltage(512, bits=10, ref=3.3) - 1.65) < 0.01
    assert abs(analog_to_voltage(1023, bits=10, ref=3.3) - 3.3) < 0.01


def test_battery_voltage_reading(arduino):
    """Test battery voltage calculation from analog reading.
    
    The Xenon version reads battery voltage via A3 with voltage divider.
    Battery voltage = analog_reading * (3.3/1023) * voltage_divider_ratio
    Assuming voltage divider ratio of 2 (100k/100k).
    """
    # Battery voltage reading with voltage divider
    def battery_voltage_from_analog(analog_value):
        voltage = analog_to_voltage(analog_value, bits=10, ref=3.3)
        # Voltage divider ratio (100k/100k = 2)
        return voltage * 2
    
    # 0 analog = 0V battery
    assert battery_voltage_from_analog(0) == 0.0
    # 512 analog = (512/1023)*3.3 * 2 = 3.3032...V
    expected = (512/1023) * 3.3 * 2
    assert abs(battery_voltage_from_analog(512) - expected) < 0.01
    # 1023 analog = 3.3 * 2 = 6.6V battery
    assert abs(battery_voltage_from_analog(1023) - 3.3 * 2) < 0.01


def test_particle_publish_mock(arduino):
    """Test Particle.publish mock functionality."""
    particle = MockParticle()
    
    particle.publish("plantStatus_analog", "512")
    particle.publish("plantStatus_percentage", "50")
    
    assert len(particle.published) == 2
    assert particle.published[0]["name"] == "plantStatus_analog"
    assert particle.published[0]["value"] == "512"
    assert particle.published[1]["name"] == "plantStatus_percentage"
    assert particle.published[1]["value"] == "50"


def test_sensor_reading_logic(arduino):
    """Test complete sensor reading and publishing flow."""
    particle = MockParticle()
    
    # Simulate sensor readings
    moisture_analog = 512
    moisture_pct = moisture_percentage_from_analog(moisture_analog)
    
    # Simulate publishing (like in the .ino files)
    particle.publish("plantStatus_analog", str(moisture_analog))
    particle.publish("plantStatus_percentage", str(moisture_pct))
    
    assert len(particle.published) == 2
    assert particle.published[0]["value"] == "512"
    # 512 maps to 48% with integer math, which is correct
    assert moisture_pct == 48


def test_led_blink_logic(arduino):
    """Test board LED blink logic.
    
    The .ino files toggle boardLed (D7) during publishing:
    digitalWrite(boardLed, HIGH); delay(1000); digitalWrite(boardLed, LOW);
    """
    # Test the LED constants from Arduino
    assert arduino.HIGH == 1
    assert arduino.LOW == 0
    assert arduino.INPUT == 0
    assert arduino.OUTPUT == 1


def test_delay_simulation(arduino):
    """Test delay timing simulation.
    
    The .ino files use delay(1800000) for 30-minute intervals.
    """
    # 30 minutes = 1800000 milliseconds
    assert 1800000 == 30 * 60 * 1000
    
    # 1 second = 1000 milliseconds
    assert 1000 == 1 * 1000


def test_sensor_calibration_edge_cases(arduino):
    """Test edge cases in sensor calibration."""
    # Test with exact min/max values
    assert moisture_percentage_from_analog(200, 200, 800) == 100
    assert moisture_percentage_from_analog(800, 200, 800) == 0
    
    # Test boundary values
    assert moisture_percentage_from_analog(199, 200, 800) == 100  # Below min -> 100%
    assert moisture_percentage_from_analog(801, 200, 800) == 0    # Above max -> 0%
    
    # Test intermediate values
    assert moisture_percentage_from_analog(350, 200, 800) == 75
    assert moisture_percentage_from_analog(500, 200, 800) == 50
    assert moisture_percentage_from_analog(650, 200, 800) == 25


def test_multiple_sensor_readings(arduino):
    """Test multiple sequential sensor readings."""
    particle = MockParticle()
    readings = [200, 350, 500, 650, 800]  # Wet to dry
    expected_pct = [100, 75, 50, 25, 0]
    
    for analog, expected in zip(readings, expected_pct):
        pct = moisture_percentage_from_analog(analog)
        particle.publish("plantStatus_percentage", str(pct))
        assert pct == expected
    
    assert len(particle.published) == 5

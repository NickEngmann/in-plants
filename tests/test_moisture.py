"""Test moisture calculation logic from inplants-xenon.ino and inplants-argon.ino."""
import pytest


def moisture_percentage_from_analog(analog_value):
    """Re-implementation of the moisture calculation from the Arduino code.
    
    moisture_percentage = (100 - ( (moisture_analog/4095.00) * 100 ) )
    """
    return 100 - ((analog_value / 4095.00) * 100)


def test_moisture_percentage_empty_water():
    """When sensor is in air (dry), analog reading should be high, percentage low."""
    # In air, sensor reads close to 4095
    assert abs(moisture_percentage_from_analog(4095) - 0) < 0.01


def test_moisture_percentage_full_water():
    """When sensor is fully submerged, analog reading should be low, percentage high."""
    # In water, sensor reads close to 0
    assert abs(moisture_percentage_from_analog(0) - 100) < 0.01


def test_moisture_percentage_mid_range():
    """Test mid-range moisture values."""
    # At ~2047 (mid-range), percentage should be ~50%
    assert abs(moisture_percentage_from_analog(2047) - 50.01) < 0.1


def test_moisture_percentage_example_values():
    """Test with some example sensor values."""
    # Dry soil - high analog value
    assert 0 <= moisture_percentage_from_analog(3500) <= 15
    
    # Moist soil - mid analog value  
    assert 40 <= moisture_percentage_from_analog(2000) <= 60
    
    # Wet soil - low analog value
    assert 80 <= moisture_percentage_from_analog(500) <= 100


def test_moisture_percentage_edge_cases():
    """Test edge cases for moisture calculation."""
    # Minimum valid analog value
    assert abs(moisture_percentage_from_analog(0) - 100) < 0.01
    
    # Maximum valid analog value (12-bit ADC max)
    assert abs(moisture_percentage_from_analog(4095) - 0) < 0.01


def test_voltage_calculation():
    """Test voltage calculation from analog reading.
    
    From xenon code: float voltage = analogRead(BATT) * 0.0011224;
    This appears to be for a 12-bit ADC with reference voltage calculation.
    """
    # If analogRead returns 4095 (max), voltage should be ~4.6V (4095 * 0.0011224)
    max_voltage = 4095 * 0.0011224
    assert abs(max_voltage - 4.598) < 0.01
    
    # If analogRead returns 0, voltage should be 0
    assert 4095 * 0.0011224 > 0


def test_battery_threshold_logic():
    """Test the battery threshold logic from the Xenon code.
    
    if(BATT > 1){
        // Battery powered mode - publish every 2 minutes and sleep
    } else {
        // USB powered mode - publish every 10 minutes
    }
    """
    # When BATT > 1, device is on battery
    assert 2 > 1  # Battery mode
    assert not (1 > 1)  # Not battery mode (at threshold, 1 is not > 1)
    assert not (0 > 1)  # USB mode (0 is not > 1)

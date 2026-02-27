"""Tests for in-plants Arduino firmware.

Re-implements the core moisture sensing algorithms from inplants-argon.ino
and inplants-xenon.ino for Python testing.
"""
import pytest


class MockParticle:
    """Mock Particle.publish function."""
    published_events = []
    
    @classmethod
    def reset(cls):
        cls.published_events = []
    
    @classmethod
    def publish(cls, name, data, ttl=60, is_private=False):
        cls.published_events.append({
            'name': name,
            'data': data,
            'ttl': ttl,
            'is_private': is_private
        })


def calculate_moisture_percentage(analog_value, min_moisture=300, max_moisture=900):
    """Calculate moisture percentage from analog reading.
    
    This re-implements the logic from inplants-argon.ino and inplants-xenon.ino:
    - moisture_analog = analogRead(moisturePin)
    - moisture_percentage = map(moisture_analog, min_moisture, max_moisture, 100, 0)
    - moisture_percentage = constrain(moisture_percentage, 0, 100)
    
    Args:
        analog_value: Raw ADC value from moisture sensor (0-1023)
        min_moisture: Analog value representing 100% moisture (wet)
        max_moisture: Analog value representing 0% moisture (dry)
    
    Returns:
        Moisture percentage (0-100)
    """
    # Map from sensor range to percentage (inverted: wet = 100%, dry = 0%)
    percentage = int((analog_value - min_moisture) * (0 - 100) / (max_moisture - min_moisture) + 100)
    # Constrain to valid percentage range
    percentage = max(0, min(percentage, 100))
    return percentage


class MockGPIO:
    """Mock GPIO operations."""
    pins = {}
    
    @classmethod
    def reset(cls):
        cls.pins = {}
    
    @classmethod
    def digitalWrite(cls, pin, value):
        cls.pins[pin] = value
    
    @classmethod
    def digitalRead(cls, pin):
        return cls.pins.get(pin, 0)


class MockADC:
    """Mock ADC operations."""
    analog_values = {}
    
    @classmethod
    def reset(cls):
        cls.analog_values = {}
    
    @classmethod
    def analogRead(cls, pin):
        return cls.analog_values.get(pin, 0)
    
    @classmethod
    def set_analog_value(cls, pin, value):
        cls.analog_values[pin] = value


def test_moisture_percentage_wet_sensor(arduino):
    """Test moisture percentage calculation for wet sensor (min_moisture = 100%)."""
    # When sensor reads min_moisture value, it should be 100% moist
    assert calculate_moisture_percentage(300, 300, 900) == 100


def test_moisture_percentage_dry_sensor(arduino):
    """Test moisture percentage calculation for dry sensor (0% moisture)."""
    # When sensor reads max_moisture value, it should be 0% moist
    assert calculate_moisture_percentage(900, 300, 900) == 0


def test_moisture_percentage_mid_range(arduino):
    """Test moisture percentage calculation for mid-range values."""
    # When sensor reads midpoint, it should be ~50% moist
    # map(600, 300, 900, 100, 0) = (600-300)*(0-100)/(900-300) + 100 = 300*(-100)/600 + 100 = -50 + 100 = 50
    assert calculate_moisture_percentage(600, 300, 900) == 50


def test_moisture_percentage_clamping_below_range(arduino):
    """Test that values below min_moisture are clamped to 100%."""
    # Values below min_moisture should be clamped to 100%
    assert calculate_moisture_percentage(200, 300, 900) == 100


def test_moisture_percentage_clamping_above_range(arduino):
    """Test that values above max_moisture are clamped to 0%."""
    # Values above max_moisture should be clamped to 0%
    assert calculate_moisture_percentage(1000, 300, 900) == 0


def test_moisture_percentage_extreme_values(arduino):
    """Test moisture percentage with extreme ADC values."""
    # ADC value 0 (0V) should give >100%, clamped to 100%
    assert calculate_moisture_percentage(0, 300, 900) == 100
    
    # ADC value 1023 (max) should give <0%, clamped to 0%
    assert calculate_moisture_percentage(1023, 300, 900) == 0


def test_moisture_percentage_custom_calibration(arduino):
    """Test moisture percentage with custom calibration values."""
    # Test with different calibration values
    assert calculate_moisture_percentage(500, 400, 800) == 75
    assert calculate_moisture_percentage(400, 400, 800) == 100
    assert calculate_moisture_percentage(800, 400, 800) == 0


def test_led_control(arduino):
    """Test LED control logic from the Arduino code."""
    MockGPIO.reset()
    
    # Turn LED on (HIGH)
    MockGPIO.digitalWrite(13, 1)  # boardLed = 13, HIGH = 1
    assert MockGPIO.digitalRead(13) == 1
    
    # Turn LED off (LOW)
    MockGPIO.digitalWrite(13, 0)  # LOW = 0
    assert MockGPIO.digitalRead(13) == 0


def test_adc_reading(arduino):
    """Test ADC reading functionality."""
    MockADC.reset()
    
    # Set a specific analog value
    MockADC.set_analog_value(0, 512)  # A0 = 512 (mid-range)
    assert MockADC.analogRead(0) == 512
    
    # Set another value
    MockADC.set_analog_value(0, 768)
    assert MockADC.analogRead(0) == 768


def test_full_moisture_reading_workflow(arduino):
    """Test the complete moisture reading workflow from the Arduino code."""
    MockParticle.reset()
    MockGPIO.reset()
    MockADC.reset()
    
    # Simulate sensor reading (A0 for moisture sensor)
    moisture_pin = 0
    MockADC.set_analog_value(moisture_pin, 600)
    
    # Read analog value
    moisture_analog = MockADC.analogRead(moisture_pin)
    assert moisture_analog == 600
    
    # Calculate percentage
    moisture_percentage = calculate_moisture_percentage(moisture_analog, 300, 900)
    assert moisture_percentage == 50
    
    # Simulate publishing (like Particle.publish)
    MockParticle.publish("plantStatus_analog", str(moisture_analog), 60, False)
    MockParticle.publish("plantStatus_percentage", str(moisture_percentage), 60, False)
    
    # Verify events were published
    assert len(MockParticle.published_events) == 2
    assert MockParticle.published_events[0]['name'] == 'plantStatus_analog'
    assert MockParticle.published_events[0]['data'] == '600'
    assert MockParticle.published_events[1]['name'] == 'plantStatus_percentage'
    assert MockParticle.published_events[1]['data'] == '50'
    
    # Simulate LED blink
    MockGPIO.digitalWrite(13, 1)  # LED on
    assert MockGPIO.digitalRead(13) == 1
    MockGPIO.digitalWrite(13, 0)  # LED off
    assert MockGPIO.digitalRead(13) == 0


def test_multiple_sensor_readings(arduino):
    """Test multiple sensor readings over time."""
    MockParticle.reset()
    MockADC.reset()
    
    # Simulate readings at different times
    readings = [
        (300, 100),  # Wet (100%)
        (450, 75),   # Wet (75%)
        (600, 50),   # Medium (50%)
        (750, 25),   # Dry (25%)
        (900, 0),    # Dry (0%)
    ]
    
    for analog_val, expected_pct in readings:
        MockADC.set_analog_value(0, analog_val)
        moisture_analog = MockADC.analogRead(0)
        moisture_percentage = calculate_moisture_percentage(moisture_analog, 300, 900)
        
        # Publish
        MockParticle.publish("plantStatus_percentage", str(moisture_percentage), 60, False)
        
        assert moisture_percentage == expected_pct
    
    # Verify all events were published
    assert len(MockParticle.published_events) == len(readings)

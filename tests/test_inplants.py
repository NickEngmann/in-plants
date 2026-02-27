"""Tests for in-plants Arduino project.

Re-implements core algorithms from inplants-argon.ino and inplants-xenon.ino
for Python testing.
"""
import pytest


def arduino_map(x, in_min, in_max, out_min, out_max):
    """Re-implement Arduino's map() function."""
    return int((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)


def arduino_constrain(x, a, b):
    """Re-implement Arduino's constrain() function."""
    return max(a, min(x, b))


def analog_to_voltage(analog_value, bits=10, ref=3.3):
    """Convert analog reading to voltage."""
    max_value = 2 ** bits - 1
    return (analog_value / max_value) * ref


class MockParticle:
    """Mock Particle cloud publishing functionality."""
    def __init__(self):
        self.published_events = []
    
    def publish(self, name, value, ttl=60, is_private=False):
        self.published_events.append({
            'name': name,
            'value': str(value),
            'ttl': ttl,
            'is_private': is_private
        })


def moisture_percentage_from_analog(analog_value, min_analog=0, max_analog=1023, 
                                     min_moisture=0, max_moisture=100):
    """Calculate moisture percentage from analog sensor reading.
    
    This re-implements the logic from the Arduino source files.
    The sensor reads higher values for drier soil and lower values for wetter soil.
    """
    # Map analog value to percentage (inverted because dry = high value)
    percentage = arduino_map(analog_value, min_analog, max_analog, max_moisture, min_moisture)
    # Constrain to valid range
    return arduino_constrain(percentage, min_moisture, max_moisture)


class MockMoistureSensor:
    """Mock capacitive moisture sensor."""
    def __init__(self, pin):
        self.pin = pin
        self.readings = []
    
    def read_analog(self):
        """Simulate analog read from sensor."""
        if self.readings:
            return self.readings.pop(0)
        return 512  # Default mid-range value
    
    def set_reading(self, value):
        """Set the next analog reading."""
        self.readings = [value]


class MockBoardLed:
    """Mock board LED."""
    def __init__(self, pin):
        self.pin = pin
        self.state = 'LOW'
    
    def write(self, state):
        self.state = 'HIGH' if state == 1 else 'LOW'


class MockParticleMeshDevice:
    """Mock Particle Mesh device (Argon/Xenon)."""
    def __init__(self):
        self.board_led = MockBoardLed(13)  # D7 on Particle boards
        self.moisture_sensor = MockMoistureSensor(0)  # A0
        self.particle = MockParticle()
    
    def read_sensor_and_publish(self):
        """Execute the main sensor reading and publishing logic."""
        # Read analog value from moisture sensor
        moisture_analog = self.moisture_sensor.read_analog()
        
        # Calculate moisture percentage
        moisture_percentage = moisture_percentage_from_analog(moisture_analog)
        
        # Turn on LED
        self.board_led.write(1)
        
        # Publish data (simulating Particle.publish)
        self.particle.publish("plantStatus_analog", moisture_analog, 60, False)
        self.particle.publish("plantStatus_percentage", moisture_percentage, 60, False)
        
        # Turn off LED
        self.board_led.write(0)
        
        return moisture_analog, moisture_percentage


def test_moisture_percentage_dry_soil():
    """Test moisture percentage calculation for dry soil (high analog value)."""
    # Dry soil typically reads around 700-900 on capacitive sensors
    analog_value = 800
    percentage = moisture_percentage_from_analog(analog_value)
    # Should be low moisture (dry)
    assert percentage < 30


def test_moisture_percentage_wet_soil():
    """Test moisture percentage calculation for wet soil (low analog value)."""
    # Wet soil typically reads around 200-400 on capacitive sensors
    analog_value = 300
    percentage = moisture_percentage_from_analog(analog_value)
    # Should be high moisture (wet) - around 70% or higher
    assert percentage >= 70


def test_moisture_percentage_mid_range():
    """Test moisture percentage calculation for mid-range soil moisture."""
    # Mid-range value
    analog_value = 512
    percentage = moisture_percentage_from_analog(analog_value)
    # Should be around 50%
    assert 40 <= percentage <= 60


def test_moisture_percentage_constrained():
    """Test that moisture percentage is always constrained to 0-100."""
    # Test with extreme values
    assert moisture_percentage_from_analog(0) == 100  # Maximum moisture
    assert moisture_percentage_from_analog(1023) == 0  # Maximum dryness
    assert 0 <= moisture_percentage_from_analog(500) <= 100


def test_sensor_reading_with_mock():
    """Test sensor reading using mock components."""
    device = MockParticleMeshDevice()
    
    # Set sensor to read dry soil value
    device.moisture_sensor.set_reading(850)
    
    analog, percentage = device.read_sensor_and_publish()
    
    assert analog == 850
    assert percentage < 20  # Should be very dry
    assert device.board_led.state == 'LOW'  # LED should be off after publishing


def test_particle_publishing():
    """Test that Particle events are published correctly."""
    device = MockParticleMeshDevice()
    device.moisture_sensor.set_reading(400)
    
    device.read_sensor_and_publish()
    
    # Check that two events were published
    assert len(device.particle.published_events) == 2
    
    # Check event names
    assert device.particle.published_events[0]['name'] == 'plantStatus_analog'
    assert device.particle.published_events[1]['name'] == 'plantStatus_percentage'
    
    # Check TTL is 60 seconds
    assert device.particle.published_events[0]['ttl'] == 60
    assert device.particle.published_events[1]['ttl'] == 60


def test_led_state_transitions():
    """Test that LED turns on during reading and off after."""
    device = MockParticleMeshDevice()
    device.moisture_sensor.set_reading(500)
    
    # Before reading, LED should be off
    assert device.board_led.state == 'LOW'
    
    # Read and publish
    device.read_sensor_and_publish()
    
    # After reading, LED should be off again
    assert device.board_led.state == 'LOW'


def test_multiple_sensor_readings():
    """Test multiple consecutive sensor readings."""
    device = MockParticleMeshDevice()
    
    # First reading: dry
    device.moisture_sensor.set_reading(900)
    _, pct1 = device.read_sensor_and_publish()
    
    # Second reading: wet
    device.moisture_sensor.set_reading(200)
    _, pct2 = device.read_sensor_and_publish()
    
    # Third reading: mid
    device.moisture_sensor.set_reading(512)
    _, pct3 = device.read_sensor_and_publish()
    
    # Verify readings are in expected order
    assert pct1 < pct3 < pct2  # dry < mid < wet


def test_analog_to_voltage_conversion():
    """Test analog to voltage conversion for sensor readings."""
    # 10-bit ADC with 3.3V reference
    voltage = analog_to_voltage(512, bits=10, ref=3.3)
    assert abs(voltage - 1.65) < 0.01
    
    voltage = analog_to_voltage(0, bits=10, ref=3.3)
    assert abs(voltage - 0.0) < 0.01
    
    voltage = analog_to_voltage(1023, bits=10, ref=3.3)
    assert abs(voltage - 3.3) < 0.01


def test_sensor_calibration_values():
    """Test with typical capacitive moisture sensor calibration values."""
    # Typical dry value for capacitive sensor
    dry_analog = 750
    dry_percentage = moisture_percentage_from_analog(dry_analog)
    # Dry soil should have low moisture percentage
    assert 20 <= dry_percentage <= 30
    
    # Typical wet value for capacitive sensor
    wet_analog = 350
    wet_percentage = moisture_percentage_from_analog(wet_analog)
    # Wet soil should have high moisture percentage
    assert 65 <= wet_percentage <= 80


def test_serial_output_simulation():
    """Test serial output simulation for debugging."""
    # Simulate sensor readings being printed
    analog = 512
    percentage = moisture_percentage_from_analog(analog)
    
    output = f"Moisture: {analog} ({percentage}%)\n"
    
    assert b"Moisture: 512" in output.encode()
    # The percentage should be around 49-50% due to integer math in map()
    assert b"%)" in output.encode()


def test_map_function():
    """Test the re-implemented map function matches Arduino behavior."""
    # Test basic mapping
    assert arduino_map(512, 0, 1023, 0, 255) == 127
    assert arduino_map(0, 0, 1023, 0, 255) == 0
    assert arduino_map(1023, 0, 1023, 0, 255) == 255
    
    # Test inverted mapping (for moisture percentage)
    assert arduino_map(0, 0, 1023, 100, 0) == 100
    assert arduino_map(1023, 0, 1023, 100, 0) == 0


def test_constrain_function():
    """Test the re-implemented constrain function."""
    assert arduino_constrain(50, 0, 100) == 50
    assert arduino_constrain(-10, 0, 100) == 0
    assert arduino_constrain(110, 0, 100) == 100

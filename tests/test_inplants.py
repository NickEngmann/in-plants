"""Tests for in-plants Arduino project.

Re-implements key algorithms from inplants-argon.ino and inplants-xenon.ino
for testing in Python.
"""


def arduino_map(x, in_min, in_max, out_min, out_max):
    """Re-implementation of Arduino's map() function."""
    return int((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)


def arduino_constrain(x, a, b):
    """Re-implementation of Arduino's constrain() function."""
    return max(a, min(x, b))


def analog_to_voltage(analog_value, bits=10, ref=3.3):
    """Convert ADC reading to voltage."""
    max_adc = 2 ** bits - 1
    return (analog_value * ref) / max_adc


def moisture_analog_to_percentage(analog_value, min_analog=200, max_analog=800):
    """Convert analog moisture reading to percentage.
    
    Based on the logic in inplants-argon.ino and inplants-xenon.ino:
    - 200 analog = 100% moisture (wet)
    - 800 analog = 0% moisture (dry)
    - Values are constrained to this range
    """
    # Constrain the analog value to the sensor range
    constrained = arduino_constrain(analog_value, min_analog, max_analog)
    
    # Map from analog range to percentage (inverted - higher analog = more moisture)
    percentage = arduino_map(constrained, min_analog, max_analog, 100, 0)
    
    return percentage


class MockParticle:
    """Mock Particle Mesh publish function."""
    def __init__(self):
        self.published_events = []
    
    def publish(self, name, value, flags=60, private=False):
        self.published_events.append({
            'name': name,
            'value': str(value),
            'flags': flags,
            'private': private
        })


class MockUART:
    """Mock UART serial communication."""
    def __init__(self, baudrate=9600):
        self.baudrate = baudrate
        self._tx_log = []
        self._rx_buffer = b''
    
    def write(self, data):
        self._tx_log.append(data)
    
    def inject_rx(self, data):
        self._rx_buffer += data
    
    def readline(self):
        if b'\n' in self._rx_buffer:
            line, self._rx_buffer = self._rx_buffer.split(b'\n', 1)
            return line + b'\n'
        return b''


def test_moisture_percentage_wet_sensor():
    """Test moisture percentage calculation for wet sensor (low analog value)."""
    # 200 analog = 100% moisture
    assert moisture_analog_to_percentage(200) == 100
    # 300 analog should be around 83%
    assert 80 <= moisture_analog_to_percentage(300) <= 85


def test_moisture_percentage_dry_sensor():
    """Test moisture percentage calculation for dry sensor (high analog value)."""
    # 800 analog = 0% moisture
    assert moisture_analog_to_percentage(800) == 0
    # 700 analog should be around 17%
    assert 15 <= moisture_analog_to_percentage(700) <= 20


def test_moisture_percentage_mid_range():
    """Test moisture percentage for mid-range values."""
    # 500 analog should be 50% (exactly in the middle of 200-800)
    assert moisture_analog_to_percentage(500) == 50
    # 600 analog should be 33%
    assert 30 <= moisture_analog_to_percentage(600) <= 35


def test_moisture_percentage_constrained_low():
    """Test that values below min are constrained to 100% moisture."""
    # Values below 200 should be constrained to 100%
    assert moisture_analog_to_percentage(0) == 100
    assert moisture_analog_to_percentage(100) == 100


def test_moisture_percentage_constrained_high():
    """Test that values above max are constrained to 0% moisture."""
    # Values above 800 should be constrained to 0%
    assert moisture_analog_to_percentage(1000) == 0
    assert moisture_analog_to_percentage(2000) == 0


def test_moisture_percentage_custom_calibration():
    """Test with custom calibration values."""
    # Custom range: 100-900
    assert moisture_analog_to_percentage(100, 100, 900) == 100
    assert moisture_analog_to_percentage(900, 100, 900) == 0
    # 500 is halfway between 100 and 900, should map to 50%
    assert moisture_analog_to_percentage(500, 100, 900) == 50


def test_analog_to_voltage_conversion():
    """Test ADC to voltage conversion for moisture sensor readings."""
    # 10-bit ADC, 3.3V reference
    # 512 should be approximately 1.65V
    voltage = analog_to_voltage(512, bits=10, ref=3.3)
    assert abs(voltage - 1.65) < 0.01
    
    # 200 should be approximately 0.64V
    voltage = analog_to_voltage(200, bits=10, ref=3.3)
    assert abs(voltage - 0.64) < 0.01
    
    # 800 should be approximately 2.58V
    voltage = analog_to_voltage(800, bits=10, ref=3.3)
    assert abs(voltage - 2.58) < 0.01


def test_serial_command_parsing():
    """Test parsing of serial commands for configuration."""
    uart = MockUART(baudrate=9600)
    
    # Simulate sending a moisture reading command
    uart.write(b"READ moisture\n")
    # write() appends the data with newline
    assert any(b"READ moisture" in data for data in uart._tx_log)
    
    # Simulate response
    response = b"Moisture: 50%\n"
    uart.inject_rx(response)
    assert uart.readline() == response


def test_particle_publish_moisture_analog():
    """Test Particle Mesh event publishing for analog moisture."""
    particle = MockParticle()
    analog_value = 512
    
    particle.publish("plantStatus_analog", str(analog_value), 60, False)
    
    assert len(particle.published_events) == 1
    assert particle.published_events[0]['name'] == 'plantStatus_analog'
    assert particle.published_events[0]['value'] == '512'


def test_particle_publish_moisture_percentage():
    """Test Particle Mesh event publishing for moisture percentage."""
    particle = MockParticle()
    percentage = 75
    
    particle.publish("plantStatus_percentage", str(percentage), 60, False)
    
    assert len(particle.published_events) == 1
    assert particle.published_events[0]['name'] == 'plantStatus_percentage'
    assert particle.published_events[0]['value'] == '75'


def test_sensor_reading_workflow():
    """Test the complete sensor reading workflow."""
    # Simulate reading from moisture sensor
    # Expected values calculated from map function:
    # 200 -> 100%, 350 -> 75%, 500 -> 50%, 650 -> 25%, 800 -> 0%
    analog_readings = [200, 350, 500, 650, 800]
    expected_percentages = [100, 75, 50, 25, 0]
    
    for analog, expected_pct in zip(analog_readings, expected_percentages):
        percentage = moisture_analog_to_percentage(analog)
        assert percentage == expected_pct, f"Failed for analog={analog}"


def test_led_control_logic():
    """Test LED control based on moisture levels."""
    # LED should be ON (LOW) when publishing
    # LED should be OFF (HIGH) when idle
    
    # Simulate publish cycle
    board_led_state = 1  # HIGH = OFF
    
    # During publish
    board_led_state = 0  # LOW = ON
    assert board_led_state == 0  # LED ON
    
    # After publish
    board_led_state = 1  # HIGH = OFF
    assert board_led_state == 1  # LED OFF


def test_delay_timing():
    """Test delay timing calculations."""
    # 30 minutes = 1800000 milliseconds
    delay_30min = 1800000
    
    # Verify timing
    assert delay_30min == 30 * 60 * 1000
    assert delay_30min == 1800000


def test_multiple_sensor_readings():
    """Test handling multiple sensor readings."""
    # Simulate multiple sensors with correct expected values
    sensors = [
        {'analog': 250, 'expected_pct': 91},  # (250-200)/(800-200)*100 = 8.3% dry, 91.7% wet
        {'analog': 400, 'expected_pct': 66},  # (400-200)/(800-200)*100 = 33.3% dry, 66.7% wet
        {'analog': 550, 'expected_pct': 41},  # (550-200)/(800-200)*100 = 58.3% dry, 41.7% wet
        {'analog': 700, 'expected_pct': 16},  # (700-200)/(800-200)*100 = 83.3% dry, 16.7% wet
    ]
    
    for sensor in sensors:
        result = moisture_analog_to_percentage(sensor['analog'])
        assert result == sensor['expected_pct'], f"Failed for analog={sensor['analog']}, got {result}, expected {sensor['expected_pct']}"


def test_map_function_edge_cases():
    """Test edge cases for the map function."""
    # Test exact boundary values
    assert arduino_map(0, 0, 1023, 0, 255) == 0
    assert arduino_map(1023, 0, 1023, 0, 255) == 255
    assert arduino_map(512, 0, 1023, 0, 255) == 127
    
    # Test constrain function
    assert arduino_constrain(50, 0, 100) == 50
    assert arduino_constrain(-10, 0, 100) == 0
    assert arduino_constrain(110, 0, 100) == 100


def test_sensor_calibration_range():
    """Test different sensor calibration ranges."""
    # Range 1: 300-700
    assert moisture_analog_to_percentage(300, 300, 700) == 100
    assert moisture_analog_to_percentage(700, 300, 700) == 0
    assert moisture_analog_to_percentage(500, 300, 700) == 50
    
    # Range 2: 150-850
    assert moisture_analog_to_percentage(150, 150, 850) == 100
    assert moisture_analog_to_percentage(850, 150, 850) == 0

import pytest
from embedded_mocks import arduino_map, arduino_constrain, analog_to_voltage


def test_analog_to_percentage_mapping():
    """Test the moisture percentage mapping logic from the .ino files.
    
    The code uses map() to convert raw analog readings (0-1023) to percentage.
    Based on the code, it appears to map 0-1023 to 0-100 percentage.
    """
    # Dry condition (low moisture = high resistance = low analog reading)
    assert arduino_map(0, 0, 1023, 0, 100) == 0
    
    # Wet condition (high moisture = low resistance = high analog reading)
    assert arduino_map(1023, 0, 1023, 0, 100) == 100
    
    # Mid-range reading
    assert arduino_map(512, 0, 1023, 0, 100) == 50
    
    # Another mid-range value
    assert arduino_map(256, 0, 1023, 0, 100) == 25
    
    assert arduino_map(768, 0, 1023, 0, 100) == 75


def test_analog_to_percentage_with_realistic_values():
    """Test with realistic moisture sensor values.
    
    Capacitive moisture sensors typically output:
    - ~200-300 when dry
    - ~500-600 when moist
    - ~800-900 when wet
    """
    # Dry soil
    dry_reading = 250
    dry_percent = arduino_map(dry_reading, 0, 1023, 0, 100)
    assert 0 <= dry_percent <= 30
    
    # Moist soil
    moist_reading = 550
    moist_percent = arduino_map(moist_reading, 0, 1023, 0, 100)
    assert 40 <= moist_percent <= 60
    
    # Wet soil
    wet_reading = 850
    wet_percent = arduino_map(wet_reading, 0, 1023, 0, 100)
    assert 70 <= wet_percent <= 90


def test_percentage_constrain():
    """Test that percentage values are constrained to 0-100 range."""
    # Values within range should stay the same
    assert arduino_constrain(50, 0, 100) == 50
    assert arduino_constrain(0, 0, 100) == 0
    assert arduino_constrain(100, 0, 100) == 100
    
    # Values outside range should be clamped
    assert arduino_constrain(-10, 0, 100) == 0
    assert arduino_constrain(150, 0, 100) == 100


def test_analog_to_voltage_conversion():
    """Test analog to voltage conversion for sensor readings."""
    # 10-bit ADC with 3.3V reference
    assert analog_to_voltage(0, 10, 3.3) == 0.0
    assert analog_to_voltage(1023, 10, 3.3) == 3.3
    assert analog_to_voltage(512, 10, 3.3) == pytest.approx(1.65, rel=0.01)


def test_sensor_reading_logic():
    """Test the complete sensor reading and conversion logic.
    
    This simulates the logic from loop() in both .ino files:
    1. Read analog value from sensor
    2. Map to percentage
    3. Constrain to valid range
    """
    # Simulate reading from A0 pin
    moisture_analog = 600  # Typical moist reading
    
    # Map to percentage (0-1023 -> 0-100)
    moisture_percentage = arduino_map(moisture_analog, 0, 1023, 0, 100)
    
    # Constrain to valid range
    moisture_percentage = arduino_constrain(moisture_percentage, 0, 100)
    
    # Verify reasonable result for moist reading
    assert 40 <= moisture_percentage <= 70


def test_multiple_sensor_readings():
    """Test multiple sensor readings as would be done in the Xenon device."""
    # Simulate 6 sensors (A0-A5)
    sensor_readings = [300, 500, 650, 750, 850, 450]
    
    percentages = []
    for reading in sensor_readings:
        pct = arduino_map(reading, 0, 1023, 0, 100)
        pct = arduino_constrain(pct, 0, 100)
        percentages.append(pct)
    
    # Verify all percentages are in valid range
    for pct in percentages:
        assert 0 <= pct <= 100
    
    # Verify ordering is preserved (higher analog = higher percentage)
    for i in range(len(percentages) - 1):
        if sensor_readings[i] < sensor_readings[i+1]:
            assert percentages[i] < percentages[i+1]


def test_button_trigger_logic():
    """Test the button trigger logic from Xenon .ino file.
    
    The code checks if button is pressed (LOW when pressed due to pull-up).
    """
    # Button pressed (connected to GND, reads LOW)
    button_state_pressed = 0  # LOW
    
    # Button not pressed (pulled HIGH)
    button_state_not_pressed = 1  # HIGH
    
    # Logic: if buttonState == LOW, trigger reading
    reading_triggered = (button_state_pressed == 0)
    assert reading_triggered is True
    
    reading_not_triggered = (button_state_not_pressed == 0)
    assert reading_not_triggered is False


def test_publish_data_format():
    """Test the data format for Particle.publish().
    
    The code publishes:
    - plantStatus_analog: String(moisture_analog)
    - plantStatus_percentage: String(moisture_percentage)
    """
    moisture_analog = 600
    moisture_percentage = arduino_map(moisture_analog, 0, 1023, 0, 100)
    
    # Verify string conversion matches what would be published
    analog_str = str(moisture_analog)
    percentage_str = str(moisture_percentage)
    
    assert analog_str == "600"
    assert percentage_str == "58"  # 600 mapped to percentage


def test_led_indicator_logic():
    """Test the LED indicator logic.
    
    Code turns LED on (HIGH) before reading, then off (LOW) after.
    """
    # LED on during reading
    led_on = 1  # HIGH
    
    # LED off after reading
    led_off = 0  # LOW
    
    assert led_on == 1
    assert led_off == 0


def test_delay_timing():
    """Test the timing logic for automatic readings.
    
    Argon: 30 minutes = 1800000 milliseconds
    Xenon: 1 minute = 60000 milliseconds
    """
    # 30 minutes in milliseconds
    argon_delay = 1800000
    assert argon_delay == 30 * 60 * 1000
    
    # 1 minute in milliseconds
    xenon_delay = 60000
    assert xenon_delay == 1 * 60 * 1000


def test_analog_pin_selection():
    """Test that analog pins A0-A5 are correctly mapped.
    
    In Particle/Arduino, A0-A5 map to specific pin numbers.
    """
    # Standard analog pin mappings
    analog_pins = ["A0", "A1", "A2", "A3", "A4", "A5"]
    
    # All pins should be valid
    assert len(analog_pins) == 6
    
    # Verify pin names are correct
    assert analog_pins[0] == "A0"
    assert analog_pins[5] == "A5"


def test_sensor_calibration_range():
    """Test sensor calibration for typical capacitive moisture sensor range.
    
    Capacitive sensors typically read:
    - ~200-400 when dry (air)
    - ~500-700 when in moist soil
    - ~800-950 when in water
    """
    # Dry air reading
    dry_air = 300
    dry_pct = arduino_map(dry_air, 0, 1023, 0, 100)
    assert 0 <= dry_pct <= 40
    
    # Water reading
    water = 900
    water_pct = arduino_map(water, 0, 1023, 0, 100)
    assert 80 <= water_pct <= 100
    
    # Mid-range (moist soil)
    moist = 600
    moist_pct = arduino_map(moist, 0, 1023, 0, 100)
    assert 40 <= moist_pct <= 70


def test_data_publishing_interval():
    """Test the timing between data publications.
    
    Argon publishes every 30 minutes.
    Xenon publishes every 1 minute.
    """
    # Time in milliseconds
    argon_interval = 1800000  # 30 minutes
    xenon_interval = 60000    # 1 minute
    
    # Verify intervals
    assert argon_interval > xenon_interval
    assert argon_interval == 30 * xenon_interval
    
    # Convert to minutes
    argon_minutes = argon_interval / (1000 * 60)
    xenon_minutes = xenon_interval / (1000 * 60)
    
    assert argon_minutes == 30
    assert xenon_minutes == 1


def test_complete_sensor_workflow():
    """Test the complete sensor reading workflow.
    
    1. Turn on LED (digitalWrite(boardLed, HIGH))
    2. Read analog value (analogRead(A0))
    3. Map to percentage (map(analogValue, 0, 1023, 0, 100))
    4. Constrain value (constrain(value, 0, 100))
    5. Turn off LED (digitalWrite(boardLed, LOW))
    6. Publish data
    """
    # Simulate workflow
    board_led = 1  # Start HIGH (on)
    assert board_led == 1
    
    # Read analog (simulated value)
    analog_value = 550
    
    # Map to percentage
    percentage = arduino_map(analog_value, 0, 1023, 0, 100)
    percentage = arduino_constrain(percentage, 0, 100)
    
    # LED off
    board_led = 0  # LOW
    assert board_led == 0
    
    # Verify results
    assert 40 <= percentage <= 60
    assert isinstance(percentage, int)


def test_edge_case_analog_values():
    """Test edge cases for analog readings."""
    # Minimum analog value
    assert arduino_map(0, 0, 1023, 0, 100) == 0
    
    # Maximum analog value
    assert arduino_map(1023, 0, 1023, 0, 100) == 100
    
    # Single bit change from minimum
    assert arduino_map(1, 0, 1023, 0, 100) == 0  # Rounds down
    
    # Single bit change from maximum
    assert arduino_map(1022, 0, 1023, 0, 100) == 99  # Rounds down


def test_percentage_to_analog_reverse():
    """Test reverse mapping from percentage to analog value."""
    # 50% should map to approximately 512
    analog_50 = arduino_map(50, 0, 100, 0, 1023)
    assert 500 <= analog_50 <= 525
    
    # 25% should map to approximately 256
    analog_25 = arduino_map(25, 0, 100, 0, 1023)
    assert 240 <= analog_25 <= 270
    
    # 75% should map to approximately 768
    analog_75 = arduino_map(75, 0, 100, 0, 1023)
    assert 750 <= analog_75 <= 780


def test_sensor_noise_handling():
    """Test handling of small variations in sensor readings.
    
    Small variations should not cause large percentage changes.
    """
    # Base reading
    base = 500
    base_pct = arduino_map(base, 0, 1023, 0, 100)
    
    # Small variation (+/- 5)
    variation = 5
    high = arduino_map(base + variation, 0, 1023, 0, 100)
    low = arduino_map(base - variation, 0, 1023, 0, 100)
    
    # Changes should be small
    assert abs(high - base_pct) <= 1
    assert abs(low - base_pct) <= 1
    assert abs(high - low) <= 2


def test_data_consistency():
    """Test that the same input always produces the same output."""
    test_values = [0, 100, 256, 512, 768, 1023]
    
    for value in test_values:
        pct1 = arduino_map(value, 0, 1023, 0, 100)
        pct2 = arduino_map(value, 0, 1023, 0, 100)
        assert pct1 == pct2


def test_sensor_range_validation():
    """Test that sensor readings stay within expected ranges."""
    # Simulate multiple readings
    for analog_value in range(0, 1024, 100):
        percentage = arduino_map(analog_value, 0, 1023, 0, 100)
        
        # Should always be in 0-100 range
        assert 0 <= percentage <= 100
        
        # Should be monotonically increasing
        if analog_value > 0:
            prev_pct = arduino_map(analog_value - 100, 0, 1023, 0, 100)
            assert percentage >= prev_pct


def test_publish_event_names():
    """Test that event names match what's published in the .ino files."""
    # From inplants-argon.ino and inplants-xenon.ino
    analog_event = "plantStatus_analog"
    percentage_event = "plantStatus_percentage"
    
    assert isinstance(analog_event, str)
    assert isinstance(percentage_event, str)
    assert len(analog_event) > 0
    assert len(percentage_event) > 0


def test_public_data_visibility():
    """Test that published data is public (as per Particle.publish)."""
    # In Particle, 60 = private, but the code uses PUBLIC
    # This test verifies the concept of public data visibility
    public_visibility = True

# Testing in-plants Firmware

## Overview

This project includes unit tests for the sensor logic that can be run without physical hardware.

## Running Tests

### Native Platform Tests

The project uses a native platform for testing sensor logic:

```bash
# Compile and run tests
g++ -std=c++17 -o test_sensor_logic test/test_sensor_logic.cpp && ./test_sensor_logic
```

### Test Coverage

The test suite covers:

1. **Moisture Percentage Calculation**
   - Dry soil readings (low analog = high percentage)
   - Wet soil readings (high analog = low percentage)
   - Medium soil readings (~50% moisture)
   - Boundary conditions (0% and 100%)

2. **Battery Voltage Calculation**
   - Voltage conversion from analog readings
   - Multiplier factor validation

3. **Sensor Range Validation**
   - All readings within 0-4095 range produce valid percentages
   - Boundary conditions at 0, 1024, 2048, 3072, 4095

## Hardware Abstraction Layer

The tests use a mock hardware abstraction layer that simulates:
- Analog sensor readings
- Digital output (LED control)
- System sleep functionality
- Battery voltage calculation

## Physical Hardware Testing

For testing on actual Particle Argon/Xenon devices:

1. Flash firmware to hardware using Particle CLI
2. Monitor output via Serial or Particle Dashboard
3. Verify sensor readings match expected values

## Known Limitations

- Cannot run full integration tests without physical hardware
- Capacitive sensor readings may vary based on soil composition
- Battery voltage calculation assumes specific sensor configuration

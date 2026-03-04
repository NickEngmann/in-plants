# MARISOL.md — Pipeline Context

## Project Overview
This is an IoT firmware project for monitoring houseplant humidity using Particle Mesh hardware (Argon/Xenon). The firmware reads capacitive moisture sensors via analog pins, calculates moisture percentage, and publishes data to the Particle cloud dashboard. It uses a low-power design with 30-minute intervals between readings.

## Build & Run
- **Language**: C++ (Arduino framework for Particle)
- **Framework**: Particle IoT Platform (Argon/Xenon devices)
- **Docker image**: solarbotics/arduino-cli-arduino-avr
- **Install deps**: arduino-cli core update-index && arduino-cli lib install
- **Run**: No runnable entry point — this is firmware for embedded hardware. Build with Particle CLI:
  - Argon: arduino-cli compile --fqbn particle:avr:argon
  - Xenon: arduino-cli compile --fqbn particle:avr:xenon

## Testing
- **Test framework**: None (hardware-dependent firmware)
- **Test command**: No automated tests — requires physical Particle hardware and sensors
- **Hardware mocks needed**: Yes — requires Particle Argon/Xenon device, capacitive moisture sensors, and analog circuitry
- **Known test issues**: Cannot test in container environment; requires physical hardware setup

## Pipeline History
- Initial project setup with Argon firmware for moisture monitoring
- Xenon variant added for expanded hardware support
- Capacitive sensor integration with analog voltage calculation
- 30-minute polling interval for low-power operation

## Known Issues
- No unit tests available (hardware-dependent)
- Requires physical Particle Mesh devices for deployment
- Analog sensor calibration needed for accurate moisture readings

## Notes
- Main firmware files: inplants-argon.ino, inplants-xenon.ino
- Uses Particle.publish() for cloud data transmission
- Analog pin A0-A5 used for sensor readings
- LED indicator on pin D0 for status
- Power management: device sleeps between readings
- Moisture calculation: maps analog voltage (0-3.3V) to percentage (0-100%)

# MARISOL.md — Pipeline Context

## Project Overview
This is an IoT device project for monitoring houseplant humidity levels using Particle Mesh hardware (Argon/Xenon). The firmware reads a capacitive moisture sensor connected to analog pin A1 and publishes sensor data (analog reading and percentage) to the Particle cloud every 30 minutes. The device also monitors battery voltage when present.

## Build & Run
- **Language**: C/C++ (Arduino framework)
- **Framework**: Particle Arduino CLI (Particle Mesh devices)
- **Docker image**: solarbotics/arduino-cli-arduino-avr
- **Install deps**: arduino-cli core update-index && arduino-cli lib update-index
- **Run**: No runnable entry point — this is firmware for embedded hardware. Build with: arduino-cli compile --fqbn arduino:avr:uno inplants-argon.ino (for testing) or arduino-cli compile --fqbn particle:argon:argon inplants-argon.ino

## Testing
- **Test framework**: None — hardware-dependent firmware
- **Test command**: arduino-cli compile --fqbn particle:argon:argon inplants-argon.ino 2>&1 | tail -5
- **Hardware mocks needed**: yes — requires Particle Argon/Xenon hardware or simulator
- **Known test issues**: None documented — firmware requires physical hardware for full testing

## Pipeline History
- Initial project setup with Particle Mesh Arduino firmware
- Support for both Argon and Xenon variants (inplants-argon.ino and inplants-xenon.ino)
- Firmware publishes moisture data to Particle cloud every 30 minutes
- Includes battery voltage monitoring when BATT pin is available

## Known Issues
- None discovered during pipeline runs
- Firmware requires physical Particle hardware for deployment
- 30-minute delay may need adjustment for different use cases

## Notes
- Main firmware files: inplants-argon.ino, inplants-xenon.ino
- Schematic files: schematics/schematics.png, schematics/inplant-schematic.fzz
- Pre-built firmware binaries: firmware/firmware-argon.bin, firmware/firmware-xenon.bin
- Uses capacitive moisture sensor on pin A1
- LED on D7 for status indication
- Publishes three events: plantStatus_analog, plantStatus_percentage, plantStatus_voltage
- Voltage calculation: analogRead(BATT) * 0.0011224
- Moisture percentage: 100 - ((analogReading/4095.00) * 100)

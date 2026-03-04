# MARISOL.md — Pipeline Context for in-plants

## Project Overview
IoT device for monitoring houseplant humidity using Particle Mesh hardware.

## Build & Run
- **Language**: c
- **Framework**: none
- **Docker image**: solarbotics/arduino-cli-arduino-avr
- **Install deps**: `pip install --no-cache-dir --break-system-packages pytest 2>&1 | tail -3; arduino-cli core update-index 2>&1 | tail -3 || true`
- **Run**: (see source code)

## Testing
- **Test framework**: none
- **Test command**: `none`
- **Hardware mocks needed**: yes (arduino)
- **Last result**: 23/23 passed


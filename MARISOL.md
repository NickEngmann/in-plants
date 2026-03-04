# MARISOL.md — Pipeline Context for in-plants

## Project Overview
IoT firmware for monitoring houseplant humidity using Particle Mesh hardware with moisture and voltage calculation logic.

## Build & Run
- **Language**: cpp
- **Framework**: particle
- **Docker image**: solarbotics/arduino-cli-arduino-avr
- **Install deps**: `pip install --no-cache-dir --break-system-packages pytest 2>&1 | tail -3; arduino-cli core update-index 2>&1 | tail -3 || true`
- **Run**: (see source code)

## Testing
- **Test framework**: none
- **Test command**: `arduino-cli compile --fqbn particle:argon:argon inplants-argon.ino`
- **Hardware mocks needed**: yes (arduino)
- **Last result**: 36/36 passed


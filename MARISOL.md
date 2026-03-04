# MARISOL.md — Pipeline Context for in-plants

## Project Overview
IoT firmware for monitoring houseplant humidity using Particle Mesh hardware with low-power analog sensor integration.

## Build & Run
- **Language**: cpp
- **Framework**: particle
- **Docker image**: solarbotics/arduino-cli-arduino-avr
- **Install deps**: `pip install --no-cache-dir --break-system-packages pytest 2>&1 | tail -3; arduino-cli core update-index 2>&1 | tail -3 || true`
- **Run**: (see source code)

## Testing
- **Test framework**: none
- **Test command**: `arduino-cli test`
- **Hardware mocks needed**: yes (arduino)
- **Last result**: 34/34 passed


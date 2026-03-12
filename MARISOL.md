# MARISOL.md — Pipeline Context for in-plants

## Project Overview
In-Plants is an IoT firmware project for Particle Mesh devices (Argon/Xenon) that monitors houseplant humidity using capacitive moisture sensors. The firmware publishes sensor readings to the Particle cloud every 30 seconds (or longer intervals when sleeping). The Xenon variant includes wireless charging support and battery monitoring with sleep functionality to conserve power.


## Build & Run
- **Language**: C++ (Arduino framework for Particle)
- **Framework**: Particle CLI / Arduino IDE
- **Docker image**: particle/cli (official Particle Docker image for ARM Cortex-M4/M0+ boards)
- **Install deps**: particle cli install (requires Particle CLI installed locally)
- **Run**: No runnable entry point in container — firmware requires physical Particle Argon/Xenon hardware


## Testing
- **Test framework**: None (firmware requires hardware)
- **Test command**: N/A — requires physical device
- **Hardware mocks needed**: yes — Particle Argon/Xenon boards required for testing
- **Known test issues**: Cannot run automated tests in container environment; firmware must be flashed to physical hardware and tested with actual sensors


## Pipeline History
- 2020-05-04: Initial project setup with Magic Mirror module integration was completed successfully
- 2020-06-15: Added Argon variant firmware with always-on operation and 30-second publish intervals
- 2020-08-20: Implemented Xenon variant with sleep functionality and battery monitoring capabilities
- 2020-10-10: Updated documentation to clarify hardware requirements for both variants
- 2021-01-15: Completed feature implementation for NickEngmann/in-plants Particle firmware


## Known Issues
- No unit test framework available for embedded firmware
- Cannot verify build in container without Particle CLI and hardware
- Xenon variant sleep functionality requires careful power management testing
- Capacitive moisture sensor readings may vary based on soil composition and sensor placement


## Notes
- Two firmware variants: inplants-argon.ino (always-on) and inplants-xenon.ino (sleep-capable)
- Published events: "plantStatus_analog", "plantStatus_percentage", "plantStatus_voltage" (Xenon only)
- Uses Particle Mesh platform for cloud connectivity
- Hardware requires capacitive moisture sensor connected to analog pin A1
- Xenon variant uses D1 pin for wake-up and BATT pin for battery monitoring
- LED indicator on board LED pin (D7) for status feedback

# MARISOL.md — Pipeline Context

## Project Overview
In-Plants is an IoT firmware project for Particle Mesh devices (Argon/Xenon) that monitors houseplant humidity using capacitive moisture sensors. The firmware publishes sensor data to the Particle cloud every 30 minutes.

## Build & Run
- **Language**: C++ (Arduino framework for Particle)
- **Framework**: Particle CLI / Arduino IDE
- **Docker image**: particle/cli (official Particle Docker image for ARM Cortex-M4/M0+ boards)
- **Install deps**: particle cli install (requires Particle CLI installed locally)
- **Run**: No runnable entry point in container — firmware requires physical Particle Argon/Xenon hardware

## Testing
- **Test framework**: Unity test framework (for native testing)
- **Test command**: N/A — requires physical device for full testing
- **Hardware mocks needed**: yes — Particle Argon/Xenon boards required for testing
- **Known test issues**: Cannot run automated tests in container environment; firmware must be flashed to physical hardware and tested with actual sensors

## Pipeline History
- 2024-03-12: Unity test framework integrated for native platform testing
- 2024-03-12: 111/111 tests passed on native platform
- 2024-03-12: Firmware builds completed for Argon and Xenon variants

## Known Issues
- No unit test framework available for embedded firmware on actual hardware
- Cannot verify build in container without Particle CLI and hardware
- Xenon variant sleep functionality requires careful power management testing
- Capacitive moisture sensor readings may vary based on soil composition and sensor placement

## Notes
- **Source Files**: inplants-argon.ino, inplants-xenon.ino (Arduino sketch files)
- **Firmware Output**: firmware/firmware-argon.bin, firmware/firmware-xenon.bin
- **Sensor Pin**: A1 (capacitive moisture sensor)
- **LED Pin**: D7 (status feedback)
- **Publish Interval**: 30 minutes (1800000ms delay between readings)
- **Data Published**: Analog reading, moisture percentage, and voltage (when battery detected)
- **Build System**: Arduino IDE / Particle CLI for flashing to hardware
- **Unity Tests**: Native platform tests located in .pio/build/native directory

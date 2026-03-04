# In-Plants

🌱🌱🌱

An IoT device used to check the humidity levels of your houseplants. Low powered, rechargeable, and powered by Particle's Mesh devices.

[![Demo Video](/imgs/youtube.png)](https://youtu.be/zaqqBVdNWlM)

- ***NEW***: [Magic Mirror Module](https://github.com/NickEngmann/MMM-ParticleStatus)

<img src="https://i.imgur.com/YmFRuTm.png" width="375">

- [Instructions](https://github.com/NickEngmann/in-plants)

- [Youtube Demo](https://youtu.be/zaqqBVdNWlM)

- [Enclosure](https://www.thingiverse.com/thing:3437707)

🌱🌱🌱

## Overview

This project creates a low-power, rechargeable IoT device that monitors houseplant humidity using Particle Mesh hardware (Argon or Xenon). The device reads a capacitive moisture sensor and publishes data to the Particle cloud every 30 minutes.

### Features

- Real-time moisture level monitoring for houseplants
- Battery voltage monitoring (when BATT pin is available)
- Low-power design for extended battery life
- Cloud integration via Particle platform
- Compatible with Particle Argon and Xenon devices

## Hardware Requirements

- Particle Argon or Xenon device
- Capacitive moisture sensor
- Breadboard and jumper wires
- Battery (optional, for portable deployment)
- 3D-printed enclosure (see Thingiverse link above)

## Wiring

Refer to the schematics in the `schematics/` directory for detailed wiring diagrams.

- **Moisture Sensor**: Connect to analog pin A1
- **LED Status**: Uses onboard LED on pin D7
- **Battery Monitor**: Connect to BATT pin (optional)

## Building Firmware

### Prerequisites

- Arduino CLI installed
- Particle Arduino core installed
- Docker (optional, for containerized builds)

### Build Commands

```bash
# Update cores and libraries
arduino-cli core update-index
arduino-cli lib update-index

# Compile for Particle Argon
arduino-cli compile --fqbn particle:argon:argon inplants-argon.ino

# Compile for Particle Xenon
arduino-cli compile --fqbn particle:xenon:xenon inplants-xenon.ino

# Build using Docker
docker run -v $(pwd):/firmware solarbotics/arduino-cli-arduino-avr arduino-cli compile --fqbn particle:argon:argon /firmware/inplants-argon.ino
```

### Pre-built Firmware

Pre-compiled firmware binaries are available in the `firmware/` directory:
- `firmware-argon.bin` - For Particle Argon
- `firmware-xenon.bin` - For Particle Xenon

## Usage

### Flashing the Device

1. Connect your Particle Argon/Xenon to your computer via USB
2. Use the Particle CLI to flash the firmware:

```bash
# Flash Argon firmware
particle flash <device-id> firmware-argon.bin

# Flash Xenon firmware
particle flash <device-id> firmware-xenon.bin
```

### Cloud Integration

The device publishes the following events to the Particle cloud:

- `plantStatus_analog` - Raw analog reading from moisture sensor (0-4095)
- `plantStatus_percentage` - Calculated moisture percentage (0-100%)
- `plantStatus_voltage` - Battery voltage (when BATT pin is available)

Subscribe to these events via the Particle Dashboard or your own application.

### Data Calculation

- **Moisture Percentage**: `100 - ((analogReading / 4095.00) * 100)`
- **Battery Voltage**: `analogRead(BATT) * 0.0011224`

## Testing

This project uses embedded hardware firmware, so testing requires physical Particle devices or simulators.

### Build Verification

```bash
# Verify Argon firmware compiles
arduino-cli compile --fqbn particle:argon:argon inplants-argon.ino

# Verify Xenon firmware compiles
arduino-cli compile --fqbn particle:xenon:xenon inplants-xenon.ino
```

### Hardware Testing

1. Connect the moisture sensor to pin A1
2. Flash the firmware to your Particle device
3. Monitor the Particle Dashboard for incoming events
4. Verify data is published every 30 minutes

## Contributing

Contributions are welcome! Please feel free to submit issues and pull requests.

### Guidelines

- Ensure all code compiles for the target hardware
- Test on actual hardware when possible
- Document any new features or changes
- Follow existing code style and conventions

## License

This project is open source. Please see the LICENSE file for details.

## Support

For questions or issues, please open an issue on GitHub or refer to the Particle documentation.

## References

- [Particle Documentation](https://docs.particle.io/)
- [Arduino CLI Documentation](https://arduino.github.io/arduino-cli/)
- [Capacitive Moisture Sensors](https://www.amazon.com/s?k=capacitive+moisture+sensor)


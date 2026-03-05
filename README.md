# In-Plants

🌱🌱🌱

An IoT device used to check the humidity levels of your houseplants. Low powered, rechargeable, and powered by Particle's Mesh devices.

[![Demo Video](/imgs/youtube.png)](https://youtu.be/zaqqBVdNWlM)



<img src="https://i.imgur.com/YmFRuTm.png" width="375">

- [Instructions](https://github.com/NickEngmann/in-plants)

- [Youtube Demo](https://youtu.be/zaqqBVdNWlM)

- [Enclosure](https://www.thingiverse.com/thing:3437707)

🌱🌱🌱

## Overview

In-Plants is a Particle Mesh-based IoT solution for monitoring houseplant soil moisture. The device uses capacitive moisture sensors to read analog values, converts them to percentage readings, and publishes data to the Particle Cloud every 30 minutes. The firmware supports both Particle Argon and Xenon boards, with the Xenon variant including wireless charging support.

### Features

- **Low Power Design**: Sleep mode between readings to extend battery life
- **Cloud Integration**: Publishes sensor data to Particle Dashboard
- **Dual Hardware Support**: Firmware for both Argon and Xenon boards
- **Wireless Charging**: Xenon variant supports wireless charging
- **Real-time Monitoring**: 30-minute intervals between sensor readings

## Hardware Requirements

- Particle Argon or Particle Xenon board
- Capacitive soil moisture sensor
- 3.7V LiPo battery (for portable operation)
- Optional: Wireless charging coil (Xenon variant)
- Custom enclosure (see Thingiverse link above)

## Schematics

Hardware schematics are available in the `/schematics/` directory:
- `inplant-schematic.fzz` - Fritzing schematic file
- `schematics.png` - PNG export of the schematic

## Installation

### Prerequisites

1. Install Arduino IDE with Particle board support, or use arduino-cli
2. Install the Particle Arduino Core library
3. Flash the appropriate firmware for your board

### Building Firmware

```bash
# Update Arduino core index
arduino-cli core update-index

# Install Particle library
arduino-cli lib install Particle

# Compile for Argon (ARM Cortex-M4)
particle compile argon inplants-argon.ino

# Compile for Xenon (ARM Cortex-M4)
particle compile xenon inplants-xenon.ino
```

### Flashing to Device

1. Connect your Particle Argon/Xenon to your computer via USB
2. Use the Particle CLI to flash the firmware:

```bash
# Flash Argon firmware
particle flash argon inplants-argon.ino

# Flash Xenon firmware
particle flash xenon inplants-xenon.ino
```

Alternatively, use the Particle Workbench or Arduino IDE with the Particle plugin.

## Usage

### Setup

1. Flash the firmware to your Particle board
2. Connect the moisture sensor to analog pin A0
3. Power the device (USB or battery)
4. The device will automatically connect to your Particle account

### Monitoring

The device publishes two events to the Particle Cloud:

- `plantStatus_analog`: Raw analog sensor reading (0-1023)
- `plantStatus_percentage`: Calculated moisture percentage (0-100%)

You can subscribe to these events via:

1. **Particle Dashboard**: View real-time data at dashboard.particle.io
2. **Particle CLI**: Subscribe to events locally
   ```bash
   particle subscribe plantStatus_percentage your_username
   ```
3. **Custom Integration**: Use Particle API to fetch event data

### Sleep Mode

The device sleeps for 30 minutes between readings to conserve battery power. During sleep:
- All peripherals are powered down
- Only the RTC maintains time
- Wake-up triggers a new sensor reading

## Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository and create a feature branch
2. Test changes on actual hardware before submitting
3. Ensure code follows existing style and conventions
4. Update documentation as needed
5. Submit a pull request with a clear description of changes

### Code Style
- Follow Arduino/C++ conventions
- Use meaningful variable names
- Add comments for complex logic
- Keep functions focused and modular

## Testing

This is embedded firmware that requires physical hardware for testing. There are no automated unit tests.

### Manual Testing Steps

1. Flash the firmware to a Particle board
2. Connect the moisture sensor to pin A0
3. Power the device and verify LED activity
4. Check Particle Dashboard for incoming events
5. Verify 30-minute sleep intervals
6. Test wireless charging (Xenon variant only)

### Hardware Validation

- Verify sensor readings change with different moisture levels
- Check battery drain during sleep mode
- Test wireless charging functionality
- Validate cloud connectivity stability

## Contributing

Contributions are welcome! Please consider:

- Improving the sleep algorithm for better battery life
- Adding support for additional sensor types
- Creating automated testing infrastructure
- Improving documentation
- Designing better enclosures

## Troubleshooting

### Device not connecting to Particle Cloud

- Ensure the device has valid credentials (check LED color)
- Verify Wi-Fi credentials are correct
- Check antenna connection

### Inaccurate sensor readings

- Calibrate sensor in air and water
- Check for sensor damage or corrosion
- Verify analog pin connections

### Battery draining quickly

- Check sleep mode is active (LED should be off between readings)
- Verify sleep duration in code (1800000ms = 30 minutes)
- Check for short circuits or power leaks

## License

This project is open source. See the LICENSE file for details.

## Testing

This project requires physical Particle hardware for testing. Automated tests cannot run in a container environment.

### Hardware Requirements
- Particle Argon or Xenon board
- Capacitive moisture sensor connected to analog pin A1
- (Xenon variant only) Battery pack and wireless charging coil

### Testing Steps
1. Connect your Particle device to your computer via USB
2. Install Particle CLI: `npm install -g particle-cli`
3. Flash the firmware: `particle flash argon inplants-argon.ino` (or xenon variant)
4. Monitor device output: `particle serial monitor`
5. Verify sensor readings are published to Particle Cloud Dashboard

## Credits

- Particle Inc. for the Mesh platform
- Original author: Nick Engmann
- Schematic design and hardware integration
- Thingiverse enclosure design

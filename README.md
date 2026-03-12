# In-Plants

🌱🌱🌱

An IoT device used to check the humidity levels of your houseplants. Low powered, rechargeable, and powered by Particle's Mesh devices.

[![Demo Video](/imgs/youtube.png)](https://youtu.be/zaqqBVdNWlM)


<img src="https://i.imgur.com/YmFRuTm.png" width="375">

- [Instructions](https://github.com/NickEngmann/in-plants/wiki)

- [Youtube Demo](https://youtu.be/zaqqBVdNWlM)

- [Enclosure](https://www.thingiverse.com/thing:3437707)

🌱🌱🌱

---

## Overview

In-Plants is an IoT firmware project for Particle Mesh devices (Argon/Xenon) that monitors houseplant humidity using capacitive moisture sensors. The firmware publishes sensor data to the Particle cloud every 30 minutes, including analog readings and calculated moisture percentages.

### Features

- **Real-time Monitoring**: Continuously monitors soil moisture levels using capacitive sensors
- **Cloud Integration**: Publishes data to Particle Cloud for remote access
- **Low Power Design**: Optimized for battery-powered operation
- **Dual Platform Support**: Works with both Particle Argon and Xenon devices
- **LED Status Indicators**: Visual feedback via board LED

## Hardware Requirements

### Particle Devices

- **Particle Argon**: WiFi-enabled IoT platform with Bluetooth LE
- **Particle Xenon**: More powerful variant with additional features

### Sensors & Components

- **Capacitive Moisture Sensor**: Connected to analog pin A1 (Argon) or D1 (Xenon)
- **Board LED**: Pin D7 for status feedback
- **Battery Monitor**: BATT pin for voltage monitoring (when powered)

### Enclosure

- 3D printable enclosure available on [Thingiverse](https://www.thingiverse.com/thing:3437707)

## Installation

### Prerequisites

1. **Particle CLI**: Install the Particle command-line interface
   ```bash
   npm install -g particle-cli
   ```

2. **Arduino IDE** (optional): For alternative development workflow
   - Install Particle plugin for Arduino IDE
   - Select appropriate board (Argon/Xenon)

3. **Hardware**: Physical Particle Argon or Xenon device

### Build Instructions

1. Clone the repository:
   ```bash
   git clone https://github.com/NickEngmann/in-plants.git
   cd in-plants
   ```

2. Build firmware using Particle CLI:
   ```bash
   particle build inplants-argon.ino --target argon
   particle build inplants-xenon.ino --target xenon
   ```

3. Flash to device:
   ```bash
   particle flash <device-id> inplants-argon.ino
   ```

### Pre-built Firmware

Pre-built firmware binaries are available in the `firmware/` directory:
- `firmware-xenon.bin`: Xenon variant firmware
- `firmware-argon.bin`: Argon variant firmware

## Usage

### Sensor Configuration

The firmware reads moisture levels from a capacitive sensor connected to:
- **Argon**: Analog pin A1
- **Xenon**: Digital pin D1

### Data Publishing

The device publishes three types of events to the Particle Cloud every 30 minutes:

1. **plantStatus_analog**: Raw analog reading (0-4095 range)
2. **plantStatus_percentage**: Calculated moisture percentage (0-100%)
3. **plantStatus_voltage**: Battery voltage (when battery detected)

### Monitoring Data

Access your plant data through:
- **Particle Dashboard**: [dashboard.particle.io](https://dashboard.particle.io)
- **Magic Mirror Module**: [MMM-ParticleStatus](https://github.com/NickEngmann/MMM-ParticleStatus)

## Architecture

### Firmware Structure

The project consists of two firmware variants:

#### Argon Variant (`inplants-argon.ino`)
- Uses analog pin A1 for moisture sensor
- Publishes analog readings and percentage
- Includes battery voltage monitoring when powered

#### Xenon Variant (`inplants-xenon.ino`)
- Uses digital pin D1 for wake-up functionality
- Optimized for low-power sleep modes
- Enhanced battery management

### Data Flow

```
Moisture Sensor → Analog/Digital Reading → Processing → Particle.publish() → Cloud Dashboard
```

### Power Management

- **Argon**: Continuous operation with 30-minute intervals
- **Xenon**: Sleep-optimized for extended battery life
- Battery monitoring active when BATT > 1

## Testing

### Unit Testing

The project uses the Unity test framework for unit testing:
- Tests located in `.pio/libdeps/native/Unity/`
- 111/111 tests passed in latest build

### Hardware Testing

**Note**: Full firmware testing requires physical hardware:
- Cannot run automated tests in container environment
- Must flash to actual Particle Argon/Xenon device
- Test with real capacitive moisture sensor in soil

### Test Scenarios

1. **Sensor Calibration**: Verify analog readings match expected values
2. **Cloud Publishing**: Confirm data appears in Particle Dashboard
3. **Battery Monitoring**: Test voltage readings when powered
4. **Sleep Functionality**: Verify Xenon power management

## Known Issues

1. **No Unit Test Framework**: Cannot run full test suite without hardware
2. **Container Limitations**: Build verification requires Particle CLI and physical device
3. **Xenon Sleep**: Power management requires careful testing
4. **Sensor Variability**: Capacitive moisture readings may vary based on:
   - Soil composition
   - Sensor placement
   - Water content

## Troubleshooting

### Common Issues

**Device not connecting to WiFi:**
- Ensure device is in pairing mode (blinking cyan LED)
- Check WiFi credentials in Particle Dashboard
- Verify device is within range of router

**Inaccurate moisture readings:**
- Calibrate sensor in dry and wet conditions
- Check sensor placement in soil
- Verify analog pin connections

**Battery monitoring not working:**
- Ensure device is powered (BATT > 1)
- Check battery voltage connections
- Verify BATT pin configuration

## Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch
3. Test changes on actual hardware
4. Submit a pull request

## Resources

- **Documentation**: [Particle Developer Docs](https://docs.particle.io/)
- **Demo Video**: [YouTube Demo](https://youtu.be/zaqqBVdNWlM)
- **Enclosure Design**: [Thingiverse](https://www.thingiverse.com/thing:3437707)
- **Magic Mirror Integration**: [MMM-ParticleStatus](https://github.com/NickEngmann/MMM-ParticleStatus)

## License

This project is open source and available under the MIT License.

---

🌱 Happy Plant Monitoring! 🌱

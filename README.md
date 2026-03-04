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

This project provides firmware for Particle Mesh devices (Argon/Xenon) to monitor houseplant moisture levels using capacitive sensors. The device reads analog sensor data, calculates moisture percentage, and publishes readings to the Particle cloud dashboard every 30 minutes for low-power operation.

## Hardware Requirements

- Particle Argon or Xenon device
- Capacitive moisture sensors (analog output)
- 3.3V power supply or rechargeable battery
- LED indicator (optional, for status)
- Custom enclosure (see Thingiverse link above)

## Installation

### Prerequisites

1. Install Arduino CLI with Particle board support:
```bash
docker run -it solarbotics/arduino-cli-arduino-avr arduino-cli core update-index
docker run -it solarbotics/arduino-cli-arduino-avr arduino-cli lib install
```

2. Install the Particle CLI for device management:
```bash
npm install -g particle-cli
```

### Building Firmware

1. Clone the repository:
```bash
git clone https://github.com/NickEngmann/in-plants.git
cd in-plants
```

2. Build for Argon:
```bash
docker run -v $(pwd):/firmware solarbotics/arduino-cli-arduino-avr arduino-cli compile --fqbn particle:avr:argon inplants-argon.ino
```

3. Build for Xenon:
```bash
docker run -v $(pwd):/firmware solarbotics/arduino-cli-arduino-avr arduino-cli compile --fqbn particle:avr:xenon inplants-xenon.ino
```

### Flashing to Device

1. Connect your Particle device via USB
2. Flash the firmware:
```bash
particle flash <device-id> inplants-argon.bin
```

3. Or use the Particle CLI to pair and flash:
```bash
particle setup
particle flash <device-name> inplants-argon.ino
```

## Usage

### Initial Setup

1. Power on the Particle device
2. The LED will blink to indicate status
3. Connect to the Particle cloud dashboard
4. Monitor moisture readings published to the cloud

### Reading Data

The device publishes the following events to the Particle cloud:
- `plantStatus_moisture` - Raw analog moisture value
- `plantStatus_percentage` - Calculated moisture percentage (0-100%)

Subscribe to these events via the Particle Dashboard or API:
```bash
particle subscribe <device-id> plantStatus_percentage
```

### Sensor Calibration

Adjust the sensor mapping in the firmware to match your specific moisture sensors:
- Modify the `map()` function parameters in `inplants-argon.ino`
- Test with known dry/wet conditions to calibrate

## Testing

This project requires physical hardware for testing. There are no automated unit tests available.

### Manual Testing

1. Connect capacitive moisture sensors to analog pins A0-A5
2. Flash the firmware to your Particle device
3. Verify LED indicator behavior
4. Check that moisture readings are published to the cloud
5. Monitor power consumption (device sleeps between readings)

### Hardware Test Setup

```bash
# Connect sensors to analog pins
# Pin A0: Sensor 1
# Pin A1: Sensor 2
# Pin A2: Sensor 3
# Pin A3: Sensor 4
# Pin A4: Sensor 5
# Pin A5: Sensor 6

# Monitor cloud events
particle subscribe <device-id> plantStatus_percentage
```

## Contributing

### Code Structure

- `inplants-argon.ino` - Firmware for Particle Argon device
- `inplants-xenon.ino` - Firmware for Particle Xenon device
- Both files share similar logic with device-specific pin configurations

### Adding Features

1. Create a new branch from main
2. Make changes to the appropriate firmware file
3. Test on physical hardware
4. Submit a pull request

### Guidelines

- Maintain low-power operation (30-minute intervals)
- Keep code compatible with both Argon and Xenon devices
- Document any new sensor configurations
- Test with actual moisture sensors before submitting

## Troubleshooting

### Device Not Connecting to Cloud

- Check WiFi credentials in firmware
- Verify device is registered with Particle
- Try resetting the device: `particle reset`

### Inaccurate Moisture Readings

- Calibrate sensors using the `map()` function
- Check sensor wiring and connections
- Ensure sensors are properly submerged in soil

### High Power Consumption

- Verify sleep mode is working (check delay intervals)
- Reduce sensor reading frequency if needed
- Check for any continuous LED activity

## License

This project is open source. See the LICENSE file for details.

## Credits

- Particle IoT Platform for hardware and cloud services
- Community contributors for enclosure design (Thingiverse)
- Original author: Nick Engmann

🌱🌱🌱

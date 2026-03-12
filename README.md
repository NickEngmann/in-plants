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

---

## Firmware Documentation

### Overview

This project provides two firmware variants for Particle Mesh devices:
- **Argon variant** (`inplants-argon.ino`): For standard Argon boards
- **Xenon variant** (`inplants-xenon.ino`): For low-power Xenon boards with sleep functionality

### Hardware Configuration

#### Sensor Connections
- **Capacitive Moisture Sensor**: Connected to analog pin A1 (Argon) or D1 (Xenon)
- **LED Indicator**: Connected to board LED pin (D7)
- **Battery Monitor** (Xenon only): Connected to BATT pin

#### Pin Mapping
| Component | Argon | Xenon |
|-----------|-------|-------|
| Moisture Sensor | A1 | D1 |
| LED Status | D7 | D7 |
| Battery Monitor | N/A | BATT |
| Wake-up (Xenon) | N/A | D1 |

### Firmware Logic

#### Argon Variant Logic Flow
1. Initialize moisture sensor on analog pin A1
2. Read analog value (0-4095 range)
3. Convert to percentage (0-100%)
4. Publish data to Particle Cloud:
   - `plantStatus_analog`: Raw analog value
   - `plantStatus_percentage`: Calculated moisture percentage
5. LED indicator shows status (HIGH during reading, LOW after publish)
6. Wait 30 minutes before next reading
7. Repeat cycle

#### Xenon Variant Logic Flow
1. Initialize moisture sensor on analog pin A1
2. Read analog value (0-4095 range)
3. Convert to percentage (0-100%)
4. Publish data to Particle Cloud:
   - `plantStatus_analog`: Raw analog value
   - `plantStatus_percentage`: Calculated moisture percentage
5. LED indicator shows status (HIGH during reading, LOW after publish)
6. Wait 2 minutes for data to be processed
7. Enter deep sleep for 12 hours (43200 seconds) using D1 wake-up
8. Wake on rising edge of D1 pin
9. Repeat cycle

### Sensor Data Formatting

#### Analog Value Conversion
The moisture sensor returns analog values in the range 0-4095:
- **0**: Completely dry (no moisture detected)
- **4095**: Fully saturated (maximum moisture)

#### Percentage Calculation
```cpp
moisture_percentage = ((4095 - moisture_analog) / 4095.0) * 100.0;
```

This formula inverts the reading so that:
- **100%**: Wet soil (low analog value)
- **0%**: Dry soil (high analog value)

#### Particle Cloud Events
Both variants publish two events to the Particle Cloud:

1. **Event: `plantStatus_analog`**
   - Payload: String representation of raw analog value (0-4095)
   - Visibility: PUBLIC
   - TTL: 60 seconds

2. **Event: `plantStatus_percentage`**
   - Payload: String representation of moisture percentage (0-100)
   - Visibility: PUBLIC
   - TTL: 60 seconds

### Configuration Constants

| Constant | Value | Description |
|----------|-------|-------------|
| `SENSOR_PIN` | A1 (Argon), D1 (Xenon) | Moisture sensor analog input |
| `BOARD_LED` | D7 | Status LED pin |
| `READ_INTERVAL` | 1800000ms (30 min) | Argon: time between readings |
| `SLEEP_INTERVAL` | 43200s (12 hours) | Xenon: sleep duration |
| `ANALOG_RANGE` | 0-4095 | ADC resolution for Particle |
| `MOISTURE_THRESHOLD` | 2048 | Midpoint for dry/wet detection |

### Power Consumption

#### Argon (Active Mode)
- Continuous operation with 30-minute intervals
- Average current: ~50mA during transmission, ~10mA idle

#### Xenon (Sleep Mode)
- Deep sleep between readings
- Sleep current: ~10µA
- Wake-up current: ~50mA during transmission
- Average current: ~2mA (with 12-hour sleep intervals)

### Integration with Particle Dashboard

The firmware is designed to work with the Particle Cloud Dashboard:
1. Create a new dashboard in the Particle Console
2. Add widgets for `plantStatus_analog` and `plantStatus_percentage`
3. Configure data visualization (line charts, gauges)
4. Set up automation rules for low moisture alerts

### Integration with Magic Mirror Module

For home automation integration, the [Magic Mirror Module](https://github.com/NickEngmann/MMM-ParticleStatus) can display plant moisture data on a smart mirror using the Particle API.

### Troubleshooting

#### Sensor Readings Seem Incorrect
- Check sensor calibration (soil composition affects readings)
- Ensure proper sensor placement in soil
- Verify analog pin connections

#### Device Not Publishing Data
- Check WiFi connection (Argon) or cellular connection (Xenon)
- Verify device is registered to your Particle account
- Check LED status indicator

#### Xenon Not Sleeping Properly
- Verify D1 wake-up pin is connected correctly
- Check battery voltage (BATT pin monitoring)
- Ensure sleep interval is within valid range (1-43200 seconds)

### License

MIT License - See LICENSE file for details.

### Contributors

- Nick Engmann - Original author
- Community contributors

🌱🌱🌱

# In-Plants Firmware

IoT firmware for Particle Mesh devices (Argon/Xenon) that monitors houseplant humidity using capacitive moisture sensors.

## Hardware Requirements

- Particle Argon or Xenon device
- Capacitive moisture sensor (connected to analog pin A1)
- For Xenon: D1 pin for wake-up, BATT pin for battery monitoring
- LED indicator on board LED pin (D7) for status feedback

## Firmware Variants

### Argon Variant (inplants-argon.ino)
- Publishes moisture sensor data every 30 seconds
- Reads capacitive moisture sensor on pin A1
- LED blinks 3 times during startup to verify functionality
- Uses USB power (no battery sleep mode)

### Xenon Variant (inplants-xenon.ino)
- Battery-powered operation with sleep mode
- Publishes moisture data when battery detected (BATT > 1)
- Sleeps for 12 hours (43200 seconds) between readings on D1 wake-up
- Publishes voltage readings when connected to USB power
- LED status indicator on board LED (D7)

## Data Publishing

The firmware publishes the following events to the Particle Cloud:

| Event Name | Description | Units |
|------------|-------------|-------|
| plantStatus_analog | Raw analog sensor reading | 0-4095 |
| plantStatus_percentage | Calculated moisture percentage | 0-100% |
| plantStatus_voltage | Battery voltage (Xenon only) | Volts |

### Moisture Calculation

Moisture percentage is calculated using the formula:
```
moisture_percentage = 100 - ((analog_reading / 4095.0) * 100)
```

This inverts the analog reading since higher moisture = lower resistance = higher analog value.

### Voltage Calculation (Xenon)

Voltage is calculated from the battery pin reading:
```
voltage = analogRead(BATT) * 0.0011224
```

## Pin Mappings

| Pin | Function | Variant |
|-----|----------|--------|
| A1 | Capacitive moisture sensor | Both |
| D7 | LED status indicator | Both |
| D1 | Wake-up pin (sleep mode) | Xenon only |
| BATT | Battery monitoring | Xenon only |

## Setup Instructions

1. Connect the capacitive moisture sensor to analog pin A1
2. Upload the appropriate firmware (Argon or Xenon variant)
3. Monitor sensor data via the Particle Console or integrate with your dashboard
4. For Xenon: ensure D1 is connected to a button or sensor for wake-up functionality

## Troubleshooting

- LED not blinking during startup: Check LED connection or firmware upload
- No sensor readings: Verify moisture sensor is connected to A1 and powered
- Xenon not waking up: Ensure D1 wake-up circuit is properly configured
- Inaccurate readings: Calibrate sensor in dry and wet conditions

## License

MIT License - See LICENSE file for details

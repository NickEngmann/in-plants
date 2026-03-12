#ifndef PLANT_SENSOR_H
#define PLANT_SENSOR_H

// Configuration constants
#ifndef NATIVE_BUILD
#include <Particle.h>
#endif

// Pin definitions
#define DEFAULT_MOISTURE_PIN A1
#define DEFAULT_BOARD_LED D7

// Native build definitions
#define D1 1
#define RISING 1

// Moisture sensor configuration
#define ANALOG_MAX 4095.00
#define MOISTURE_SCALE_FACTOR 0.0011224

// Sleep configuration for Xenon
#define SLEEP_INTERVAL_SECONDS 43200
#define SLEEP_PIN D1
#define SLEEP_MODE RISING

// Battery detection threshold
#define BATTERY_THRESHOLD 1

/**
 * Calculate moisture percentage from analog reading
 * @param analog_value Raw analog reading from sensor (0-4095)
 * @return Moisture percentage (0-100)
 */
float calculate_moisture_percentage(int analog_value);

/**
 * Calculate voltage from battery analog reading
 * @param analog_value Raw analog reading from battery pin
 * @return Voltage in volts
 */
float calculate_battery_voltage(int analog_value);

/**
 * Check if battery is connected based on analog reading
 * @param analog_value Raw analog reading from battery pin
 * @return true if battery is connected (value > 1), false otherwise
 */
bool is_battery_connected(int analog_value);

/**
 * Get sleep interval in seconds for Xenon device
 * @return Sleep interval in seconds
 */
int get_sleep_interval();

/**
 * Get sleep pin for Xenon device
 * @return Sleep pin number
 */
int get_sleep_pin();

/**
 * Get sleep mode for Xenon device
 * @return Sleep mode (RISING)
 */
int get_sleep_mode();

#endif // PLANT_SENSOR_H

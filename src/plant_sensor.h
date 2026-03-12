#ifndef PLANT_SENSOR_H
#define PLANT_SENSOR_H

#ifdef __cplusplus
extern "C" {
#endif

#include <stdint.h>

// Sensor types supported by the in-plants system
typedef enum {
    SENSOR_TYPE_MOISTURE_CAPACITIVE = 0,
    SENSOR_TYPE_TEMPERATURE,
    SENSOR_TYPE_LIGHT
} sensor_type_t;

// Moisture sensor data structure
typedef struct {
    uint16_t analog_value;      // Raw analog reading (0-4095 for Particle boards)
    float percentage;           // Calculated moisture percentage (0-100)
    int16_t temperature_c;      // Temperature in Celsius (if available)
    uint16_t light_lux;         // Light level in lux (if available)
    uint32_t timestamp;         // Unix timestamp of reading
} moisture_reading_t;

// Plant sensor interface
typedef struct {
    int pin;                    // GPIO pin for sensor
    sensor_type_t type;
    uint16_t min_value;         // Minimum analog value (dry)
    uint16_t max_value;         // Maximum analog value (wet)
    float calibration_offset;   // Calibration offset for percentage calculation
} plant_sensor_t;

// Sensor functions
void plant_sensor_init(plant_sensor_t* sensor, int pin, sensor_type_t type);
moisture_reading_t plant_sensor_read(plant_sensor_t* sensor);
float calculate_moisture_percentage(uint16_t analog_value, plant_sensor_t* sensor);
void plant_sensor_calibrate(plant_sensor_t* sensor, uint16_t dry_value, uint16_t wet_value);

#ifdef __cplusplus
}
#endif

#endif // PLANT_SENSOR_H

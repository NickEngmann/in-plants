#include "plant_sensor.h"
#include <math.h>

// Initialize a plant sensor with given pin and type
void plant_sensor_init(plant_sensor_t* sensor, int pin, sensor_type_t type) {
    if (sensor == NULL) return;
    
    sensor->pin = pin;
    sensor->type = type;
    sensor->min_value = 100;    // Default dry value (capacitive sensor)
    sensor->max_value = 3500;   // Default wet value (capacitive sensor)
    sensor->calibration_offset = 0.0f;
}

// Calculate moisture percentage from analog reading using linear interpolation
float calculate_moisture_percentage(uint16_t analog_value, plant_sensor_t* sensor) {
    if (sensor == NULL) return 0.0f;
    if (sensor->max_value == sensor->min_value) return 0.0f;
    
    // Clamp value to valid range
    if (analog_value < sensor->min_value) analog_value = sensor->min_value;
    if (analog_value > sensor->max_value) analog_value = sensor->max_value;
    
    // Linear interpolation: percentage = (value - min) / (max - min) * 100
    float range = (float)(sensor->max_value - sensor->min_value);
    float normalized = (float)(analog_value - sensor->min_value) / range;
    
    // Apply calibration offset
    normalized += sensor->calibration_offset;
    if (normalized < 0.0f) normalized = 0.0f;
    if (normalized > 1.0f) normalized = 1.0f;
    
    return normalized * 100.0f;
}

// Read sensor and return moisture data
moisture_reading_t plant_sensor_read(plant_sensor_t* sensor) {
    moisture_reading_t reading = {0};
    
    if (sensor == NULL || sensor->pin < 0) {
        return reading;
    }
    
    // In native build, simulate analog reading
    #ifdef NATIVE_BUILD
    // Simulate a moderate moisture reading (50%)
    reading.analog_value = (sensor->min_value + sensor->max_value) / 2;
    #else
    // Real hardware: read analog pin
    reading.analog_value = analogRead(sensor->pin);
    #endif
    
    reading.percentage = calculate_moisture_percentage(reading.analog_value, sensor);
    reading.temperature_c = -1;  // Not available on capacitive moisture sensor
    reading.light_lux = 0;       // Not available on capacitive moisture sensor
    reading.timestamp = 0;       // Would be set in real implementation
    
    return reading;
}

// Calibrate sensor with actual dry and wet values
void plant_sensor_calibrate(plant_sensor_t* sensor, uint16_t dry_value, uint16_t wet_value) {
    if (sensor == NULL) return;
    
    if (dry_value < wet_value) {
        sensor->min_value = dry_value;
        sensor->max_value = wet_value;
    }
}

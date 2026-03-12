#ifndef PLANT_SENSOR_H
#define PLANT_SENSOR_H

// Constants
#define ANALOG_MAX 4095
#define BATTERY_PIN D7
#define MOISTURE_PIN D6
#define SLEEP_PIN D4
#define SLEEP_INTERVAL_SECONDS 300
#define SLEEP_MODE 1

// Function declarations
float calculate_moisture_percentage(int analog_value);
float calculate_battery_voltage(int analog_value);
int get_sleep_interval();
int get_sleep_pin();
int get_sleep_mode();

#endif // PLANT_SENSOR_H

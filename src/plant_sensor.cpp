#include "plant_sensor.h"

float calculate_moisture_percentage(int analog_value) {
    return (100.0 - ((static_cast<float>(analog_value) / ANALOG_MAX) * 100.0));
}

float calculate_battery_voltage(int analog_value) {
    return static_cast<float>(analog_value) * MOISTURE_SCALE_FACTOR;
}

bool is_battery_connected(int analog_value) {
    return analog_value > BATTERY_THRESHOLD;
}

int get_sleep_interval() {
    return SLEEP_INTERVAL_SECONDS;
}

int get_sleep_pin() {
    return SLEEP_PIN;
}

int get_sleep_mode() {
    return SLEEP_MODE;
}

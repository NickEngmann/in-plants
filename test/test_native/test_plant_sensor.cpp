#include "plant_sensor.h"
#include <unity.h>
#include <cmath>
#include <cstring>

void setUp(void) {
    // Setup before each test
}

void tearDown(void) {
    // Cleanup after each test
}

void test_sensor_init(void) {
    plant_sensor_t sensor;
    plant_sensor_init(&sensor, A0, SENSOR_TYPE_MOISTURE_CAPACITIVE);
    
    TEST_ASSERT_EQUAL(0, sensor.pin);
    TEST_ASSERT_EQUAL(SENSOR_TYPE_MOISTURE_CAPACITIVE, sensor.type);
    TEST_ASSERT_EQUAL_UINT16(100, sensor.min_value);
    TEST_ASSERT_EQUAL_UINT16(3500, sensor.max_value);
    TEST_ASSERT_FLOAT_WITHIN(0.001f, 0.0f, sensor.calibration_offset);
}

void test_sensor_init_null_pointer(void) {
    plant_sensor_init(NULL, A0, SENSOR_TYPE_MOISTURE_CAPACITIVE);
    // Should not crash
    TEST_ASSERT_TRUE(true);
}

void test_calculate_moisture_percentage_min_value(void) {
    plant_sensor_t sensor;
    plant_sensor_init(&sensor, A0, SENSOR_TYPE_MOISTURE_CAPACITIVE);
    
    float percentage = calculate_moisture_percentage(100, &sensor);
    TEST_ASSERT_FLOAT_WITHIN(0.1f, 0.0f, percentage);
}

void test_calculate_moisture_percentage_max_value(void) {
    plant_sensor_t sensor;
    plant_sensor_init(&sensor, A0, SENSOR_TYPE_MOISTURE_CAPACITIVE);
    
    float percentage = calculate_moisture_percentage(3500, &sensor);
    TEST_ASSERT_FLOAT_WITHIN(0.1f, 100.0f, percentage);
}

void test_calculate_moisture_percentage_mid_value(void) {
    plant_sensor_t sensor;
    plant_sensor_init(&sensor, A0, SENSOR_TYPE_MOISTURE_CAPACITIVE);
    
    // Midpoint between 100 and 3500 is 1800
    float percentage = calculate_moisture_percentage(1800, &sensor);
    TEST_ASSERT_FLOAT_WITHIN(0.1f, 50.0f, percentage);
}

void test_calculate_moisture_percentage_clamping_low(void) {
    plant_sensor_t sensor;
    plant_sensor_init(&sensor, A0, SENSOR_TYPE_MOISTURE_CAPACITIVE);
    
    float percentage = calculate_moisture_percentage(0, &sensor);
    TEST_ASSERT_FLOAT_WITHIN(0.1f, 0.0f, percentage);
}

void test_calculate_moisture_percentage_clamping_high(void) {
    plant_sensor_t sensor;
    plant_sensor_init(&sensor, A0, SENSOR_TYPE_MOISTURE_CAPACITIVE);
    
    float percentage = calculate_moisture_percentage(5000, &sensor);
    TEST_ASSERT_FLOAT_WITHIN(0.1f, 100.0f, percentage);
}

void test_calculate_moisture_percentage_with_calibration(void) {
    plant_sensor_t sensor;
    plant_sensor_init(&sensor, A0, SENSOR_TYPE_MOISTURE_CAPACITIVE);
    sensor.calibration_offset = 0.1f;  // 10% offset
    
    float percentage = calculate_moisture_percentage(1800, &sensor);
    TEST_ASSERT_FLOAT_WITHIN(0.1f, 60.0f, percentage);
}

void test_calculate_moisture_percentage_null_sensor(void) {
    float percentage = calculate_moisture_percentage(1000, NULL);
    TEST_ASSERT_FLOAT_WITHIN(0.1f, 0.0f, percentage);
}

void test_calculate_moisture_percentage_equal_min_max(void) {
    plant_sensor_t sensor;
    plant_sensor_init(&sensor, A0, SENSOR_TYPE_MOISTURE_CAPACITIVE);
    sensor.min_value = 100;
    sensor.max_value = 100;  // Equal values
    
    float percentage = calculate_moisture_percentage(100, &sensor);
    TEST_ASSERT_FLOAT_WITHIN(0.1f, 0.0f, percentage);
}

void test_read_sensor_native_build(void) {
    plant_sensor_t sensor;
    plant_sensor_init(&sensor, A0, SENSOR_TYPE_MOISTURE_CAPACITIVE);
    
    moisture_reading_t reading = plant_sensor_read(&sensor);
    
    TEST_ASSERT_NOT_NULL(reading.analog_value);
    TEST_ASSERT_GREATER_OR_EQUAL(0, reading.percentage);
    TEST_ASSERT_LESS_OR_EQUAL(100, reading.percentage);
    TEST_ASSERT_EQUAL_INT(-1, reading.temperature_c);
    TEST_ASSERT_EQUAL_UINT16(0, reading.light_lux);
}

void test_read_sensor_null_sensor(void) {
    moisture_reading_t reading = plant_sensor_read(NULL);
    
    TEST_ASSERT_EQUAL_UINT16(0, reading.analog_value);
    TEST_ASSERT_FLOAT_WITHIN(0.1f, 0.0f, reading.percentage);
}

void test_calibrate_sensor(void) {
    plant_sensor_t sensor;
    plant_sensor_init(&sensor, A0, SENSOR_TYPE_MOISTURE_CAPACITIVE);
    
    plant_sensor_calibrate(&sensor, 50, 4000);
    
    TEST_ASSERT_EQUAL_UINT16(50, sensor.min_value);
    TEST_ASSERT_EQUAL_UINT16(4000, sensor.max_value);
}

void test_calibrate_sensor_invalid_values(void) {
    plant_sensor_t sensor;
    plant_sensor_init(&sensor, A0, SENSOR_TYPE_MOISTURE_CAPACITIVE);
    
    // dry_value > wet_value should not change values
    plant_sensor_calibrate(&sensor, 500, 100);
    
    TEST_ASSERT_EQUAL_UINT16(100, sensor.min_value);
    TEST_ASSERT_EQUAL_UINT16(3500, sensor.max_value);
}

void test_calibrate_sensor_null_pointer(void) {
    plant_sensor_calibrate(NULL, 100, 3500);
    // Should not crash
    TEST_ASSERT_TRUE(true);
}

int main(void) {
    UNITY_BEGIN();
    
    RUN_TEST(test_sensor_init);
    RUN_TEST(test_sensor_init_null_pointer);
    RUN_TEST(test_calculate_moisture_percentage_min_value);
    RUN_TEST(test_calculate_moisture_percentage_max_value);
    RUN_TEST(test_calculate_moisture_percentage_mid_value);
    RUN_TEST(test_calculate_moisture_percentage_clamping_low);
    RUN_TEST(test_calculate_moisture_percentage_clamping_high);
    RUN_TEST(test_calculate_moisture_percentage_with_calibration);
    RUN_TEST(test_calculate_moisture_percentage_null_sensor);
    RUN_TEST(test_calculate_moisture_percentage_equal_min_max);
    RUN_TEST(test_read_sensor_native_build);
    RUN_TEST(test_read_sensor_null_sensor);
    RUN_TEST(test_calibrate_sensor);
    RUN_TEST(test_calibrate_sensor_invalid_values);
    RUN_TEST(test_calibrate_sensor_null_pointer);
    
    return UNITY_END();
}

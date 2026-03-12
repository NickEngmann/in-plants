#include <unity.h>
#include "plant_sensor.h"

void setUp(void) {
    // Setup for each test
}

void tearDown(void) {
    // Teardown for each test
}

// Test moisture percentage calculation with zero analog value (dry soil)
void test_moisture_percentage_zero_analog(void) {
    float result = calculate_moisture_percentage(0);
    TEST_ASSERT_FLOAT_WITHIN(0.01f, 100.0f, result);
}

// Test moisture percentage calculation with max analog value (wet soil)
void test_moisture_percentage_max_analog(void) {
    float result = calculate_moisture_percentage(4095);
    TEST_ASSERT_FLOAT_WITHIN(0.01f, 0.0f, result);
}

// Test moisture percentage calculation with mid-range analog value
void test_moisture_percentage_mid_analog(void) {
    float result = calculate_moisture_percentage(2047);
    TEST_ASSERT_FLOAT_WITHIN(0.02f, 50.0f, result);
}

// Test moisture percentage calculation with quarter analog value
void test_moisture_percentage_quarter_analog(void) {
    float result = calculate_moisture_percentage(1023);
    TEST_ASSERT_FLOAT_WITHIN(0.02f, 75.0f, result);
}

// Test moisture percentage calculation with three-quarter analog value
void test_moisture_percentage_three_quarter_analog(void) {
    float result = calculate_moisture_percentage(3071);
    TEST_ASSERT_FLOAT_WITHIN(0.01f, 25.0f, result);
}

// Test battery voltage calculation with zero analog value
void test_battery_voltage_zero(void) {
    float result = calculate_battery_voltage(0);
    TEST_ASSERT_FLOAT_WITHIN(0.001f, 0.0f, result);
}

// Test battery voltage calculation with typical analog value
void test_battery_voltage_typical(void) {
    float result = calculate_battery_voltage(1000);
    TEST_ASSERT_FLOAT_WITHIN(0.001f, 1.122f, result);
}

// Test battery voltage calculation with max analog value
void test_battery_voltage_max(void) {
    float result = calculate_battery_voltage(4095);
    TEST_ASSERT_FLOAT_WITHIN(0.01f, 4.606f, result);
}

// Test battery connected with value > 1
void test_battery_connected(void) {
    TEST_ASSERT_TRUE(is_battery_connected(2));
    TEST_ASSERT_TRUE(is_battery_connected(100));
    TEST_ASSERT_TRUE(is_battery_connected(4095));
}

// Test battery disconnected with value <= 1
void test_battery_disconnected(void) {
    TEST_ASSERT_FALSE(is_battery_connected(0));
    TEST_ASSERT_FALSE(is_battery_connected(1));
}

// Test battery boundary condition
void test_battery_boundary(void) {
    TEST_ASSERT_FALSE(is_battery_connected(1));
    TEST_ASSERT_TRUE(is_battery_connected(2));
}

// Test battery boundary plus one
void test_battery_boundary_plus_one(void) {
    TEST_ASSERT_TRUE(is_battery_connected(2));
    TEST_ASSERT_TRUE(is_battery_connected(3));
}

// Test sleep interval configuration
void test_sleep_interval(void) {
    TEST_ASSERT_EQUAL_INT(SLEEP_INTERVAL_SECONDS, get_sleep_interval());
}

// Test sleep pin configuration
void test_sleep_pin(void) {
    TEST_ASSERT_EQUAL_INT(SLEEP_PIN, get_sleep_pin());
}

// Test sleep mode configuration
void test_sleep_mode(void) {
    TEST_ASSERT_EQUAL_INT(SLEEP_MODE, get_sleep_mode());
}

// Test moisture calculation edge cases
void test_moisture_edge_cases(void) {
    // Zero should give 100%
    TEST_ASSERT_FLOAT_WITHIN(0.01f, 100.0f, calculate_moisture_percentage(0));
    // Max should give 0%
    TEST_ASSERT_FLOAT_WITHIN(0.01f, 0.0f, calculate_moisture_percentage(4095));
    // Half should give 50%
    TEST_ASSERT_FLOAT_WITHIN(0.01f, 50.0f, calculate_moisture_percentage(2047));
}

int main(void) {
    UNITY_BEGIN();
    
    RUN_TEST(test_moisture_percentage_zero_analog);
    RUN_TEST(test_moisture_percentage_max_analog);
    RUN_TEST(test_moisture_percentage_mid_analog);
    RUN_TEST(test_moisture_percentage_quarter_analog);
    RUN_TEST(test_moisture_percentage_three_quarter_analog);
    RUN_TEST(test_battery_voltage_zero);
    RUN_TEST(test_battery_voltage_typical);
    RUN_TEST(test_battery_voltage_max);
    RUN_TEST(test_battery_connected);
    RUN_TEST(test_battery_disconnected);
    RUN_TEST(test_battery_boundary);
    RUN_TEST(test_battery_boundary_plus_one);
    RUN_TEST(test_sleep_interval);
    RUN_TEST(test_sleep_pin);
    RUN_TEST(test_sleep_mode);
    RUN_TEST(test_moisture_edge_cases);
    
    return UNITY_END();
}

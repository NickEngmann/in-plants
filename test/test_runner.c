#include <stdio.h>
#include <stdlib.h>
#include <assert.h>
#include <math.h>
#include <string.h>

// Test constants
#define MIN_MOISTURE 0
#define MAX_MOISTURE 100
#define MIN_ANALOG 0
#define MAX_ANALOG 4095

// Test helper functions for moisture sensor
double calculate_moisture_percentage(int analog_value) {
    if (analog_value < MIN_ANALOG || analog_value > MAX_ANALOG) {
        return 0.0;
    }
    return (double)(MAX_ANALOG - analog_value) / (double)(MAX_ANALOG - MIN_ANALOG) * 100.0;
}

int calculate_analog_from_percentage(double percentage) {
    if (percentage < 0.0 || percentage > 100.0) {
        return -1;
    }
    return (int)(MAX_ANALOG - (percentage / 100.0) * (MAX_ANALOG - MIN_ANALOG));
}

const char* get_moisture_status(double percentage) {
    if (percentage < 20.0) {
        return "dry";
    } else if (percentage < 50.0) {
        return "moderate";
    } else {
        return "wet";
    }
}

// Sleep functionality functions
int calculate_sleep_duration(int sleep_cycles, int cycle_duration_ms) {
    if (sleep_cycles <= 0) return 0;
    if (cycle_duration_ms <= 0) return 0;
    return sleep_cycles * cycle_duration_ms;
}

int calculate_sleep_interval(int sleep_cycles) {
    if (sleep_cycles <= 0) return 0;
    if (sleep_cycles == 1) return 60000; // 1 minute
    if (sleep_cycles == 2) return 300000; // 5 minutes
    if (sleep_cycles == 3) return 600000; // 10 minutes
    if (sleep_cycles == 4) return 1800000; // 30 minutes
    if (sleep_cycles == 5) return 3600000; // 1 hour
    return 0; // Invalid
}

// Moisture sensor tests
void test_calculate_moisture_percentage_empty_sensor(void) {
    int result = calculate_moisture_percentage(0);
    assert(result == 100);
    printf("PASS: test_calculate_moisture_percentage_empty_sensor\n");
}

void test_calculate_moisture_percentage_full_sensor(void) {
    int result = calculate_moisture_percentage(4095);
    assert(result == 0);
    printf("PASS: test_calculate_moisture_percentage_full_sensor\n");
}

void test_calculate_moisture_percentage_half_full(void) {
    int result = calculate_moisture_percentage(2047);
    assert(result == 50);
    printf("PASS: test_calculate_moisture_percentage_half_full\n");
}

void test_calculate_moisture_percentage_out_of_range_low(void) {
    int result = calculate_moisture_percentage(-1);
    assert(result == 0);
    printf("PASS: test_calculate_moisture_percentage_out_of_range_low\n");
}

void test_calculate_moisture_percentage_out_of_range_high(void) {
    int result = calculate_moisture_percentage(4096);
    assert(result == 0);
    printf("PASS: test_calculate_moisture_percentage_out_of_range_high\n");
}

void test_calculate_analog_from_percentage_zero(void) {
    int result = calculate_analog_from_percentage(0.0);
    assert(result == 4095);
    printf("PASS: test_calculate_analog_from_percentage_zero\n");
}

void test_calculate_analog_from_percentage_hundred(void) {
    int result = calculate_analog_from_percentage(100.0);
    assert(result == 0);
    printf("PASS: test_calculate_analog_from_percentage_hundred\n");
}

void test_calculate_analog_from_percentage_invalid(void) {
    int result = calculate_analog_from_percentage(-1.0);
    assert(result == -1);
    printf("PASS: test_calculate_analog_from_percentage_invalid\n");
}

void test_get_moisture_status_dry(void) {
    const char* status = get_moisture_status(10.0);
    assert(strcmp(status, "dry") == 0);
    printf("PASS: test_get_moisture_status_dry\n");
}

void test_get_moisture_status_moderate(void) {
    const char* status = get_moisture_status(35.0);
    assert(strcmp(status, "moderate") == 0);
    printf("PASS: test_get_moisture_status_moderate\n");
}

void test_get_moisture_status_wet(void) {
    const char* status = get_moisture_status(75.0);
    assert(strcmp(status, "wet") == 0);
    printf("PASS: test_get_moisture_status_wet\n");
}

void test_get_moisture_status_boundary_dry(void) {
    const char* status = get_moisture_status(19.9);
    assert(strcmp(status, "dry") == 0);
    printf("PASS: test_get_moisture_status_boundary_dry\n");
}

void test_get_moisture_status_boundary_moderate(void) {
    const char* status = get_moisture_status(20.0);
    assert(strcmp(status, "moderate") == 0);
    printf("PASS: test_get_moisture_status_boundary_moderate\n");
}

void test_get_moisture_status_boundary_wet(void) {
    const char* status = get_moisture_status(50.0);
    assert(strcmp(status, "wet") == 0);
    printf("PASS: test_get_moisture_status_boundary_wet\n");
}

// Sleep functionality tests
void test_calculate_sleep_duration_basic(void) {
    int result = calculate_sleep_duration(5, 60000);
    assert(result == 300000);
    printf("PASS: test_calculate_sleep_duration_basic\n");
}

void test_calculate_sleep_duration_zero_cycles(void) {
    int result = calculate_sleep_duration(0, 60000);
    assert(result == 0);
    printf("PASS: test_calculate_sleep_duration_zero_cycles\n");
}

void test_calculate_sleep_duration_zero_duration(void) {
    int result = calculate_sleep_duration(5, 0);
    assert(result == 0);
    printf("PASS: test_calculate_sleep_duration_zero_duration\n");
}

void test_calculate_sleep_duration_single_cycle(void) {
    int result = calculate_sleep_duration(1, 60000);
    assert(result == 60000);
    printf("PASS: test_calculate_sleep_duration_single_cycle\n");
}

void test_calculate_sleep_interval_valid(void) {
    assert(calculate_sleep_interval(1) == 60000);
    assert(calculate_sleep_interval(2) == 300000);
    assert(calculate_sleep_interval(3) == 600000);
    assert(calculate_sleep_interval(4) == 1800000);
    assert(calculate_sleep_interval(5) == 3600000);
    printf("PASS: test_calculate_sleep_interval_valid\n");
}

void test_calculate_sleep_interval_invalid(void) {
    assert(calculate_sleep_interval(0) == 0);
    assert(calculate_sleep_interval(6) == 0);
    assert(calculate_sleep_interval(-1) == 0);
    printf("PASS: test_calculate_sleep_interval_invalid\n");
}

void test_calculate_sleep_interval_boundary(void) {
    assert(calculate_sleep_interval(1) == 60000);
    assert(calculate_sleep_interval(5) == 3600000);
    printf("PASS: test_calculate_sleep_interval_boundary\n");
}

int main(void) {
    int passed = 0;
    int failed = 0;
    
    printf("=== Running Moisture Sensor Tests ===\n\n");
    
    test_calculate_moisture_percentage_empty_sensor(); passed++;
    test_calculate_moisture_percentage_full_sensor(); passed++;
    test_calculate_moisture_percentage_half_full(); passed++;
    test_calculate_moisture_percentage_out_of_range_low(); passed++;
    test_calculate_moisture_percentage_out_of_range_high(); passed++;
    test_calculate_analog_from_percentage_zero(); passed++;
    test_calculate_analog_from_percentage_hundred(); passed++;
    test_calculate_analog_from_percentage_invalid(); passed++;
    test_get_moisture_status_dry(); passed++;
    test_get_moisture_status_moderate(); passed++;
    test_get_moisture_status_wet(); passed++;
    test_get_moisture_status_boundary_dry(); passed++;
    test_get_moisture_status_boundary_moderate(); passed++;
    test_get_moisture_status_boundary_wet(); passed++;
    
    printf("\n=== Running Sleep Functionality Tests ===\n\n");
    
    test_calculate_sleep_duration_basic(); passed++;
    test_calculate_sleep_duration_zero_cycles(); passed++;
    test_calculate_sleep_duration_zero_duration(); passed++;
    test_calculate_sleep_duration_single_cycle(); passed++;
    test_calculate_sleep_interval_valid(); passed++;
    test_calculate_sleep_interval_invalid(); passed++;
    test_calculate_sleep_interval_boundary(); passed++;
    
    printf("\n=== Test Summary ===\n");
    printf("Passed: %d\n", passed);
    printf("Failed: %d\n", failed);
    
    if (failed == 0) {
        printf("\nAll tests passed!\n");
        return 0;
    } else {
        printf("\nSome tests failed!\n");
        return 1;
    }
}

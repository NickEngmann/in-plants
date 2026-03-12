#include <iostream>
#include <cmath>
#include <cassert>
#include <string>

// Arduino-style constants for testing
#define LOW 0
#define HIGH 1

// Mock hardware abstraction layer for testing
namespace MockHardware {
    int boardLedState = LOW;
    int moistureAnalogValue = 2048;
    int batteryLevel = 2;
    int sleepPin = 1;
    int sleepMode = 0;
    int sleepDuration = 0;
    
    void digitalWrite(int pin, int value) {
        boardLedState = value;
    }
    
    int analogRead(const std::string& pin) {
        if (pin == "BATT") {
            return batteryLevel * 4095 / 10;
        }
        return moistureAnalogValue;
    }
    
    void System_sleep(int pin, int mode, int duration) {
        sleepPin = pin;
        sleepMode = mode;
        sleepDuration = duration;
    }
    
    void reset() {
        boardLedState = LOW;
        moistureAnalogValue = 2048;
        batteryLevel = 2;
        sleepPin = 0;
        sleepMode = 0;
        sleepDuration = 0;
    }
}

// Sensor logic functions extracted from the main code
float calculateMoisturePercentage(int analogValue) {
    return (100.0 - ((static_cast<float>(analogValue) / 4095.00) * 100.0));
}

int calculateBatteryVoltage(int analogValue) {
    return static_cast<int>(analogValue * 0.0011224 * 1000); // Return in millivolts
}

// Test cases for sensor logic
void test_calculateMoisturePercentage_dry_soil() {
    // Dry soil = low analog reading = high percentage
    int dryAnalog = 100;
    float percentage = calculateMoisturePercentage(dryAnalog);
    assert(percentage > 95.0);
    std::cout << "✓ test_calculateMoisturePercentage_dry_soil passed" << std::endl;
}

void test_calculateMoisturePercentage_wet_soil() {
    // Wet soil = high analog reading = low percentage
    int wetAnalog = 4000;
    float percentage = calculateMoisturePercentage(wetAnalog);
    assert(percentage < 3.0);
    std::cout << "✓ test_calculateMoisturePercentage_wet_soil passed" << std::endl;
}

void test_calculateMoisturePercentage_medium_soil() {
    // Medium soil = ~50% moisture
    int mediumAnalog = 2048;
    float percentage = calculateMoisturePercentage(mediumAnalog);
    assert(percentage > 45.0 && percentage < 55.0);
    std::cout << "✓ test_calculateMoisturePercentage_medium_soil passed" << std::endl;
}

void test_calculateMoisturePercentage_extreme_wet() {
    // Maximum analog = 0% moisture reading
    int maxAnalog = 4095;
    float percentage = calculateMoisturePercentage(maxAnalog);
    assert(percentage == 0.0);
    std::cout << "✓ test_calculateMoisturePercentage_extreme_wet passed" << std::endl;
}

void test_calculateMoisturePercentage_extreme_dry() {
    // Minimum analog = 100% moisture reading
    int minAnalog = 0;
    float percentage = calculateMoisturePercentage(minAnalog);
    assert(percentage == 100.0);
    std::cout << "✓ test_calculateMoisturePercentage_extreme_dry passed" << std::endl;
}

void test_battery_voltage_calculation() {
    // Test battery voltage calculation
    int batteryAnalog = 1000;
    int voltage = calculateBatteryVoltage(batteryAnalog);
    assert(voltage > 1000 && voltage < 1200); // Should be around 1122mV
    std::cout << "✓ test_battery_voltage_calculation passed" << std::endl;
}

void test_sensor_range_boundary() {
    // Test boundary conditions
    for (int i = 0; i <= 4095; i += 1024) {
        float percentage = calculateMoisturePercentage(i);
        assert(percentage >= 0.0 && percentage <= 100.0);
    }
    std::cout << "✓ test_sensor_range_boundary passed" << std::endl;
}

int main() {
    std::cout << "Running sensor logic tests..." << std::endl;
    std::cout << "================================" << std::endl;
    
    test_calculateMoisturePercentage_dry_soil();
    test_calculateMoisturePercentage_wet_soil();
    test_calculateMoisturePercentage_medium_soil();
    test_calculateMoisturePercentage_extreme_wet();
    test_calculateMoisturePercentage_extreme_dry();
    test_battery_voltage_calculation();
    test_sensor_range_boundary();
    
    std::cout << "================================" << std::endl;
    std::cout << "All tests passed!" << std::endl;
    
    return 0;
}

#!/bin/bash
# Test script to validate README documentation

echo "Testing README documentation..."

# Check if README exists
if [ ! -f "README.md" ]; then
    echo "FAIL: README.md not found"
    exit 1
fi

# Check for firmware logic section
if grep -q "Firmware Logic" README.md; then
    echo "PASS: Firmware Logic section found"
else
    echo "FAIL: Firmware Logic section not found"
    exit 1
fi

# Check for sensor data formatting section
if grep -q "Sensor Data Formatting" README.md; then
    echo "PASS: Sensor Data Formatting section found"
else
    echo "FAIL: Sensor Data Formatting section not found"
    exit 1
fi

# Check for configuration constants section
if grep -q "Configuration Constants" README.md; then
    echo "PASS: Configuration Constants section found"
else
    echo "FAIL: Configuration Constants section not found"
    exit 1
fi

# Check for Argon firmware documentation
if grep -q "Argon Firmware" README.md; then
    echo "PASS: Argon Firmware documentation found"
else
    echo "FAIL: Argon Firmware documentation not found"
    exit 1
fi

# Check for Xenon firmware documentation
if grep -q "Xenon Firmware" README.md; then
    echo "PASS: Xenon Firmware documentation found"
else
    echo "FAIL: Xenon Firmware documentation not found"
    exit 1
fi

echo "All documentation tests passed!"
exit 0

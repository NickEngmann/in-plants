CC = gcc
CFLAGS = -Iinclude -I.pio/libdeps/native/Unity/src -std=c++17 -Wall -Wextra
LDFLAGS = -std=c++17

# Source files
SRC_DIR = src
TEST_DIR = test/test_native
UNITY_SRC = .pio/libdeps/native/Unity/src/unity.c

# Object files
SRC_OBJS = $(SRC_DIR)/plant_sensor.cpp
TEST_OBJS = $(TEST_DIR)/test_moisture.cpp

# Test executable
TEST_EXEC = test_runner

.PHONY: all clean test

all: $(TEST_EXEC)

$(TEST_EXEC): $(SRC_OBJS) $(TEST_OBJS) $(UNITY_SRC)
	$(CC) $(CFLAGS) $(LDFLAGS) -o $@ $(SRC_OBJS) $(TEST_OBJS) $(UNITY_SRC)

test: $(TEST_EXEC)
	./$(TEST_EXEC)

clean:
	rm -f $(TEST_EXEC)
	rm -f *.o

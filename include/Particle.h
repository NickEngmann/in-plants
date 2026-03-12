// Mock Particle.h for testing
#ifndef PARTICLE_H
#define PARTICLE_H

#include <stdint.h>
#include <string>
#include <vector>
#include <functional>

// Mock Particle system
namespace Particle {
    class System {
    public:
        static void sleep(unsigned long seconds) {}
        static void sleep(unsigned long seconds, const std::string& mode) {}
        static bool isSleeping() { return false; }
        static unsigned long uptime() { return 0; }
    };
    
    class WiFi {
    public:
        static bool connected() { return true; }
        static void connect() {}
        static void disconnect() {}
    };
    
    class Cloud {
    public:
        static void connect() {}
        static void disconnect() {}
        static bool connected() { return true; }
        static void onEvent(const std::string& event, std::function<void(const std::string&, int)> callback) {}
        static void onVariable(const std::string& variable, std::function<std::string()> callback) {}
    };
    
    class Variable {
    public:
        static void publish(const std::string& name, const std::string& value) {}
        static void publish(const std::string& name, int value) {}
        static void publish(const std::string& name, float value) {}
    };
    
    class Event {
    public:
        static void on(const std::string& name, std::function<void(const std::string&)> callback) {}
    };
}

#define SYSTEM_MODE(AUTO) 0
#define SYSTEM_MODE(MANUAL) 1
#define SYSTEM_MODE(AUTOMATIC) 0

// Mock pin definitions
#define D0 0
#define D1 1
#define D2 2
#define D3 3
#define D4 4
#define D5 5
#define D6 6
#define D7 7
#define A0 14
#define A1 15
#define A2 16
#define A3 17
#define A4 18
#define A5 19
#define A6 20
#define A7 21
#define TX 22
#define RX 23
#define SCL 24
#define SDA 25
#define LED_RED 13
#define LED_GREEN 12
#define LED_BLUE 11

// Mock analog/digital functions
inline void pinMode(int pin, int mode) {}
inline void digitalWrite(int pin, int value) {}
inline int digitalRead(int pin) { return 0; }
inline int analogRead(int pin) { return 0; }
inline void analogWrite(int pin, int value) {}
inline float analogReadVoltage(int pin) { return 0.0f; }
inline void delay(unsigned long ms) {}
inline unsigned long millis() { return 0; }
inline unsigned long micros() { return 0; }

#endif // PARTICLE_H

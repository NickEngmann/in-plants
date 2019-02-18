// -----------------------------------------
// Publish Xenon data and Dashboard with Capacitive Moisture Sensors
// -----------------------------------------
// This app will publish an event every 30 seconds reporting the moisture sensor analog and percentage


// We start by declaring which pins everything is plugged into.

int boardLed = D7; // This is the LED that is already on your device.
// On the Core, it's the LED in the upper right hand corner.
// On the Photon, it's next to the D7 pin.

int moisture_pin = A1; // This is where your capacitive moisture sensor is plugged in.


// We start with the setup function.

void setup() {
  pinMode(boardLed,OUTPUT); // Our on-board LED is output as well
  pinMode(moisture_pin,INPUT);  // Our capacitive moisture sensor pin is input (reading the capacitive moisture sensor)


  // Just to make sure everything is workign we are going to toggle the LED on and then off really quickly 3x
  digitalWrite(boardLed,HIGH);
  delay(200);
  digitalWrite(boardLed,LOW);
  delay(200);

}


// Now for the loop.

void loop() {
    /* In this loop function, we're going to check to read the moisture sensor
    After a specified time period we'll send a Particle.publish() to the cloud.
    After Particle implements sleep capability we will also start placing the 
    device in sleep mode for various intervals in between reads.

    Currently the Particle Firmware doesn't support the "Sleep" functionality.
    The Sleep functionality allows the Particle Xenon/Argon to enter a low power 
    or very low power state. When this state is enabled it will allow the battery 
    life of the device to be exponentnailyl better. Unfortunately this update will
    be coming out in a later firmware update.
    */

    digitalWrite(boardLed,HIGH);
    // Now we'll take some readings...
    int moisture_analog = analogRead(moisture_pin); // read capacitive sensor
    float moisture_percentage = (100 - ( (moisture_analog/4095.00) * 100 ) );
    if(BATT){
        float voltage = analogRead(BATT) * 0.0011224;
        Particle.publish("plantStatus_voltage", String(voltage),60,PUBLIC);
    }
    delay(7000);
    // Send a publish to your devices...
    Particle.publish("plantStatus_analog", String(moisture_analog),60,PUBLIC);
    Particle.publish("plantStatus_percentage", String(moisture_percentage),60,PUBLIC);
    digitalWrite(boardLed,LOW);

    // System.sleep(30);
    delay(30000);
}

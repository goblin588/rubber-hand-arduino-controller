#include <Servo.h>

// Servo Motors
Servo ServoA;  
Servo ServoB;

// Pressure sensors pins
int SensorA = A1; //Middle Finger
int SensorB = A0; //Index Finger

//LED Pins
int LED_GREEN = 13;
int LED_RED = 12;

// Initial servo angles for finger position
int s1d = 150;
int s1u = 70;
int s2d = 180;
int s2u = 90;

void setup() {
  // Serial baud rate 
  Serial.begin(14400);
  //Set pin modes
  pinMode(SensorA, INPUT);
  pinMode(SensorB, INPUT);

  //Set and initialise Servos and DOWN
  ServoA.attach(10);
  ServoB.attach(11);
  ServoA.write(s1d);
  ServoB.write(s2d);

  //Initialise LED pins 
  pinMode(LED_GREEN, OUTPUT);
  pinMode(LED_RED, OUTPUT);
  
}

int readSensor(int sensorPin) {
  //Reads current value of a sensor
  return analogRead(sensorPin);
}

void led_on(int LED) {
  //Turns on LED 
  digitalWrite(LED, HIGH);
}

void led_off(int LED) {
  //Turns off LED
  digitalWrite(LED, LOW);
}

int runAngles = 1; 
void loop() {
  //This chunk was trying to get angles to be initialised from python - can delete 
  // int s1up;
  // int s1dw;
  // int s2up;
  // int s2dw;
  // int angles[4];

  // if(runAngles){
  //     //Retrieves angle values from python on startup
  //   int wait = 0;
  //   //Initial 'safe' angles
  //   while (wait){
  //     if (Serial.available()) {
  //       String serialData = Serial.readStringUntil('\n');
  //       if(serialData.length() > 2){
  //         // Parse and store angle values in the angles array
  //         char* token = strtok(const_cast<char*>(serialData.c_str()), ",");
  //         for (int i = 0; i < 4; i++) {
  //           angles[i] = atoi(token);
  //           token = strtok(NULL, ",");
  //         }
  //         wait = 1;
  //       }
  //     }
  //   }
  //   //Assign servo angles 
  //   s1up = angles[0];
  //   s1dw = angles[1];
  //   s2up = angles[2];
  //   s2dw = angles[3];

  //   runAngles = 0;
  // }

  //Check for serial available
  if (Serial.available()) {
    //Read command from python 
    if (String command = Serial.readStringUntil('\n')) {
      //Read Command returns current sensor readings of both A and B
      if (command == "read") {
        Serial.print(analogRead(SensorA));
        Serial.print(", ");
        Serial.println(analogRead(SensorB));
      }
      //Middle finger Up/Down commands
      if (command == "middle_up") {
        ServoA.write(s1u);
      }
      if (command == "middle_down") {
        ServoA.write(s1d);
      }
      //Middle finger LED commands
      if (command == "middle_led_on") {
        led_on(LED_GREEN);
      }
      if (command == "middle_led_off") {
        led_off(LED_GREEN);
      }
      //Index finger Up/Down commands 
      if (command == "index_up") {
        ServoB.write(s2u);
      }
      if (command == "index_down") {
        ServoB.write(s2d);
      }
      //Index finger LED commands
      if (command == "index_led_on") {
        led_on(LED_RED);
      }
      if (command == "index_led_off") {
        led_off(LED_RED);
      }
    }
  }
}

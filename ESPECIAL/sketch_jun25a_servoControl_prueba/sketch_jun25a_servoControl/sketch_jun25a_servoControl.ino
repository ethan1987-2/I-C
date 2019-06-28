/*
 Controlling a servo position using a potentiometer (variable resistor)
 by Michal Rinott <http://people.interaction-ivrea.it/m.rinott>

 modified on 8 Nov 2013
 by Scott Fitzgerald
 http://www.arduino.cc/en/Tutorial/Knob
*/
#include <Arduino.h>
#include <Servo.h>

Servo myservo;  // create servo object to control a servo


int pos;
int v=0;

void setup() {
  myservo.attach(9);  // attaches the servo on pin 9 to the servo object
}


void loop() {
myservo.writeMicroseconds(650);
delay(100);
//myservo.writeMicroseconds(1500);
//myservo.write(90);

}





// void loop() {
//  val = analogRead(potpin);            // reads the value of the potentiometer (value between 0 and 1023)

//  val = map(val, 0, 1023, 0, 180);     // scale it to use it with the servo (value between 0 and 180)
                   // sets the servo position according to the scaled value
  //myservo.write(5);  
  //delay(15);                           // waits for the servo to get there
 

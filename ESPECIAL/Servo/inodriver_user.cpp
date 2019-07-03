//// ****** THIS FILE IS AUTOGENERATED ******
////
////          >>>> PLEASE ADAPT IT TO YOUR NEEDS <<<<
////
/// 
///  Filename; E:\TOMAS_G\I-C\Arduino0.py
///  Source class: Servo
///  Generation timestamp: 2019-06-25T19:08:31.870850
///  Class code hash: cf4f85ed888f284b59884ff3ad75b9c079d5f6e9
///
/////////////////////////////////////////////////////////////

#include "inodriver_user.h"
#include <Arduino.h>
#include <Servo.h>

Servo myservo;  // create servo object to control a servo

void user_setup() {
  myservo.attach(9);  // attach servo to pin 9
}

void user_loop() {
}
// COMMAND: ANGLE, FEAT: angle
int set_ANGLE(float value) {
  int servo_value = value;
  myservo.writeMicroseconds(servo_value);
  //myservo.write(servo_value);                  // sets the servo position according to the input value
  delay(1000);                           // waits for the servo to get there
  //return 0;
};

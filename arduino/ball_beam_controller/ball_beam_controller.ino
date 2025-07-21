
#include <Servo.h>
Servo myservo;
const int servoPin=9;


void setup() {
  Serial.begin(9600);
  myservo.attach(servoPin);
  myservo.write(105);
  // put your setup code here, to run once:

}

void loop() {
  if (Serial.available()){
    String input = Serial.readStringUntil('\n');
    input.trim();
    Serial.print("Got: ");
    Serial.println(input);
    if (input.length()>0){
      int angle=input.toInt();
      angle=constrain(angle,65,150);
      myservo.write(angle);

    }
  }
  // put your main code here, to run repeatedly:

}

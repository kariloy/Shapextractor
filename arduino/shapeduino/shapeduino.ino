/*

 Controls the stepper motor, laser line module (and LED lights?) 
 via ULN2003 board for the Shapextractor 2
 
 Created by Kariloy "PPK" Markief
 
 */


#include <Stepper.h>


const int A  = 7;    //7;  // IN1
const int An = 4;    //6;  // IN2
const int B  = 5;    //5;  // IN3
const int Bn = 6;    //4;  // IN4


const int light = 9;

const int laser = 11;
// laser duty cycle/pwm val?
//const int val = 12;


//sets the Steps Per Rotation, in this case it is 64 * the 283712/4455 annoying ger ratio
//for my motor (it works with float to be able to deal with these non-integer gear ratios)

// the 28BYJ-48 stepper has 4075.7728395
// steps per revolution, hopefully the
// approximation will do just fine. 4076 vs 2048 steps?
// seems like it's actually 2048 or somewhere near (w/ the 
// step sequence from the standard arduino the library).
const int stepsPerRevolution = 2048;



//int stepCount = 0;         // number of steps the motor has taken
//int lastStep = 0;


String message = "";



// initialize the stepper library
Stepper myStepper(stepsPerRevolution, A,An,B,Bn);           

// =========================================================== //


void setup() {

  Serial.begin(57600);

  pinMode(laser, OUTPUT);
  pinMode(light, OUTPUT);
}


// =========================================================== //

void loop() {


  int i=0;
  char commandbuffer[100];

  if(Serial.available()){
    delay(100);
    while( Serial.available() && i< 99) {
      commandbuffer[i++] = Serial.read();
    }
    commandbuffer[i++]='\0';
  }

  if(i>0)
  {
    message = (char*)commandbuffer;
    message.toUpperCase();
  }


  // Move ONE step forward
  if(message == "S"){
    myStepper.step(1);
    message = "";
    //stepCount++;
  }

  // turn laser on/off -- pwm laser
  if(message == "I"){
    //digitalWrite(laser, HIGH);
    analogWrite(laser, 50);
    //analogWrite(laser, val);
    message = "";
  }
  if(message == "O"){
    digitalWrite(laser, LOW);
    message = "";
  }

  
  // Turn lights ON
  if(message == "L"){
    digitalWrite(laser, HIGH);
    message = "";
  }
  // Turn lights OFF
  if(message == "D"){
    digitalWrite(laser, LOW);
    message = "";
  }
  




  //  if (stepCount > lastStep){    
  //    Serial.println(stepCount);
  //    lastStep++;
  //  }


}


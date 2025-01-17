/*
 *  Application note: incremental encoder and RS422/RS485 Shield  
 *  Version 1.0
 *  Copyright (C) 2020  Hartmut Wendt  www.zihatec.de
 *  
 *  used encoder: SICK DFS60 www.sick.com
 *  
 *
 *  This program is free software: you can redistribute it and/or modify
 *  it under the terms of the GNU General Public License as published by
 *  the Free Software Foundation, either version 3 of the License, or
 *  (at your option) any later version.
 *
 *  This program is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU General Public License for more details.
 *
 *  You should have received a copy of the GNU General Public License
 *  along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/   

/*
Behavior of IRC sensor Sick "DFS60I-S4PM65536":

1) When ZeroPin connected to HIGH (disconnected = PULL UP as defined) -> encoders takes current position and sets it to zero
2) When rotation clockwise from 0 degrees to 180 degrees it returns value between <0; +65536/2= +32768>
3) When rotation counter-clockwise from 0 degrees to -180 degrees it returns value between <0; -65536/2= -32768>
4) To convert from returned value to degrees use following equation:

  Alpha = returnValue * 32768/180
  * where Alpha is current angle in degrees and returnValue is value returned from encoder (does not have any unit)

Hardware connection notes:
1) see pictures
2) use 2x RS485 moduls (physical layer compatible with RS422 used by IRC according to Readme in this github project)
3) RS485 bought from here "https://www.gme.cz/v/1507872/modul-sbernice-rs-485"
4) to be save it would be best to have 3 of them, but probably will not be needed


*/
// Pin definitions
const byte COSPin = 12;   // RS422 input for A channel (cos signal) 
const byte SINPin = 14;   // RS422 input for B channel (sin signal)  
const byte ZeroPin = 27;  // RS422 input for Z channel (zero detection)

// variables
enum {ENC_STOP, ENC_CLOCKWISE_ROTATION, ENC_COUNTERCLOCKWISE_ROTATION};  // encoder operation modes
volatile byte encoder_state = ENC_STOP;
volatile long encoder_position = 0; 
volatile long encoder_oldpos = 0; 


void setup() {
  Serial.begin(115200); //Use serial monitor for debugging
  delay(1000); //Give some time to establish the serial connection

  // Define pins for input and output
  pinMode(SINPin, INPUT);

  // set internal pullup resistor for interrupt pin
  pinMode(COSPin, INPUT_PULLUP);
  pinMode(ZeroPin, INPUT_PULLUP);
  
  
  // set 1st interrupt service routine to COSPin and 'RISING' edge 
  attachInterrupt(digitalPinToInterrupt(COSPin), encoder_isr, RISING);

  // set 2nd interrupt service routine to ZeroPin and 'HIGH' level 
  attachInterrupt(digitalPinToInterrupt(ZeroPin), zero_detection_isr, HIGH);
}


void loop() {
  // Detect Encoder Stop
  if (encoder_oldpos == encoder_position) encoder_state= ENC_STOP;

  // output encoder incremental and status
  //Serial.print("Encoder position: ");
  Serial.println(encoder_position*360.000/65536, 8);
  //Serial.print(", Encoder state: ");
  
  if (encoder_state==ENC_CLOCKWISE_ROTATION) {
    //Serial.println("Clockwise Rotation");
        
  } else if (encoder_state==ENC_COUNTERCLOCKWISE_ROTATION) {
    //Serial.println("Counter-Clockwise Rotation");
    
  } else {
    //Serial.println("Stop");  
  }
  
  encoder_oldpos = encoder_position;
  
  delay(50);
}


void encoder_isr() {
  
  if  (digitalRead(SINPin) == LOW) {
    // clockwise rotation
    encoder_state=ENC_CLOCKWISE_ROTATION;
    encoder_position++;
  } else {
    //counter-clockwise rotation
    encoder_state=ENC_COUNTERCLOCKWISE_ROTATION;
    encoder_position--;    
  } 
}


void zero_detection_isr() {
  // detect pulse on zero channel
  encoder_position = 0;
}

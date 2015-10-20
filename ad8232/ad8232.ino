/* This program control Sparkfun SEN-12650 with Arduino */

// See: AD8232 Heart Rate Monitor Hookup Guide
// https://learn.sparkfun.com/tutorials/ad8232-heart-rate-monitor-hookup-guide?_ga=1.202489809.1577254265.1443793022
// This code is from that tutorial

void setup() {
  // initialize the serial communication:
  Serial.begin(9600);
  pinMode(10, INPUT); // Setup for leads off detection LO +
  pinMode(11, INPUT); // Setup for leads off detection LO -
}

void loop() {
  
  if((digitalRead(10) == 1)||(digitalRead(11) == 1)){
    Serial.println('!');
  }
  else{
    // send the value of analog input 0:
      Serial.println(analogRead(A0));
  }
  //Wait for a bit to keep serial data from saturating
  delay(1);
}

String inputString = "";         // a string to hold incoming data
boolean stringComplete = false;  // whether the string is complete

int m13 = 13;
int m12 = 12;
int m11 = 11;
int m10 = 10;

int m09 = 9;
int m08 = 8;
int m07 = 7;
int m06 = 6;

int time01 = 10;
int time00 = 0;

void setup() {
  // initialize serial:
  Serial.begin(9600);
  // reserve 200 bytes for the inputString:
  inputString.reserve(200);
  pinMode(m13, OUTPUT); 
  pinMode(m12, OUTPUT);
  pinMode(m11, OUTPUT); 
  pinMode(m10, OUTPUT); 
  
  pinMode(m09, OUTPUT); 
  pinMode(m08, OUTPUT); 
  pinMode(m07, OUTPUT); 
  pinMode(m06, OUTPUT); 
  
}

void loop() {
  // print the string when a newline arrives:
  if (stringComplete) {
    if(inputString.startsWith("x")){
      //Serial.println(inputString);
        digitalWrite(m13, HIGH);   // turn the LED on (HIGH is the voltage level)
        delay(time01);               // wait for a second
        digitalWrite(m13, LOW);    // turn the LED off by making the voltage LOW
        delay(time00);               // wait for a second
        
        digitalWrite(m12, HIGH);   // turn the LED on (HIGH is the voltage level)
        delay(time01);               // wait for a second
        digitalWrite(m12, LOW);    // turn the LED off by making the voltage LOW
        delay(time00);               // wait for a second
        
        digitalWrite(m11, HIGH);   // turn the LED on (HIGH is the voltage level)
        delay(time01);               // wait for a second
        digitalWrite(m11, LOW);    // turn the LED off by making the voltage LOW
        delay(time00);               // wait for a second
        
        digitalWrite(m10, HIGH);   // turn the LED on (HIGH is the voltage level)
        delay(time01);               // wait for a second
        digitalWrite(m10, LOW);    // turn the LED off by making the voltage LOW
        delay(time00);               // wait for a second
    }
    else if(inputString.startsWith("y")){
      //Serial.println(inputString);
        digitalWrite(m09, HIGH);   // turn the LED on (HIGH is the voltage level)
        delay(time01);               // wait for a second
        digitalWrite(m09, LOW);    // turn the LED off by making the voltage LOW
        delay(time00);               // wait for a second
        
        digitalWrite(m08, HIGH);   // turn the LED on (HIGH is the voltage level)
        delay(time01);               // wait for a second
        digitalWrite(m08, LOW);    // turn the LED off by making the voltage LOW
        delay(time00);               // wait for a second
        
        digitalWrite(m07, HIGH);   // turn the LED on (HIGH is the voltage level)
        delay(time01);               // wait for a second
        digitalWrite(m07, LOW);    // turn the LED off by making the voltage LOW
        delay(time00);               // wait for a second
        
        digitalWrite(m06, HIGH);   // turn the LED on (HIGH is the voltage level)
        delay(time01);               // wait for a second
        digitalWrite(m06, LOW);    // turn the LED off by making the voltage LOW
        delay(time00);               // wait for a second
    }
    delay(50);
    // clear the string:
    inputString = "";
    stringComplete = false;
  }
}

/*
  SerialEvent occurs whenever a new data comes in the
 hardware serial RX.  This routine is run between each
 time loop() runs, so using delay inside loop can delay
 response.  Multiple bytes of data may be available.
 */
void serialEvent() {

    while (Serial.available()) {
    // get the new byte:
      char inChar = (char)Serial.read(); 
    // add it to the inputString:
      inputString += inChar;
    // if the incoming character is a newline, set a flag
    // so the main loop can do something about it:
      if (inChar == '|') {
        stringComplete = true;
      }

    }
}

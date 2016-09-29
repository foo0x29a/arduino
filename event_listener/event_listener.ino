#include <string.h>

String inputString = "";         // A string to hold incoming data
boolean stringComplete = false;  // Whether the string is complete

/* X axis */
int m_x_01 = 13;
int m_x_02 = 12;
int m_x_03 = 11;
int m_x_04 = 10;

/* Y axis */
int m_y_01 = 9;
int m_y_02 = 8;
int m_y_03 = 7;
int m_y_04 = 6;

int current_x = 0;
int current_y = 0;

const char SPACE_CHAR = ' ';

void setup() {
  Serial.begin(9600);         // Initialize serial
  inputString.reserve(200);   // Reserve 200 bytes for the inputString

  pinMode(m_x_01, OUTPUT);
  pinMode(m_x_02, OUTPUT);
  pinMode(m_x_03, OUTPUT);
  pinMode(m_x_04, OUTPUT);

  pinMode(m_y_01, OUTPUT);
  pinMode(m_y_02, OUTPUT);
  pinMode(m_y_03, OUTPUT);
  pinMode(m_y_04, OUTPUT);
}

void signal_and_sleep(int pin){
  digitalWrite(pin, HIGH);
  delay(10);
  digitalWrite(pin, LOW);
  delay(0);
}

void inc_x(){
  current_x++;
  signal_and_sleep(m_x_01);
  signal_and_sleep(m_x_02);
  signal_and_sleep(m_x_03);
  signal_and_sleep(m_x_04);
}

void inc_y(){
  current_y++;
  signal_and_sleep(m_y_01);
  signal_and_sleep(m_y_02);
  signal_and_sleep(m_y_03);
  signal_and_sleep(m_y_04);
}

void dec_x(){
  current_x--;
  signal_and_sleep(m_x_04);
  signal_and_sleep(m_x_03);
  signal_and_sleep(m_x_02);
  signal_and_sleep(m_x_01);
}

void dec_y(){
  current_y--;
  signal_and_sleep(m_y_04);
  signal_and_sleep(m_y_03);
  signal_and_sleep(m_y_02);
  signal_and_sleep(m_y_01);
}

void mov_x(String inputString){
  char inputChars[inputString.length() - 6];
  inputString.substring(6).toCharArray(inputChars, inputString.length() - 6);
  int desired_x = atoi(inputChars);
  while(desired_x > current_x)
    inc_x();
  while(desired_x < current_x)
    dec_x();
}

void mov_y(String inputString){
  char inputChars[inputString.length() - 6];
  inputString.substring(6).toCharArray(inputChars, inputString.length() - 6);
  int desired_y = atoi(inputChars);
  while(desired_y > current_y)
    inc_y();
  while(desired_y < current_y)
    dec_y();
}

void loop() {
  if (stringComplete) {
    Serial.println(inputString);
    if(inputString.startsWith("INC_X"))
      inc_x();
    else if(inputString.startsWith("INC_Y"))
      inc_y();
    else if(inputString.startsWith("DEC_X"))
      dec_x();
    else if(inputString.startsWith("DEC_Y"))
      dec_y();
    else if(inputString.startsWith("MOV_X"))
      mov_x(inputString);
    else if(inputString.startsWith("MOV_Y"))
      mov_y(inputString);
    delay(50);
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
      char inChar = (char)Serial.read();    // Get the new byte
      inputString += inChar;
      if (inChar == '\n') {                 // If the incoming character is a newline, set a flag
        stringComplete = true;
      }
    }
}

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

int time01 = 10;
int time00 = 0;

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

void inc_and_sleep(int pin){
  digitalWrite(pin, HIGH);
  delay(time01);
  digitalWrite(pin, LOW);
  delay(time00);
}

void loop() {
  if (stringComplete) {
    Serial.println(inputString);
    if(inputString.startsWith("INC_X")){
        inc_and_sleep(m_x_01);
        inc_and_sleep(m_x_02);
        inc_and_sleep(m_x_03);
        inc_and_sleep(m_x_04);    
    }
    else if(inputString.startsWith("INC_Y")){
        inc_and_sleep(m_y_01);
        inc_and_sleep(m_y_02);
        inc_and_sleep(m_y_03);
        inc_and_sleep(m_y_04);    
    }
    else if(inputString.startsWith("DEC_X")){
        inc_and_sleep(m_x_04);
        inc_and_sleep(m_x_03);
        inc_and_sleep(m_x_02);
        inc_and_sleep(m_x_01);    
    }
    else if(inputString.startsWith("DEC_Y")){
        inc_and_sleep(m_y_04);
        inc_and_sleep(m_y_03);
        inc_and_sleep(m_y_02);
        inc_and_sleep(m_y_01);    
    }    
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

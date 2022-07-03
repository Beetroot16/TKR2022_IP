int pin1 = 11;
int pin2 = 10;

int flag1 = 0;
int flag2 = 0; 

void setup() {
  pinMode(pin1,INPUT);
  pinMode(pin2,INPUT);
  Serial.begin(9600);
}

void loop() {
  if (digitalRead(pin1)==HIGH && flag1 == 0){
    flag1 = 1;
    flag2 = 0;
    Serial.write("a");
  }
  if (digitalRead(pin2)==HIGH && flag2 == 0){
    flag2 = 1;
    flag1 = 0;
    Serial.write("b");
  }
}

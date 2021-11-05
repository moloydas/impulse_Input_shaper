const int step_pin = 9;
const int dir_pin = 8;

int dir = HIGH;

void setup() {
  Serial.begin(9600);
  // put your setup code here, to run once:
  pinMode(step_pin, OUTPUT);
  pinMode(dir_pin, OUTPUT);
  pinMode(12, OUTPUT);
  digitalWrite(12, HIGH);
  pinMode(13, OUTPUT);
  //Set Dir 
  digitalWrite(dir_pin, HIGH);

  pinMode(0, OUTPUT);
  digitalWrite(0,HIGH);
  pinMode(1, OUTPUT);
  digitalWrite(1,LOW);
  pinMode(2, OUTPUT);
  digitalWrite(2,LOW);
}

void step(int step_pin, int delay_micro){
  digitalWrite(step_pin, HIGH);
  digitalWrite(13, HIGH);
  delayMicroseconds(delay_micro);
  digitalWrite(step_pin, LOW);
  delayMicroseconds(delay_micro);
  digitalWrite(13, LOW);  
}

#define MICROSTEPPING 2
float step_size = 1.8/MICROSTEPPING;

int deg_2_numsteps(int degs){
  return int(degs/step_size);
}

void loop() {
  // put your main code here, to run repeatedly:

  if (dir == HIGH){
    dir = LOW;
  }
  else{
    dir = HIGH;  
  }
  
  Serial.println(dir);
  digitalWrite(dir_pin, dir);
  Serial.println(deg_2_numsteps(90));

  for (int i=0; i<deg_2_numsteps(160); i++){
    step(step_pin, 2000);
  }
  delay(15000);
}

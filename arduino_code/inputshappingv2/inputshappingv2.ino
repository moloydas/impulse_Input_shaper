const int step_pin = 9;
const int dir_pin = 8;
#define PI 3.1415926535897932384626433832795
int dir = HIGH;

#define MICROSTEPPING 2

// First broken print
//float w0 = 18.0822;
//float beta = 0.0699;

// Second imperfect print 
//float w0 = 20.95;
//float beta = 0.0695;
float w0 = 27.0;
float beta = 0.01;

// third print perfect
//float w0 = 23.0;
//float beta = 0.060;

float K = exp((-beta*PI)/(sqrt(1-pow(beta,2))));
float delta_T = PI/(w0*sqrt(1-pow(beta,2))) * 1000;
float D = 1 + 3*K + 3*pow(K,2) + pow(K,3);

float shape_stages[4] = {1/D,
                        3*K/D,
                        3*pow(K,2)/D,
                        pow(K,3)/D};

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
  digitalWrite(0,LOW);
  pinMode(1, OUTPUT);
  digitalWrite(1,LOW);
  pinMode(2, OUTPUT);
  digitalWrite(2,LOW);
}

void take_one_step(int step_pin, int dir_pin, int dir, int delay_micro){
  digitalWrite(dir_pin, dir);
  digitalWrite(step_pin, HIGH);
  digitalWrite(13, HIGH);
  delayMicroseconds(delay_micro);
  digitalWrite(step_pin, LOW);
  delayMicroseconds(delay_micro);
  digitalWrite(13, LOW);  
}

float step_size = 1.8/MICROSTEPPING;
int deg_2_numsteps(int degs){
  return int(degs/step_size);
}

float min_delay = 2.0/MICROSTEPPING; // is in second
float set_vel = 1.0/min_delay;
float curr_vel = 0;

int accel = 1;
int stage = 0;
uint32_t req_delay = 10000;
float shape_input_start_time = 0;

float shape_input(float curr_vel, float set_vel, int accel, float curr_time){
  float del_vel = 0;
  if ((accel == 1) and (stage < 4)){
    del_vel = shape_stages[stage] * set_vel;
  }
  else if ((accel == -1) and (stage < 4)){
    del_vel = -shape_stages[stage] * set_vel;
  }
  else{
    return curr_vel;
  }

//first stage
  if((curr_time < shape_input_start_time + delta_T) and (stage == 0)){
    curr_vel += del_vel;
    stage = 1;
  }
//second stage
  else if( (curr_time>shape_input_start_time+delta_T) and (curr_time<shape_input_start_time+2*delta_T) and (stage == 1)){
    curr_vel += del_vel;
    stage = 2;
  }
//third stage
  else if ((curr_time > shape_input_start_time + 2*delta_T) and (curr_time < shape_input_start_time + 3*delta_T) and (stage == 2)){
    curr_vel += del_vel;
    stage = 3;
  }
//final stage
  else if ((curr_time > shape_input_start_time + 3*delta_T) and (stage == 3)){
    curr_vel += del_vel;
    stage = 4;
  }
  return curr_vel;
}

void loop() {
  if (dir == HIGH){
    dir = LOW;
  }
  else{
    dir = HIGH;  
  }

  accel = 1;
  stage = 0;
  float curr_time = millis();
  shape_input_start_time = curr_time;

  for (int i=0; i<deg_2_numsteps(90); i++){
    curr_time = millis();
    curr_vel = shape_input(curr_vel, set_vel, accel, curr_time);
    req_delay = int(1000/curr_vel);
    take_one_step(step_pin, dir_pin, dir, req_delay);
  }

  accel = -1;
  stage = 0;
  shape_input_start_time = millis();
  int i=0;
  while(1){
    curr_time = millis();
    curr_vel = shape_input(curr_vel, set_vel, accel, curr_time);
    if (curr_vel < 0.1){
      break;
    }
    else{
      req_delay = int(1000/curr_vel);
    }
    take_one_step(step_pin, dir_pin, dir, req_delay);
    i+=1;
  }
  delay(15000);
}

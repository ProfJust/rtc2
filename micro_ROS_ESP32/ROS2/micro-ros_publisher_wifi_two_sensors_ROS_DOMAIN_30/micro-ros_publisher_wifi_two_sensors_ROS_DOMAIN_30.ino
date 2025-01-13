// zwei Sensoren  VL53L0X 
// an einem ESP32
// sendet über Micro-ROS-Wifiauf ROS_DOMAIN_ID 30
// OJ 10.1.25
//---------------------------------------------------
// tested @ Home Office 
/// Starting Mikro-ROS Agent
//  Wifi Version:   $ ros2 run micro_ros_agent micro_ros_agent udp4 --port 8888 -v6
//
// Important: ROS_DOMAIN_ID = 30, ROS_LOCALHOST_ONLY = 0 
//---------------------------------------------------
#include "Adafruit_VL53L0X.h"
#include <micro_ros_arduino.h>
#include <stdio.h>
#include <rcl/rcl.h>
#include <rcl/error_handling.h>
#include <rclc/rclc.h>
#include <rclc/executor.h>
#include <std_msgs/msg/int32.h>

rcl_publisher_t publisher1;
rcl_publisher_t publisher2;
std_msgs__msg__Int32 msg1;
std_msgs__msg__Int32 msg2;
rclc_executor_t executor;
rclc_support_t support;
rcl_allocator_t allocator;
rcl_init_options_t init_options;
rcl_node_t node;
rcl_timer_t timer;

#define LED_PIN 2
#define RCCHECK(fn) { rcl_ret_t temp_rc = fn; if((temp_rc != RCL_RET_OK)){error_loop();}}
#define RCSOFTCHECK(fn) { rcl_ret_t temp_rc = fn; if((temp_rc != RCL_RET_OK)){}}

// address we will assign if dual sensor is present
#define LOX1_ADDRESS 0x30
#define LOX2_ADDRESS 0x31

// set the XSHUT - Pins 
#define SHT_LOX1 18
#define SHT_LOX2 19

// objects for the vl53l0x
Adafruit_VL53L0X lox1 = Adafruit_VL53L0X();
Adafruit_VL53L0X lox2 = Adafruit_VL53L0X();
uint32_t range1=0;
uint32_t range2=0;

void setID() {
  // all reset
  digitalWrite(SHT_LOX1, LOW);    
  digitalWrite(SHT_LOX2, LOW);
  delay(10);
  // all unreset
  digitalWrite(SHT_LOX1, HIGH);
  digitalWrite(SHT_LOX2, HIGH);
  delay(10);

  // activating LOX1 and resetting LOX2
  digitalWrite(SHT_LOX1, HIGH);
  digitalWrite(SHT_LOX2, LOW);

  // initing LOX1
  if(!lox1.begin(LOX1_ADDRESS)) {while(1);}
  delay(10);

  // activating LOX2
  digitalWrite(SHT_LOX2, HIGH);
  delay(10);

  //initing LOX2
  if(!lox2.begin(LOX2_ADDRESS)) {while(1);}
}

void error_loop(){  //LED_BUILD_IN starts blinking
  while(1){
    digitalWrite(LED_PIN, !digitalRead(LED_PIN));
    delay(100);
  }
}

void timer_callback(rcl_timer_t * timer, int64_t last_call_time)
{  
  RCLC_UNUSED(last_call_time);
  if (timer != NULL) {
    RCSOFTCHECK(rcl_publish(&publisher1, &msg1, NULL));
    RCSOFTCHECK(rcl_publish(&publisher2, &msg2, NULL));
    //msg.data++; // Hat hier keine Auswirkung ==> Loop
  }
}

void setup() {
  // ---- set I2C-Adresses  ----
  pinMode(SHT_LOX2, OUTPUT);
  digitalWrite(SHT_LOX1, LOW);
  digitalWrite(SHT_LOX2, LOW);
  setID();
  // ---- set I2C-Adresses  END ----
  
  //--- Set ERROR-Loop LED ----- 
  pinMode(LED_PIN, OUTPUT);
  digitalWrite(LED_PIN, HIGH);

  // ############################# IP Adresse des PCs auf dem der µROS-Agent läuft !!! #####
  //WHS 
  set_microros_wifi_transports("TP-Link_Robotik", "48095655", "192.168.0.183", 8888); 
  //HomeOffice
  //set_microros_wifi_transports("just_a_FRITZbox", "PASSWORD", "192.168.178.37", 8888); 
  
  delay(2000);

  allocator = rcl_get_default_allocator();
  //-------  Set ROS_DOMAIN_ID to 30 ----------------
  init_options = rcl_get_zero_initialized_init_options();
  rcl_init_options_init(&init_options, allocator);
  rcl_init_options_set_domain_id(&init_options, 30);
  RCCHECK(rclc_support_init_with_options(&support, 0, NULL, &init_options, &allocator));
  //-------  End set ROS_DOMAIN_ID to 30 ----------------

   // create node
  RCCHECK(rclc_node_init_default(&node, "uros_wifi_range_node", "", &support));

  // create publisher 1
  RCCHECK(rclc_publisher_init_best_effort(
    &publisher1,
    &node,
    ROSIDL_GET_MSG_TYPE_SUPPORT(std_msgs, msg, Int32),
    "range1"));
    // create publisher 2

  RCCHECK(rclc_publisher_init_best_effort(
    &publisher2,
    &node,
    ROSIDL_GET_MSG_TYPE_SUPPORT(std_msgs, msg, Int32),
    "range2"));

  // create timer,
  const unsigned int timer_timeout = 100;
  RCCHECK(rclc_timer_init_default(
    &timer,
    &support,
    RCL_MS_TO_NS(timer_timeout),
    timer_callback));
  
  // create executor
  RCCHECK(rclc_executor_init(&executor, &support.context, 1, &allocator));
  RCCHECK(rclc_executor_add_timer(&executor, &timer));

  msg1.data = 0;
  msg2.data = 0;

  //if (!lox1.begin()) { while(1); }  Funkt nicht =>>> BLEIBT HIER HÄNGEN 
  lox1.startRangeContinuous(); 
  
  //if (!lox2.begin()) { while(1); }   Funkt nicht =>>> BLEIBT HIER HÄNGEN 
  lox2.startRangeContinuous();
}

void loop() {
  RCSOFTCHECK(rcl_publish(&publisher1, &msg1, NULL));
  RCSOFTCHECK(rcl_publish(&publisher2, &msg2, NULL));
  
  if (lox1.isRangeComplete()) {  range1 = lox1.readRange(); }
  if (range1 < 2000)  // if not out of range
    msg1.data = range1; 
 
  if (lox2.isRangeComplete()) {  range2 = lox2.readRange(); }
  if (range2 < 2000)  // if not out of range
    msg2.data = range2;
}

// zwei Sensoren  VL53L0X 
// an einem ESP32
// sendet über Micro-ROS-Wifiauf ROS_DOMAIN_ID 30
// OJ 10.1.25
// D22 SCL Gelb
// D21 SDA Grün
// D19  XSHUT_1
// D18  XSHUT_2
// GND  braun
// 3V3 rot

//---------------------------------------------------
// tested @ Home Office 
/// Starting Mikro-ROS Agent
//  Wifi Version:   $ ros2 run micro_ros_agent micro_ros_agent udp4 --port 8888 -v6
//
// Important: ROS_DOMAIN_ID = 30, ROS_LOCALHOST_ONLY = 0 

//################################# ADD WS25 ################
// Should send LaserScan Message directly
// sensor_msgs/msg/LaserScan Message  => publisher3
//---------------------------------------------------
#include "Adafruit_VL53L0X.h"
#include <micro_ros_arduino.h>
#include <stdio.h>
#include <rcl/rcl.h>
#include <rcl/error_handling.h>
#include <rclc/rclc.h>
#include <rclc/executor.h>
#include <std_msgs/msg/int32.h>
#include <sensor_msgs/msg/laser_scan.h>

rcl_publisher_t publisher1;
rcl_publisher_t publisher2;
rcl_publisher_t publisher3;
std_msgs__msg__Int32 msg1;
std_msgs__msg__Int32 msg2;
sensor_msgs__msg__LaserScan laserScanMsg;
static float ranges_buf[N]; 
static float intensities_buf[N];
// Anzahl Messstrahlen mit VL53L0X
#define BUF_LEN        2


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
    RCSOFTCHECK(rcl_publish(&publisher3, &laserScanMsg, NULL));
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

  RCCHECK(rclc_publisher_init_best_effort(
    &publisher3,
    &node,
    ROSIDL_GET_MSG_TYPE_SUPPORT(sensor_msgs, msg, LaserScan),
    "range_scan"));

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
  RCSOFTCHECK(rcl_publish(&publisher3, &laserScanMsg, NULL));
  
  if (lox1.isRangeComplete()) {  range1 = lox1.readRange(); }
  // if not out of range
  if (range1 < 2000) {  msg1.data = range1; } 
 
  if (lox2.isRangeComplete()) {  range2 = lox2.readRange(); }
  // if not out of range
  if (range2 < 2000) {  msg2.data = range2; }

//####### Create LaserScanMessage ###############
// Vgl. https://docs.ros2.org/foxy/api/sensor_msgs/msg/LaserScan.html
// ----------------------------------------------------------------------
// Zeitstempel setzen (sehr grob mit millis(); für produktiv besser Time-Sync)
  uint32_t now_ms = millis();
  laserScanMsg.header.stamp.sec = now_ms / 1000;
  laserScanMsg.header.stamp.nanosec = (now_ms % 1000) * 1000000;
  laserScanMsg.header.frame_id = "range_scan"; // ==> ins URDF für den RealBot eintragen

// Parameter (hier zurzeit nur Dummy-Werte)
  laserScanMsg.angle_min = -0.03;
  laserScanMsg.angle_max =  0.03;

  laserScanMsg.time_increment = 0.0f;
  laserScanMsg.angle_increment =
      (laserScanMsg.angle_max - laserScanMsg.angle_min) / BUF_LEN;

  laserScanMsg.scan_time = 0.1f;    // 10 Hz

  // Reichweitenbegrenzung
  laserScanMsg.range_min = 0.12f;
  laserScanMsg.range_max = 1.50f; //Meter


  laserScanMsg.ranges.size = BUF_LEN;
  laserScanMsg.intensities.size = BUF_LEN;

//Messwerte der VL53L0X zuweisen
  laserScanMsg.ranges.data[0] = msg1.data / 1000.0; //mm in m
  laserScanMsg.ranges.data[1] = msg2.data / 1000.0; //mm in m

  laserScanMsg.ranges.intensities[0] = 
  //laserScanMsg.ranges.size = BUF_LEN;
  //laserScanMsg.ranges.capacity = BUF_LEN;
 
  //  Leave Empty laserScanMsg.intensities.data 
  

/*
  for (int i = 0; i < BUF_LEN; i++) {
    float base = 2.0f + 1.5f * sinf(phase + i * 0.05f);
    if (base < laserScanMsg.range_min) base = laserScanMsg.range_min;
    if (base > laserScanMsg.range_max) base = laserScanMsg.range_max;
    ranges_buf[i] = base;
    intensities_buf[i] = 1.0f;  // konstante Intensität
  }

  // LaserScan-Message nullen und Felder initialisieren
  memset(&laserScanMsg, 0, sizeof(laserScanMsg));

  // Frame-ID setzen (als statischer String)
  static char frame_id[] = FRAME_ID;
  laserScanMsg.header.frame_id.data = frame_id;
  laserScanMsg.header.frame_id.size = strlen(frame_id);
  laserScanMsg.header.frame_id.capacity = strlen(frame_id);

  // Winkelbereich (0 .. 2*pi)
  laserScanMsg.angle_min = 0.0f;
  laserScanMsg.angle_max = 2.0f * 3.1415926f;
  

  // Zeitparameter (hier nur Dummy-Werte)
  laserScanMsg.time_increment = 0.0f;
  laserScanMsg.scan_time = 0.1f;    // 10 Hz

  // Reichweitenbegrenzung
  laserScanMsg.range_min = 0.12f;
  laserScanMsg.range_max = 10.0f;

  // statische Speicherbereiche für ranges/intensities zuweisen
  laserScanMsg.ranges.data = ranges_buf;
  laserScanMsg.ranges.size = 0;
  laserScanMsg.ranges.capacity = BUF_LEN;

  laserScanMsg.intensities.data = intensities_buf;
  laserScanMsg.intensities.size = 0;
  laserScanMsg.intensities.capacity = BUF_LEN;
*/

}

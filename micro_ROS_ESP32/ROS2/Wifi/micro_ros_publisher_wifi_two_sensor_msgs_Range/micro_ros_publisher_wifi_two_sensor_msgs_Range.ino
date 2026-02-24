
// Starting Mikro-ROS Agent
// Wifi Version Jazzy: 
// Auf dem Remote PC den Agent starten mit
// $ docker run -it --rm -v /dev:/dev --privileged --net=host microros/micro-ros-agent:jazzy udp4 --port 7777 -v6

// tested with Hardware as OK!! 8.1.2026
// D22 SCL Gelb
// D21 SDA Grün
// GND  braun
// 3V3 rot

/* FRAMES müssen gesendet werden (hier vom realen TB3)
// Wichtig! Sonst bekommt RVIZ Timing Probleme  !!!!!!!!!!!!!!!!!!!!!!!!!!!!!
// Auf dem realen TB3 den Frame setzen
// ubuntu@tb3: cd ~/turtlebot3_ws/src/turtlebot3/turtlebot3_description/urdf
// ubuntu@tb3: nano turtlebot3_burger.urdf
// Dort einfügen:

<!-- Range sensor links -->
   <link name="range_left_link"/>
   <link name="range_right_link"/>   
<!-- Range sensor joints -->
   <joint name="range_left_joint" type="fixed">
          <parent link="base_link"/>
          <child link="range_left_link"/>
          <!-- Position und Orientierung anpassen! -->
          <origin xyz="0.03 0.07 0.05" rpy="0 0 -0.3"/>
   </joint>
   <joint name="range_right_joint" type="fixed">
          <parent link="base_link"/>
          <child link="range_right_link"/>
          <!-- Position und Orientierung anpassen! -->
          <origin xyz="0.03 -0.07 0.05" rpy="0 0 0.3"/>
   </joint>

*/
// ################## Konfiguration des Netzwerkes ##############
// ===>>> secrets.h

#include "secrets.h"
#include "Adafruit_VL53L0X.h"
#include <micro_ros_arduino.h>
#include <stdio.h>
#include <rcl/rcl.h>
#include <rcl/error_handling.h>
#include <rclc/rclc.h>
#include <rclc/executor.h>
#include <rcl/time.h>
#include <sensor_msgs/msg/range.h>
#include <rosidl_runtime_c/string_functions.h>
#include <rosidl_runtime_c/primitives_sequence_functions.h>
#include <rmw_microros/time_sync.h>
#include <limits>

#if !defined(ESP32) && !defined(TARGET_PORTENTA_H7_M7) && !defined(ARDUINO_NANO_RP2040_CONNECT) && !defined(ARDUINO_WIO_TERMINAL)
#error This example is only avaible for Arduino Portenta, Arduino Nano RP2040 Connect, ESP32 Dev module and Wio Terminal
#endif

rcl_publisher_t range_pub_left;
rcl_publisher_t range_pub_right;

sensor_msgs__msg__Range range_msg_left;
sensor_msgs__msg__Range range_msg_right;
// Anzahl der range- Messpunkte bzw. der VL53L0X
// hier zunächst nur einer, aber der wird zweimal eingetragen 
#define BUF_LEN 2   // Sie schreiben ranges.data[0] und [1] -> also 2

rclc_executor_t executor;
rclc_support_t support;
rcl_allocator_t allocator;
rcl_init_options_t init_options;
rcl_node_t node;
rcl_timer_t timer;

#define LED_PIN  2 //beim ESP32
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

// this holds the measurement
uint32_t range1=0;
uint32_t range2=0;

void setID() {
  // beide aus
  digitalWrite(SHT_LOX1, LOW);
  digitalWrite(SHT_LOX2, LOW);
  delay(10);

  // LOX1 an, LOX2 bleibt aus
  digitalWrite(SHT_LOX1, HIGH);
  delay(10);
  if (!lox1.begin(0x29)) { while(1){} }          // erst am Default
  lox1.setAddress(LOX1_ADDRESS);                // dann umadressieren
  delay(10);

  // LOX2 an
  digitalWrite(SHT_LOX2, HIGH);
  delay(10);
  if (!lox2.begin(0x29)) { while(1){} }          // wieder am Default
  lox2.setAddress(LOX2_ADDRESS);                // dann umadressieren
  delay(10);
}


void error_loop(){
  while(1){
    digitalWrite(LED_PIN, !digitalRead(LED_PIN));
    delay(100);
  }
}

void timer_callback(rcl_timer_t * timer, int64_t last_call_time)
{
  RCLC_UNUSED(last_call_time);
  if (timer != NULL) {
    RCSOFTCHECK(rcl_publish(&range_pub_left, &range_msg_left, NULL));
    RCSOFTCHECK(rcl_publish(&range_pub_right, &range_msg_right, NULL));
  }
}

void init_range_msg_left(){
  sensor_msgs__msg__Range__init(&range_msg_left);

  // Frame im TF-Tree (z. B. Sensorframe)
  rosidl_runtime_c__String__assign(
    &range_msg_left.header.frame_id,
    "range_left_link"
  );

  // Sensor-Typ (VL53L0X = Infrarot / ToF)
  range_msg_left.radiation_type = sensor_msgs__msg__Range__INFRARED;

  // Öffnungswinkel des Sensors (VL53L0X ca. 25°)
  range_msg_left.field_of_view = 25.0f * M_PI / 180.0f;

  range_msg_left.min_range = 0.03f;   // 3 cm
  range_msg_left.max_range = 2.0f;    // 2 m
}

void init_range_msg_right(){
  sensor_msgs__msg__Range__init(&range_msg_right);

  // Frame im TF-Tree (z. B. Sensorframe)
  rosidl_runtime_c__String__assign(
    &range_msg_right.header.frame_id,
    "range_right_link"
  );

  // Sensor-Typ (VL53L0X = Infrarot / ToF)
  range_msg_right.radiation_type = sensor_msgs__msg__Range__INFRARED;

  // Öffnungswinkel des Sensors (VL53L0X ca. 25°)
  range_msg_right.field_of_view = 25.0f * M_PI / 180.0f;

  range_msg_right.min_range = 0.03f;   // 3 cm
  range_msg_right.max_range = 2.0f;    // 2 m
}

void setup() {
  // ########################### IP Adresse des PCs auf dem der µROS-Agent läuft , !!!!nicht der ESP32 im Router!!! #####
  
  set_microros_wifi_transports(ssid, pass, agent_ip, 7777);
  // Alternative WLAN 
  //  set_microros_wifi_transports("TP-Link_6F5A", "13078553", "192.168.0.183", 8888);
  //  set_microros_wifi_transports("AEJJ", "81202126", "192.168.1.107", 8888);
  
  pinMode(LED_PIN, OUTPUT);    // Wenn der ESP32 ein LED hat.
  digitalWrite(LED_PIN, HIGH);
  delay(2000);
  allocator = rcl_get_default_allocator();

  //-------  Set ROS_DOMAIN_ID to 30 ----------------
  //create init_options
    init_options = rcl_get_zero_initialized_init_options();
    RCCHECK(rcl_init_options_init(&init_options, allocator));
    RCCHECK(rcl_init_options_set_domain_id(&init_options, 30));
    RCCHECK(rclc_support_init_with_options(&support, 0, NULL, &init_options, &allocator));
  //-------  End set ROS_DOMAIN_ID to 30 ----------------
  // create node
  RCCHECK(rclc_node_init_default(&node, "uros_wifi_range_node", "", &support));
  
  // Hier Time Synchronisation mit uROS-Agent (Epoch Time)
  // rmw_uros_sync_session(1000);
  // --- erzwinge Zeitsynchronisation beim Start ---
  bool synced = false;
  while (!synced) {
      synced = rmw_uros_sync_session(500) == RCL_RET_OK; // 500 ms Timeout
      if (!synced) {
          Serial.println("Waiting for time sync with micro-ROS Agent...");
          delay(100);
      }
  }
  Serial.println("Time sync successful!");
 
  // create publisher
  init_range_msg_left();
  RCCHECK(rclc_publisher_init_best_effort(
    &range_pub_left,
    &node,
    ROSIDL_GET_MSG_TYPE_SUPPORT(sensor_msgs, msg, Range),
    "range_left")
  );

  init_range_msg_right();
  RCCHECK(rclc_publisher_init_best_effort(
    &range_pub_right,
    &node,
    ROSIDL_GET_MSG_TYPE_SUPPORT(sensor_msgs, msg, Range),
    "range_right")
  );
  
  // Starte VL53L0X
  pinMode(SHT_LOX1, OUTPUT);
  pinMode(SHT_LOX2, OUTPUT);
  digitalWrite(SHT_LOX1, LOW);
  digitalWrite(SHT_LOX2, LOW);
  setID();
  lox1.startRangeContinuous(); 
  lox2.startRangeContinuous(); 
}

void loop() {
  //### nur mit 20 Hz publishen um den micro-ROS Agent nicht zu überfordern
  static uint32_t last_pub = 0;
  if (millis() - last_pub >= 50) {   // 50 ms -> 20 Hz
    last_pub = millis();  
    //###  Messwerte holen
    if (lox1.isRangeComplete()) {  range2 = lox1.readRange(); }
    if (lox2.isRangeComplete()) {  range1 = lox2.readRange(); }
        
    //### Time Stamp synchronisieren ###
    static uint32_t last_sync_ms = 0;
    if((millis() - last_sync_ms) > 10000) { // Alle 10 sec nachsynchronisieren
      last_sync_ms = millis();
      rmw_uros_sync_session(300);
    }

    //### Zeitstempel setzen ####
    uint64_t now_ns = rmw_uros_epoch_nanos(); //Epoch-Zeit in ns holen
    range_msg_left.header.stamp.sec     = now_ns / 1000000000ULL;
    range_msg_left.header.stamp.nanosec = now_ns % 1000000000ULL; 
    range_msg_right.header.stamp.sec     = now_ns / 1000000000ULL;
    range_msg_right.header.stamp.nanosec = now_ns % 1000000000ULL; 
      
    //### Messwerte der VL53L0X zuweisen  ###
    float range_l_m = range2 / 1000.0f;
    // 0 oder NaN/Inf -> als "frei" behandeln
    if (!isfinite(range_l_m) || range_l_m <= 0.0f) {
      range_l_m = range_msg_left.max_range;
    }
    // clamp
    if (range_l_m < range_msg_left.min_range) range_l_m = range_msg_left.min_range;
    if (range_l_m > range_msg_left.max_range) range_l_m = range_msg_left.max_range;

    range_msg_left.range = range_l_m;


    float range_r_m = range1 / 1000.0f;
    if (!isfinite(range_r_m) || range_r_m <= 0.0f) {
      range_r_m = range_msg_right.max_range;
    }
    // clamp
    if (range_r_m < range_msg_right.min_range) range_r_m = range_msg_right.min_range;
    if (range_r_m > range_msg_right.max_range) range_r_m = range_msg_right.max_range;
          
    range_msg_right.range = range_r_m;
    
    //===> PUBLISH
    rcl_ret_t rc_left  = rcl_publish(&range_pub_left,  &range_msg_left,  NULL);
    rcl_ret_t rc_right = rcl_publish(&range_pub_right, &range_msg_right, NULL);
  } //end if
}


// Starting Mikro-ROS Agent
// Wifi Version Jazzy: 
// Auf dem Remote PC den Agent starten mit
// $ docker run -it --rm -v /dev:/dev --privileged --net=host microros/micro-ros-agent:jazzy udp4 --port 7777 -v6

// tested with Hardware as OK!! 8.1.2026
// D22 SCL Gelb
// D21 SDA Grün
// GND  braun
// 3V3 rot

// Wichtig! Sonst bekommt RVIZ Timing Probleme  !!!!!!!!!!!!!!!!!!!!!!!!!!!!!
// Auf dem realen TB3 den Frame setzen
// ubuntu@tb3: cd ~/turtlebot3_ws/src/turtlebot3/turtlebot3_description/urdf
// ubuntu@tb3: nano turtlebot3_burger.urdf
// Dort einfügen:
""" 
      <!-- Range sensor frame -->
        <link name="range_scan"/>

        <joint name="range_scan_joint" type="fixed">
                <parent link="base_link"/>
                <child link="range_scan"/>
                <!-- Position und Orientierung anpassen! -->
                <origin xyz="0.10 0.0 0.15" rpy="0 0 0"/>
        </joint>
"""

#include "Adafruit_VL53L0X.h"
#include <micro_ros_arduino.h>
#include <stdio.h>
#include <rcl/rcl.h>
#include <rcl/error_handling.h>
#include <rclc/rclc.h>
#include <rclc/executor.h>
#include <rcl/time.h>
#include <sensor_msgs/msg/laser_scan.h>
#include <rosidl_runtime_c/string_functions.h>
#include <rosidl_runtime_c/primitives_sequence_functions.h>
#include <rmw_microros/time_sync.h>

#if !defined(ESP32) && !defined(TARGET_PORTENTA_H7_M7) && !defined(ARDUINO_NANO_RP2040_CONNECT) && !defined(ARDUINO_WIO_TERMINAL)
#error This example is only avaible for Arduino Portenta, Arduino Nano RP2040 Connect, ESP32 Dev module and Wio Terminal
#endif

rcl_publisher_t publisher3;       // LaserScan 
sensor_msgs__msg__LaserScan laserScanMsg;

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

Adafruit_VL53L0X lox = Adafruit_VL53L0X();
uint32_t range=0;

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
    RCSOFTCHECK(rcl_publish(&publisher3, &laserScanMsg, NULL));
  }
}

void init_laserscan_msg()
{
  sensor_msgs__msg__LaserScan__init(&laserScanMsg);
  // frame_id im tf-Tree setzen
  rosidl_runtime_c__String__assign(&laserScanMsg.header.frame_id, "range_scan");
  // VL53 Parameter (anpassen)
  laserScanMsg.angle_min = 0.0f;
  laserScanMsg.angle_max = 0.1f;
  laserScanMsg.angle_increment = (laserScanMsg.angle_max - laserScanMsg.angle_min) / (BUF_LEN > 1 ? (BUF_LEN - 1) : 1);
  laserScanMsg.time_increment = 0.0f;
  laserScanMsg.scan_time = 0.0f;
  laserScanMsg.range_min = 0.03f;   // VL53L0X typ. ~3 cm
  laserScanMsg.range_max = 2.0f;    // je nach Setup

  // ranges/intensities Speicher anlegen
  rosidl_runtime_c__float__Sequence__init(&laserScanMsg.ranges, BUF_LEN);
  rosidl_runtime_c__float__Sequence__init(&laserScanMsg.intensities, BUF_LEN);

  // Optional: initialisieren
  for (size_t i = 0; i < BUF_LEN; i++) {
    laserScanMsg.ranges.data[i] = 0.0f;
    laserScanMsg.intensities.data[i] = 0.0f;
  }
}


void setup() {
  // ########################### IP Adresse des PCs auf dem der µROS-Agent läuft , !!!!nicht der ESP32 im Router!!! #####
  char ssid[] = "TP-Link_Robotik";
  char pass[] = "48095655";
  char agent_ip[] = "192.168.0.57"; // IP des Remote PCs mit Agent
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
  rmw_uros_sync_session(1000);
 
  // create publisher
  init_laserscan_msg();
  RCCHECK(rclc_publisher_init_best_effort(
  &publisher3,
  &node,
  ROSIDL_GET_MSG_TYPE_SUPPORT(sensor_msgs, msg, LaserScan),
  "range_scan"));
  
  // Starte VL53L0X
  if (!lox.begin()) {
      //Serial.println(F("Failed to boot VL53L0X"));
      error_loop();
  }
  lox.startRangeContinuous();
}

void loop() {
   // nur mit 20 Hz publishen um den micro-ROS Agent nicht zu überfordern
  static uint32_t last_pub = 0;
  if (millis() - last_pub >= 50) {   // 50 ms -> 20 Hz
    last_pub = millis();  
    // Messwert holen
      if (lox.isRangeComplete()) {
          range = lox.readRange();
      }
      
    //  ####### Create LaserScanMessage ###############
      // Time Stamp setzen (Epoch Time, matches TF)
      static uint32_t last_sync_ms = 0;
      if((millis() - last_sync_ms) > 10000) { // Alle 10 sec nachsynchronisieren
        last_sync_ms = millis();
        rmw_uros_sync_session(300);
      }

      uint64_t now_ns = rmw_uros_epoch_nanos(); //Epoch-Zeit in ns holen
      //RCSOFTCHECK(rcl_clock_get_now(&ros_clock, &now_ns));
      laserScanMsg.header.stamp.sec    = (int32_t)(now_ns / 1000000000ULL); //ns => sec
      laserScanMsg.header.stamp.nanosec = (uint32_t)(now_ns % 1000000000ULL); 
      //Messwerte der VL53L0X zuweisen
      laserScanMsg.ranges.data[0] = range / 1000.0; //mm in m wandeln
      laserScanMsg.ranges.data[1] = range / 1000.0; //mm in m wandeln
      laserScanMsg.intensities.data[0] = 0.0f;
      laserScanMsg.intensities.data[1] = 0.0f;  
    //===> PUBLISH
      rcl_ret_t rc = rcl_publish(&publisher3, &laserScanMsg, NULL);
    //if (rc != RCL_RET_OK) {
      // LED dauerhaft an oder Serial print, damit Sie es sehen
    //  digitalWrite(LED_PIN, HIGH);
    //}
  }
}

// see https://robofoundry.medium.com/esp32-micro-ros-actually-working-over-wifi-and-udp-transport-519a8ad52f65

// Starting Mikro-ROS Agent
// Serial Version: $ ros2 run micro_ros_agent micro_ros_agent serial --dev /dev/ttyUSB0
// Wifi Version:   $ ros2 run micro_ros_agent micro_ros_agent udp4 --port 8888 -v6

// see https://github.com/micro-ROS/micro_ros_setup/issues/532
//     https://robofoundry.medium.com/esp32-micro-ros-actually-working-over-wifi-and-udp-transport-519a8ad52f65
#include "Adafruit_VL53L0X.h"
#include <micro_ros_arduino.h>
#include <stdio.h>
#include <rcl/rcl.h>
#include <rcl/error_handling.h>
#include <rclc/rclc.h>
#include <rclc/executor.h>
#include <std_msgs/msg/int32.h>
//################################## SET SSID here !! ######################
/*#define WIFI_SSID "TP-Link_Robotik"
#define WIFI_PASS "4809565"
#define IP "192.168.0.183"*/
//################################## SET SSID here !! ######################

#if !defined(ESP32) && !defined(TARGET_PORTENTA_H7_M7) && !defined(ARDUINO_NANO_RP2040_CONNECT) && !defined(ARDUINO_WIO_TERMINAL)
#error This example is only avaible for Arduino Portenta, Arduino Nano RP2040 Connect, ESP32 Dev module and Wio Terminal
#endif

rcl_publisher_t publisher;
std_msgs__msg__Int32 msg;
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
    RCSOFTCHECK(rcl_publish(&publisher, &msg, NULL));
    //msg.data = range; HIER FUNKTIONIERT DAS NICHT !!! => LOOP
  }
}

void setup() {
  // ############################# IP Adresse des PCs auf dem der µROS-Agent läuft !!! #####
  set_microros_wifi_transports("TP-Link_Robotik", "48095655", "192.168.0.183", 8888); 
  
  pinMode(LED_PIN, OUTPUT);
  digitalWrite(LED_PIN, HIGH);

  delay(2000);

  allocator = rcl_get_default_allocator();

  //create init_options
  RCCHECK(rclc_support_init(&support, 0, NULL, &allocator));

  // create node
  RCCHECK(rclc_node_init_default(&node, "micro_ros_arduino_wifi_node", "", &support));

  // create publisher
  RCCHECK(rclc_publisher_init_best_effort(
    &publisher,
    &node,
    ROSIDL_GET_MSG_TYPE_SUPPORT(std_msgs, msg, Int32),
    "range"));

  //msg.data = 0;
  if (!lox.begin()) {
      //Serial.println(F("Failed to boot VL53L0X"));
      while(1);
  }
  lox.startRangeContinuous();
}

void loop() {
    RCSOFTCHECK(rcl_publish(&publisher, &msg, NULL));
  
    if (lox.isRangeComplete()) {
      range = lox.readRange();
    }
    msg.data = range;
}

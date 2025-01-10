// Erster Test des Sensors VL53L0X 
// an einem ESP32
// OJ 16.12.24
//---------------------------------------------------
/*Die `ROSDOMAINID` ist eine Umgebungsvariable, die im Robot Operating System 2 (ROS 2) verwendet wird. Sie wird genutzt, um Netzwerkkonflikte zu vermeiden, wenn mehrere unabhängige ROS 2 Netze im selben physischen Netzwerk laufen. Die `ROSDOMAINID` funktioniert als ein Logik-Filter, der sicherstellt, dass nur Knoten, die dieselbe Domain ID teilen, miteinander kommunizieren können.

Standardmäßig ist die `ROSDOMAINID` auf `0` gesetzt. Wenn du jedoch mehrere separate ROS 2 Systeme in der gleichen Netzwerkumgebung betreiben möchtest, kannst du für jedes System eine unterschiedliche `ROSDOMAINID` einstellen, um Interferenzen zwischen den Systemen zu vermeiden.

Um die `ROS_DOMAIN_ID` zu setzen, kannst du in der Shell, aus der du dein ROS 2 System startest, den folgenden Befehl verwenden:
*/
// usage:
// $ export ROS_DOMAIN_ID=0

// ROS_DOMAIN_ID auf 30 ändern (wie beim tb3)  siehe
// https://micro.ros.org/docs/tutorials/programming_rcl_rclc/node/

// ggf: 
// git clone https://github.com/micro-ROS/micro-ROS-Agent.git -b humble
// rosdep install --from-paths src --ignore-src -r -y
// build & source
// $ ros2 run micro_ros_agent micro_ros_agent serial --dev /dev/ttyUSB0 ROS_DOMAIN_ID=0
// Ensure ROS_DOMAIN_ID is 0, e.g.  export ROS_DOMAIN_ID=0 in .bashrc  
// Ensure ROS_LOCALHOST_ONLY is 0, see export in .bashrc  


//---------------------------------------------------
#include "Adafruit_VL53L0X.h"
#include <micro_ros_arduino.h>
#include <stdio.h>
#include <rcl/rcl.h>
#include <rcl/error_handling.h>
#include <rclc/rclc.h>
#include <rclc/executor.h>
#include <std_msgs/msg/int32.h>

rcl_publisher_t publisher;
std_msgs__msg__Int32 msg;
rclc_executor_t executor;
rclc_support_t support;
rcl_allocator_t allocator;
rcl_init_options_t init_options;
rcl_node_t node;
rcl_timer_t timer;

#define LED_PIN 13
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
    //msg.data++;
    msg.data = range;
  }
}

void setup() {
  set_microros_transports();
  
  pinMode(LED_PIN, OUTPUT);
  digitalWrite(LED_PIN, HIGH);  

  allocator = rcl_get_default_allocator();
  
  RCCHECK(rclc_support_init(&support, 0, NULL, &allocator)); 
  
  // create node
  RCCHECK(rclc_node_init_default(&node, "micro_ros_range_node", "", &support));

  // create publisher
  RCCHECK(rclc_publisher_init_default(
    &publisher,
    &node,
    ROSIDL_GET_MSG_TYPE_SUPPORT(std_msgs, msg, Int32),
    "range"));

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

  msg.data = 0;

  if (!lox.begin()) {
      //Serial.println(F("Failed to boot VL53L0X"));
      while(1);
  }
  lox.startRangeContinuous();
  
}

void loop() {
  //delay(100);
  RCSOFTCHECK(rclc_executor_spin_some(&executor, RCL_MS_TO_NS(100)));
  if (lox.isRangeComplete()) {
    range = lox.readRange();
  }
  msg.data = range;
}

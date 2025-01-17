#!/usr/bin/env python3
import rclpy
from rclpy.node import Node

from example_interfaces.msg import Int64
import random

class TemperatureSensorNode(Node):
    def __init__(self):
        super().__init__("node_temperature_sensor")
        self.temperature_publisher_ = self.create_publisher(
            Int64, "topic_temperature", 10)
        
        self.temperature_timer_ = self.create_timer(
            2.0, self.publish_temperature)
        
        print(" Node 'node_temperature_sensor' started to publish random value 'topic_temperature'")

    def publish_temperature(self):
        temperature = random.randint(20, 30)
        msg = Int64()
        msg.data = temperature
        self.temperature_publisher_.publish(msg)
        print(temperature)

def main(args=None):
    rclpy.init(args=args)
    node = TemperatureSensorNode()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == "__main__":
    main()
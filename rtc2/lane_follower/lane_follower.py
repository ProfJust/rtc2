#!/usr/bin/env python3
import rclpy
from rclpy.node import Node

from sensor_msgs.msg import Image
from geometry_msgs.msg import Twist
from cv_bridge import CvBridge

import cv2
import numpy as np
import time


class LineFollower(Node):
    def __init__(self):
        super().__init__('line_follower_hsv')

        # Topics
        self.declare_parameter('image_topic', '/camera/camera/color/image_raw')
        self.declare_parameter('cmd_vel_topic', '/cmd_vel')

        # ROI
        self.declare_parameter('roi_y_start_ratio', 0.60)  # untere 40%

        # HSV "weiß": low saturation, high value
        self.declare_parameter('s_max', 60)     # 0..255 (kleiner = "weißer")
        self.declare_parameter('v_min', 170)    # 0..255 (größer = "heller")

        # Control
        self.declare_parameter('kp', 1.4)
        self.declare_parameter('kd', 0.12)
        self.declare_parameter('v_fast', 0.15)
        self.declare_parameter('v_slow', 0.08)
        self.declare_parameter('max_w', 1.5)

        # Detection thresholds
        self.declare_parameter('min_contour_area', 150)  # ggf. anpassen

        self.bridge = CvBridge()

        self.roi_y_start_ratio = float(self.get_parameter('roi_y_start_ratio').value)
        self.s_max = int(self.get_parameter('s_max').value)
        self.v_min = int(self.get_parameter('v_min').value)

        self.kp = float(self.get_parameter('kp').value)
        self.kd = float(self.get_parameter('kd').value)
        self.v_fast = float(self.get_parameter('v_fast').value)
        self.v_slow = float(self.get_parameter('v_slow').value)
        self.max_w = float(self.get_parameter('max_w').value)

        self.min_contour_area = int(self.get_parameter('min_contour_area').value)

        image_topic = self.get_parameter('image_topic').value
        cmd_vel_topic = self.get_parameter('cmd_vel_topic').value

        self.sub = self.create_subscription(Image, image_topic, self.on_image, 10)
        self.pub = self.create_publisher(Twist, cmd_vel_topic, 10)

        self.prev_error = 0.0
        self.prev_t = time.time()

        self.get_logger().info(f"Subscribed: {image_topic} | Publishing: {cmd_vel_topic}")

    def on_image(self, msg: Image):
        frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        h, w, _ = frame.shape

        # ROI
        y0 = int(h * self.roi_y_start_ratio)
        roi = frame[y0:h, :]

        hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

        # "white" mask: S <= s_max AND V >= v_min
        lower = np.array([0, 0, self.v_min], dtype=np.uint8)
        upper = np.array([179, self.s_max, 255], dtype=np.uint8)
        mask = cv2.inRange(hsv, lower, upper)

        # Morphology
        kernel = np.ones((5, 5), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=2)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=1)

        # Find contours
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Filter by area
        candidates = []
        for c in contours:
            area = cv2.contourArea(c)
            if area < self.min_contour_area:
                continue
            x, y, cw, ch = cv2.boundingRect(c)
            cx = x + cw / 2.0
            candidates.append((area, cx, c))

        if len(candidates) < 2:
            # Failsafe: Stop (für Oval ohne Kreuzungen meist besser als "suchen")
            self.pub.publish(Twist())
            return

        # Sort by x-position -> leftmost and rightmost are our lane borders
        candidates.sort(key=lambda t: t[1])
        left = candidates[0]
        right = candidates[-1]

        left_x = left[1]
        right_x = right[1]
        if right_x <= left_x:
            self.pub.publish(Twist())
            return

        lane_center = 0.5 * (left_x + right_x)
        img_center = w / 2.0

        error_px = lane_center - img_center
        error = error_px / (w / 2.0)  # normalize to [-1..1]

        # PD control
        now = time.time()
        dt = max(1e-3, now - self.prev_t)
        derr = (error - self.prev_error) / dt

        w_cmd = -(self.kp * error + self.kd * derr)
        w_cmd = float(np.clip(w_cmd, -self.max_w, self.max_w))

        # Speed schedule (langsamer in Kurven)
        v_cmd = self.v_fast if abs(error) < 0.20 else self.v_slow

        tw = Twist()
        tw.linear.x = float(v_cmd)
        tw.angular.z = float(w_cmd)
        self.pub.publish(tw)

        self.prev_error = error
        self.prev_t = now


def main():
    rclpy.init()
    node = LineFollower()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
""" Lane Follower für Realsense Kamera.
    Verwendet nur den Farbkanal (keine Tiefeninfos).
    Steuerung via PID-Regler basierend auf dem Schwerpunkt der erkannten weißen Fahrbahnmarkierung.
    
    Algorithmus (bewährt im Labor)  
    https://chatgpt.com/s/t_696a1a185854819190c3167a21df5950

        ROI: Nur unteren Bildbereich auswerten (z. B. untere 40–50%), weil dort die Linien „relevant“ sind.
        Weiß-Segmentierung:
            HSV ist meist stabiler als RGB.
        Weiß: niedrige Sättigung, hohe Helligkeit (V).
        Maske säubern: erode/dilate oder morphologyEx(close)
        Spurmitte bestimmen:
            Einfach: Schwerpunkt aller weißen Pixel.
            Besser: links/rechts getrennt suchen (z. B. über Spaltenhistogramm) und Mitte aus (toggle) mid = (x_left + x_right)/2 ableiten.

        Regelung:
            omega = - (Kp*e + Ki*∫e dt + Kd*de/dt)
            v konstant oder leicht reduziert bei großer Abweichung.
    
    """

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from geometry_msgs.msg import Twist
from cv_bridge import CvBridge
import cv2
import numpy as np
import time

class LaneFollower(Node):
    def __init__(self):
        super().__init__('lane_follower_realsense')

        # Parameter (einfach via ros2 param set/tunable)
        self.declare_parameter('image_topic', '/camera/camera/color/image_raw')
        self.declare_parameter('cmd_vel_topic', '/cmd_vel')
        self.declare_parameter('roi_height_ratio', 0.45)   # untere 45% des Bildes
        self.declare_parameter('v_forward', 0.12)          # m/s
        self.declare_parameter('v_min', 0.05)
        self.declare_parameter('w_max', 1.5)               # rad/s

        # HSV threshold für "weiß" (Startwerte)
        self.declare_parameter('white_s_max', 60)          # S <= 60
        self.declare_parameter('white_v_min', 180)         # V >= 180

        # PID
        self.declare_parameter('kp', 0.0040)
        self.declare_parameter('ki', 0.0000)
        self.declare_parameter('kd', 0.0015)

        self.bridge = CvBridge()
        self.cmd_pub = self.create_publisher(Twist, self.get_parameter('cmd_vel_topic').value, 10)
        self.sub = self.create_subscription(Image, self.get_parameter('image_topic').value, self.on_img, 10)

        self.e_int = 0.0
        self.e_prev = 0.0
        self.t_prev = time.time()

        self.get_logger().info('Lane follower started.')

    def on_img(self, msg: Image):
        # Timing
        t = time.time()
        dt = max(1e-3, t - self.t_prev)
        self.t_prev = t

        # Image -> OpenCV
        frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        h, w = frame.shape[:2]

        # ROI
        roi_ratio = float(self.get_parameter('roi_height_ratio').value)
        y0 = int(h * (1.0 - roi_ratio))
        roi = frame[y0:h, :]

        # HSV & Weißmaske
        hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
        s_max = int(self.get_parameter('white_s_max').value)
        v_min = int(self.get_parameter('white_v_min').value)

        lower = np.array([0, 0, v_min], dtype=np.uint8)
        upper = np.array([180, s_max, 255], dtype=np.uint8)
        mask = cv2.inRange(hsv, lower, upper)

        # Morphologie: kleine Lücken schließen
        kernel = np.ones((5, 5), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=2)

        # Schwerpunkt der weißen Pixel
        M = cv2.moments(mask)
        if M["m00"] < 1e5:
            # Zu wenig Linie gesehen -> sicherheitsorientiert: langsamer, geradeaus/leicht suchen
            self.publish_cmd(v=float(self.get_parameter('v_min').value), w=0.0)
            return

        cx = int(M["m10"] / M["m00"])  # x im ROI-Koordinatensystem
        x_mid = w // 2

        # Fehler: Spurzentrum - Bildmitte
        e = (cx - x_mid)

        # PID
        kp = float(self.get_parameter('kp').value)
        ki = float(self.get_parameter('ki').value)
        kd = float(self.get_parameter('kd').value)

        self.e_int += e * dt
        de = (e - self.e_prev) / dt
        self.e_prev = e

        w_cmd = -(kp * e + ki * self.e_int + kd * de)

        # Sättigung
        w_max = float(self.get_parameter('w_max').value)
        w_cmd = float(np.clip(w_cmd, -w_max, w_max))

        # Vorwärtsgeschwindigkeit ggf. reduzieren bei großer Abweichung
        v_fwd = float(self.get_parameter('v_forward').value)
        v_min = float(self.get_parameter('v_min').value)
        scale = max(0.0, 1.0 - min(1.0, abs(e) / (0.45 * w)))  # heuristisch
        v_cmd = v_min + (v_fwd - v_min) * scale

        self.publish_cmd(v=v_cmd, w=w_cmd)

    def publish_cmd(self, v: float, w: float):
        tw = Twist()
        tw.linear.x = float(v)
        tw.angular.z = float(w)
        self.cmd_pub.publish(tw)

def main():
    rclpy.init()
    node = LaneFollower()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        # Stop
        node.publish_cmd(0.0, 0.0)
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()

#!/usr/bin/env python3
# by Chat GPT and oj, 24.06.14
# Westfälische Hochschule - Campus Bocholt
# Steuerklasse für TurtleBot3 (Burger/Waffle) in ROS2 Jazzy.
# - Publiziert Twist auf /cmd_vel
# - Liest Odometry von /odom
# - Liest LaserScan von /scan
# - Bietet Blocking-Kommandos: stop, move_forward, rotate, go_to_goal
# -------------------------------------------
"""
| Methode                            | Aufgabe                                                      |
| ---------------------------------- | ------------------------------------------------------------ |
| `move_forward(distance, speed)`    | Fährt geradeaus, bis Distanz erreicht oder Hindernis erkannt |
| `rotate(angle_rad, angular_speed)` | Dreht um bestimmten Winkel (rad)                             |
| `go_to_goal(x, y)`                 | Fährt mit P-Regler zu Koordinate (x,y)                       |
| `stop()`                           | Sofort anhalten                                              |
| `shutdown()`                       | Node und ROS sauber beenden    

💡 Erweiterungsideen
    PID-Regler für weichere Bewegung
    Integration mit /amcl_pose für Navigation
    Hindernisumfahrung mit LaserScan
    Kompatibilität mit TwistStamped                              |
"""
import math
import time
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from sensor_msgs.msg import LaserScan
from tf_transformations import euler_from_quaternion


class TurtleBot3Controller(Node):
    """
    Steuerklasse für TurtleBot3 (Burger/Waffle) in ROS2 Jazzy.
    - Publisher: /cmd_vel (Twist)
    - Subscriber: /odom (Odometry), /scan (LaserScan)
    - Methoden: stop(), move_forward(), rotate(), go_to_goal()
    """

    def __init__(self, rate_hz: float = 20.0, dist_tol: float = 0.05, ang_tol: float = 0.05):
        super().__init__('turtlebot3_controller')

        # Publisher / Subscriber
        self.cmd_pub = self.create_publisher(Twist, '/cmd_vel', 10)
        self.odom_sub = self.create_subscription(Odometry, '/odom', self._odom_cb, 10)
        self.scan_sub = self.create_subscription(LaserScan, '/scan', self._scan_cb, 10)

        # Steuerparameter
        self.rate_hz = rate_hz
        self.dt = 1.0 / rate_hz
        self.dist_tol = dist_tol
        self.ang_tol = ang_tol

        # Zustände
        self.pose = None  # (x, y, yaw)
        self.obstacle_distance = float('inf')

        self.get_logger().info("TurtleBot3Controller bereit – warte auf Odom und Scan...")

    # ------------------- Callbacks -------------------
    def _odom_cb(self, msg: Odometry):
        pos = msg.pose.pose.position
        ori = msg.pose.pose.orientation
        _, _, yaw = euler_from_quaternion([ori.x, ori.y, ori.z, ori.w])
        self.pose = (pos.x, pos.y, yaw)

    def _scan_cb(self, msg: LaserScan):
        # mittlere Front-Distanz (0° ± 15°)
        n = len(msg.ranges)
        front_ranges = msg.ranges[n // 2 - 15:n // 2 + 15]
        self.obstacle_distance = min(front_ranges)

    # ------------------- Hilfsfunktionen -------------------
    def _wait_for_pose(self):
        self.get_logger().info("Warte auf Odom-Daten...")
        while rclpy.ok() and self.pose is None:
            rclpy.spin_once(self, timeout_sec=0.1)
        self.get_logger().info("Pose empfangen.")

    def _publish_cmd(self, lin_x=0.0, ang_z=0.0):
        msg = Twist()
        msg.linear.x = lin_x
        msg.angular.z = ang_z
        self.cmd_pub.publish(msg)

    def stop(self):
        self._publish_cmd(0.0, 0.0)

    # ------------------- Bewegungen -------------------
    def move_forward(self, distance: float, speed: float = 0.15):
        """Geradeaus fahren (mit Hinderniserkennung)."""
        self._wait_for_pose()
        start_x, start_y, _ = self.pose

        while rclpy.ok():
            rclpy.spin_once(self, timeout_sec=0.0)
            if self.obstacle_distance < 0.25:
                self.get_logger().warn("Hindernis erkannt! Stoppe.")
                break

            x, y, _ = self.pose
            dist = math.hypot(x - start_x, y - start_y)
            if dist >= distance - self.dist_tol:
                break

            v = min(speed, 0.5 * (distance - dist) + 0.05)
            self._publish_cmd(v, 0.0)
            time.sleep(self.dt)

        self.stop()
        self.get_logger().info("Vorwärtsbewegung beendet.")

    def rotate(self, angle_rad: float, angular_speed: float = 0.5):
        """Drehen um Winkel (positive = gegen Uhrzeiger)."""
        self._wait_for_pose()
        _, _, start_yaw = self.pose
        target_yaw = self._normalize_angle(start_yaw + angle_rad)

        while rclpy.ok():
            rclpy.spin_once(self, timeout_sec=0.0)
            _, _, yaw = self.pose
            err = self._normalize_angle(target_yaw - yaw)
            if abs(err) < self.ang_tol:
                break
            w = max(min(angular_speed, abs(err) * 1.5), 0.1) * (1.0 if err > 0 else -1.0)
            self._publish_cmd(0.0, w)
            time.sleep(self.dt)

        self.stop()
        self.get_logger().info("Rotation beendet.")

    def go_to_goal(self, goal_x, goal_y, v_max=0.2, w_max=0.8):
        """Fährt mit einfachem P-Regler zu einer Zielposition."""
        self._wait_for_pose()
        self.get_logger().info(f"Fahre zu Ziel: ({goal_x:.2f}, {goal_y:.2f})")

        while rclpy.ok():
            rclpy.spin_once(self, timeout_sec=0.0)
            if self.obstacle_distance < 0.25:
                self.get_logger().warn("Hindernis erkannt – Stoppe!")
                break

            x, y, yaw = self.pose
            dx, dy = goal_x - x, goal_y - y
            dist = math.hypot(dx, dy)

            if dist <= self.dist_tol:
                break

            desired = math.atan2(dy, dx)
            err_yaw = self._normalize_angle(desired - yaw)

            v = min(v_max, 0.4 * dist)
            w = max(min(w_max, 2.0 * err_yaw), -w_max)
            if abs(err_yaw) > 1.0:
                v = 0.0  # zuerst ausrichten

            self._publish_cmd(v, w)
            time.sleep(self.dt)

        self.stop()
        self.get_logger().info("Ziel erreicht oder gestoppt.")

    # ------------------- Hilfsfunktionen -------------------
    @staticmethod
    def _normalize_angle(a):
        a = math.fmod(a + math.pi, 2 * math.pi)
        if a < 0:
            a += 2 * math.pi
        return a - math.pi

    def shutdown(self):
        self.stop()
        self.destroy_node()
        self.get_logger().info("TurtleBot3Controller beendet.")


# ------------------- Hauptprogramm -------------------
def main():
    rclpy.init()
    node = TurtleBot3Controller()
    try:
        node.move_forward(0.5)
        node.rotate(math.pi / 2)
        node.go_to_goal(0.5, 0.0)
    finally:
        node.shutdown()
        rclpy.shutdown()


if __name__ == '__main__':
    main()

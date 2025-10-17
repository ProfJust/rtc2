#!/usr/bin/env python3
import subprocess
import math
import time
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose

class TurtlesimController(Node):
    """
    Steuerklasse für Turtlesim.
    - Publiziert Twist auf /turtle1/cmd_vel
    - Liest Pose von /turtle1/pose
    - Bietet Blocking-Kommandos: stop, move_forward, rotate, go_to_goal
    """

    def __init__(self, rate_hz: float = 30.0, dist_tol: float = 0.01, ang_tol: float = 0.01):
        super().__init__('turtlesim_controller')
        # # Turtlesim starten, falls er nicht läuft
        # self.get_logger().info("Starte turtlesim_node...")
        # self.sim_process = subprocess.Popen(
        #     ['ros2', 'run', 'turtlesim', 'turtlesim_node']
        # )

        time.sleep(2.0)  # kurze Pause zum Initialisieren
        self.cmd_pub = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        self.pose_sub = self.create_subscription(Pose, '/turtle1/pose', self._pose_cb, 10)

        self.rate_hz = float(rate_hz)
        self.dt = 1.0 / self.rate_hz
        self.distance_tolerance = float(dist_tol)
        self.angle_tolerance = float(ang_tol)

        self.pose = None  # wird im Callback gesetzt
        self._last_pose_time = time.time()

        self.get_logger().info('TurtlesimController bereit. Warte auf Pose...')

    # -------------------- Callbacks & Helpers --------------------

    def _pose_cb(self, msg: Pose):
        self.pose = msg
        self._last_pose_time = time.time()

    def _wait_for_pose(self, timeout: float = 5.0):
        """Wartet, bis mindestens eine Pose empfangen wurde."""
        start = time.time()
        while rclpy.ok() and self.pose is None and (time.time() - start) < timeout:
            rclpy.spin_once(self, timeout_sec=0.1)
        if self.pose is None:
            raise RuntimeError("Keine Pose empfangen. Läuft turtlesim_node? Topic: /turtle1/pose")

    @staticmethod
    def _normalize_angle(angle: float) -> float:
        """Winkel in [-pi, pi] falten."""
        a = math.fmod(angle + math.pi, 2.0 * math.pi)
        if a < 0:
            a += 2.0 * math.pi
        return a - math.pi

    # -------------------- Low-level Commands --------------------

    def stop(self):
        """Sofort stoppen (linear & angular = 0)."""
        msg = Twist()
        self.cmd_pub.publish(msg)

    def set_cmd(self, lin_x: float = 0.0, ang_z: float = 0.0):
        """Direkte Geschwindigkeitsvorgabe."""
        msg = Twist()
        msg.linear.x = float(lin_x)
        msg.angular.z = float(ang_z)
        self.cmd_pub.publish(msg)

    # -------------------- Blocking Motion Primitives --------------------

    def move_forward(self, distance: float, speed: float = 1.0):
        """
        Geradeaus um 'distance' Meter fahren (vorwärts bei distance>0, rückwärts bei distance<0).
        Begrenzung: |speed| <= 2.0
        """
        self._wait_for_pose()
        speed = max(min(abs(speed), 2.0), 0.05) * (1.0 if distance >= 0 else -1.0)

        start_x, start_y = self.pose.x, self.pose.y
        target_dist = abs(distance)

        while rclpy.ok():
            rclpy.spin_once(self, timeout_sec=0.0)

            # zurückgelegte Distanz
            dx = self.pose.x - start_x
            dy = self.pose.y - start_y
            d = math.hypot(dx, dy)

            if d >= target_dist - self.distance_tolerance:
                self.stop()
                break

            # sanft abbremsen in Zielnähe
            remaining = max(target_dist - d, 0.0)
            v = max(min(abs(speed), remaining * 1.5), 0.1) * (1.0 if speed >= 0 else -1.0)
            self.set_cmd(lin_x=v, ang_z=0.0)
            time.sleep(self.dt)

        self.stop()

    def rotate(self, angle_rad: float, angular_speed: float = 1.0):
        """
        In Place rotieren um 'angle_rad' (positiv = gegen Uhrzeiger).
        Begrenzung: |angular_speed| <= 3.0
        """
        self._wait_for_pose()
        angular_speed = max(min(abs(angular_speed), 3.0), 0.1) * (1.0 if angle_rad >= 0 else -1.0)

        start_theta = self.pose.theta
        target = self._normalize_angle(start_theta + angle_rad)

        while rclpy.ok():
            rclpy.spin_once(self, timeout_sec=0.0)
            err = self._normalize_angle(target - self.pose.theta)

            if abs(err) <= self.angle_tolerance:
                self.stop()
                break

            # sanft abbremsen
            w = max(min(abs(angular_speed), abs(err) * 2.0), 0.1) * (1.0 if err >= 0 else -1.0)
            self.set_cmd(lin_x=0.0, ang_z=w)
            time.sleep(self.dt)

        self.stop()

    def go_to_goal(self, goal_x: float, goal_y: float,
                   v_max: float = 1.5, w_max: float = 2.5,
                   kp_v: float = 1.0, kp_w: float = 3.0):
        """
        Fahre zum Ziel (goal_x, goal_y) mit einfacher P-Regelung:
        - v = kp_v * Distanz (gesättigt auf v_max)
        - w = kp_w * Winkel-Fehler (gesättigt auf w_max)
        """
        self._wait_for_pose()

        while rclpy.ok():
            rclpy.spin_once(self, timeout_sec=0.0)

            dx = goal_x - self.pose.x
            dy = goal_y - self.pose.y
            dist = math.hypot(dx, dy)

            if dist <= self.distance_tolerance:
                self.stop()
                self.get_logger().info("Ziel erreicht.")
                break

            # Zielrichtung
            desired = math.atan2(dy, dx)
            err_th = self._normalize_angle(desired - self.pose.theta)

            # P-Regler mit Sättigung
            v = max(min(kp_v * dist, v_max), 0.0)
            w_sign = 1.0 if err_th >= 0 else -1.0
            w = min(abs(kp_w * err_th), w_max) * w_sign

            # leichten Vorwärtsbias nur, wenn wir recht gut ausgerichtet sind
            if abs(err_th) > 1.0:  # ~57°
                v = min(v, 0.2)

            self.set_cmd(lin_x=v, ang_z=w)
            time.sleep(self.dt)

        self.stop()

    # -------------------- Shutdown --------------------

    def shutdown(self):
        self.get_logger().info("Shutdown...")
        self.stop()
        self.destroy_node()


# -------------------- Beispielnutzung --------------------

def main():
    rclpy.init()
    node = TurtlesimController(rate_hz=30.0, dist_tol=0.02, ang_tol=0.01)
    try:
        # Beispiele:
        # 1) 1 Meter vorwärts
        node.move_forward(1.0, speed=1.0)
        # 2) 90° links drehen
        node.rotate(math.pi / 2, angular_speed=1.0)
        # 3) Zum Punkt (x=5.5, y=5.5) fahren
        node.go_to_goal(2.5, 2.5)
    finally:
        node.shutdown()
        rclpy.shutdown()

if __name__ == "__main__":
    main()

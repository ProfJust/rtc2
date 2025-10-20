#!/usr/bin/env python3
import subprocess
import math
import time
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from sensor_msgs.msg import Joy

class TurtlesimController(Node):
    """
    Steuerklasse für Turtlesim.
    - Publiziert Twist auf /turtle1/cmd_vel
    - Liest Pose von /turtle1/pose
    - Bietet Blocking-Kommandos: stop, move_forward, rotate, go_to_goal
    """

    def __init__(self, rate_hz: float = 30.0, dist_tol: float = 0.01, ang_tol: float = 0.01):
        super().__init__('turtlesim_controller')
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
        msg.linear.x = 0.0
        msg.angular.z = 0.0
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


class JoyTeleop(Node):
    """
    ROS2 node: Abonniert /joy und veröffentlicht Twist auf /turtle1/cmd_vel.
    Konfigurierbare Achsen/Skalierung ermöglichen einfache Anpassung an verschiedene Gamepads.
    """
    def __init__(self,
                 topic_cmd: str = '/turtle1/cmd_vel',
                 axis_linear: int = 1,
                 axis_angular: int = 0,
                 scale_linear: float = 2.0,
                 scale_angular: float = 3.0,
                 deadzone: float = 0.12):
        super().__init__('joy_teleop')
        self.pub = self.create_publisher(Twist, topic_cmd, 10)
        self.sub = self.create_subscription(Joy, '/joy', self._joy_cb, 10)
        self.axis_linear = int(axis_linear)
        self.axis_angular = int(axis_angular)
        self.scale_linear = float(scale_linear)
        self.scale_angular = float(scale_angular)
        self.deadzone = float(deadzone)
        self.get_logger().info(f'JoyTeleop bereit. axes lin={self.axis_linear}, ang={self.axis_angular}')

    def _apply_deadzone(self, v: float) -> float:
        return 0.0 if abs(v) < self.deadzone else v

    def _joy_cb(self, msg: Joy):
        # Safely index axes
        ax_lin = msg.axes[self.axis_linear] if len(msg.axes) > self.axis_linear else 0.0
        ax_ang = msg.axes[self.axis_angular] if len(msg.axes) > self.axis_angular else 0.0

        ax_lin = self._apply_deadzone(ax_lin)
        ax_ang = self._apply_deadzone(ax_ang)

        # joystick forward usually negative
        lin = -ax_lin * self.scale_linear
        ang = -ax_ang * self.scale_angular

        twist = Twist()
        twist.linear.x = float(lin)
        twist.angular.z = float(ang)

        # Button 0 (A) immediate stop if present
        try:
            if len(msg.buttons) > 0 and msg.buttons[0]:
                twist.linear.x = 0.0
                twist.angular.z = 0.0
        except Exception:
            pass

        self.pub.publish(twist)


# -------------------- Beispielnutzung --------------------

def main():
    rclpy.init()
    node = TurtlesimController(rate_hz=30.0, dist_tol=0.02, ang_tol=0.01)
    try:
        # Beispiele:
        # 1) 1 Meter vorwärts
        #node.move_forward(1.0, speed=1.0)
        # 2) 90° links drehen
        #node.rotate(math.pi / 2, angular_speed=1.0)
        # 3) Zum Punkt (x=5.5, y=5.5) fahren
        node.go_to_goal(1, 7)
    finally:
        node.shutdown()
        rclpy.shutdown()

if __name__ == "__main__":
    rclpy.init()
    node = TurtlesimController(rate_hz=30.0, dist_tol=0.02, ang_tol=0.01)

    try:
        # Versuche pygame zu importieren und ein Gamepad zu benutzen.
        try:
            import pygame
        except Exception:
            node.get_logger().warn('pygame nicht gefunden. Starte stattdessen JoyTeleop (erwartet einen laufenden joy_node).')
            joy_node = JoyTeleop()
            try:
                rclpy.spin(joy_node)
            except KeyboardInterrupt:
                pass
            finally:
                joy_node.destroy_node()
        else:
            # pygame erfolgreich importiert -> nutze direkt Gamepad
            pygame.init()
            if pygame.joystick.get_count() == 0:
                node.get_logger().warn('Kein Gamepad gefunden. Führe Beispiel go_to_goal aus.')
                node.go_to_goal(1, 7)
            else:
                js = pygame.joystick.Joystick(0)
                js.init()
                node.get_logger().info(f'Gamepad verbunden: {js.get_name()}')

                # Konfiguration: Achsen-Mapping und Limits
                MAX_LIN = 2.0    # maximale lineare Geschwindigkeit
                MAX_ANG = 3.0    # maximale Winkelgeschwindigkeit
                DEADZONE = 0.12  # kleine Achsenwerte ignorieren
                rate = node.rate_hz

                def dz(v):
                    return 0.0 if abs(v) < DEADZONE else v

                node.get_logger().info('Steuerung: linker Stick vor/zurück = vorwärts/rückwärts, links/rechts = drehen')
                while rclpy.ok():
                    pygame.event.pump()
                    # Typical mapping: axis 1 = left stick vertical, axis 0 = left stick horizontal
                    try:
                        ax_y = js.get_axis(1)
                        ax_x = js.get_axis(0)
                    except Exception:
                        ax_y = 0.0
                        ax_x = 0.0

                    ax_y = dz(ax_y)
                    ax_x = dz(ax_x)

                    # Achsen-Normen: joystick nach vorn gibt negative Werte -> invertieren
                    lin = -ax_y * MAX_LIN
                    ang = -ax_x * MAX_ANG

                    # Button 0 (meist A) stoppt sofort
                    try:
                        if js.get_numbuttons() > 0 and js.get_button(0):
                            node.stop()
                        else:
                            node.set_cmd(lin_x=lin, ang_z=ang)
                    except Exception:
                        node.set_cmd(lin_x=lin, ang_z=ang)

                    rclpy.spin_once(node, timeout_sec=0.0)
                    time.sleep(1.0 / rate)
    except KeyboardInterrupt:
        pass
    finally:
        node.shutdown()
        rclpy.shutdown()

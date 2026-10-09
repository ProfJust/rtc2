# ROS2 Jazzy - Einfacher Subscriber für turtlesim
# Topic: /turtle1/pose

import rclpy
from turtlesim.msg import Pose


# Callback-Funktion: Wird bei jeder neuen Nachricht aufgerufen
def pose_callback(msg):
    print(f"Position: x={msg.x:.2f}, y={msg.y:.2f}, "
          f"Winkel={msg.theta:.2f} rad")


def main():
    # ROS2 initialisieren
    rclpy.init()

    # ROS2 Node erstellen
    node = rclpy.create_node("turtle_pose_subscriber")

    # Subscriber erstellen
    subscriber = node.create_subscription(
        Pose,                   # Nachrichtentyp
        "/turtle1/pose",        # Topic
        pose_callback,          # Callback-Funktion
        10                      # QoS Queue-Tiefe
    )

    print("Warte auf Pose-Daten von turtlesim ...")

    # Fortlaufend Nachrichten empfangen
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        print("\nSubscriber beendet.")

    # Aufräumen
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
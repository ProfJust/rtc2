# ROS2 Jazzy - TurtleSim Zufallsbewegung
# Publisher für /turtle1/cmd_vel

import rclpy
from geometry_msgs.msg import Twist
import random
import time


def main():

    # ROS2 initialisieren
    rclpy.init()

    # Node erstellen
    node = rclpy.create_node("turtle_random")

    # Publisher erstellen
    publisher = node.create_publisher(
        Twist,
        "/turtle1/cmd_vel",
        10
    )

    print("TurtleSim bewegt sich zufällig ...")
    print("Beenden mit STRG+C")

    try:
        while rclpy.ok():

            # Zufällige Geschwindigkeiten erzeugen
            v = random.uniform(0.5, 2.0)
            omega = random.uniform(-2.0, 2.0)

            # Twist-Nachricht erstellen
            msg = Twist()

            msg.linear.x = v
            msg.angular.z = omega

            # Nachricht veröffentlichen
            publisher.publish(msg)

            print(f"v = {v:.2f} m/s, "
                  f"omega = {omega:.2f} rad/s")

            # Eine Sekunde warten
            time.sleep(1.0)

    except KeyboardInterrupt:
        print("\nProgramm beendet.")

    finally:
        # Schildkröte anhalten
        msg = Twist()
        publisher.publish(msg)

        # ROS2 beenden
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
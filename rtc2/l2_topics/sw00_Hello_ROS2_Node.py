
import rclpy
from std_msgs.msg import String


def main():
    # ROS 2 initialisieren
    rclpy.init()

    # Node erzeugen
    node = rclpy.create_node("mein_publisher")

    # Publisher erzeugen
    publisher = node.create_publisher(String, "RTC_chatter", 10)

    # Nachricht vorbereiten
    nachricht = String()

    zaehler = 0

    try:
        while rclpy.ok():
            zaehler += 1
            nachricht.data = f"Hallo ROS 2! Nachricht {zaehler}"

            # Nachricht senden
            publisher.publish(nachricht)

            print(nachricht.data)

            # Eine Sekunde warten
            import time
            time.sleep(1.0)

    except KeyboardInterrupt:
        pass

    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()

from rtc2.my_class_files.TurtlesimController import TurtlesimController
import rclpy


rclpy.init()
node = TurtlesimController(rate_hz=30.0, dist_tol=0.02, ang_tol=0.01)
        # Beispiele:
        # 1) 1 Meter vorwärts
        #node.move_forward(1.0, speed=1.0)
        # 2) 90° links drehen
        #node.rotate(math.pi / 2, angular_speed=1.0)
        # 3) Zum Punkt (x=5.5, y=5.5) fahren
node.go_to_goal(7, 1)
node.shutdown()
rclpy.shutdown()
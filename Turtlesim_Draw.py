import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.srv import SetPen, TeleportAbsolute
import time

class TurtleSim(Node):
    def __init__(self):
        super().__init__('turtle_star')
        self.move = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        self.set_pen = self.create_client(SetPen, '/turtle1/set_pen')
        self.set_teleport = self.create_client(TeleportAbsolute, '/turtle1/teleport_absolute')
        
        time.sleep(1)
        self.draw_stars()

    def pen(self, r, g, b, width, off):
        request = SetPen.Request()
        request.r = r
        request.g = g
        request.b = b
        request.width = width
        request.off = off
        self.set_pen.call_async(request)

    def teleport(self, x, y, theta):
        request = TeleportAbsolute.Request()
        request.x = x
        request.y = y
        request.theta = theta
        self.set_teleport.call_async(request)

    def draw_star(self, size):
        msg = Twist()
        for i in range(5):
            msg.linear.x = size
            msg.angular.z = 0.0
            self.move.publish(msg)
            time.sleep(3)

            msg.linear.x = 0.0
            self.move.publish(msg)

            msg.angular.z = 2.5132741229
            self.move.publish(msg)
            time.sleep(1.2)

            msg.angular.z = 0.0
            self.move.publish(msg)

    def draw_stars(self):
        teleport_points = [
            (4.0, 5.0, 0.0),
            (5.4, 7.0, 0.0),
            (6.2, 5.2, 0.0)
        ]
        
        sizes = [1.4, 2.0, 0.8]

        for i in range(3):
            self.pen(0, 0, 0, 0, 1)
            time.sleep(1)

            x, y, theta = teleport_points[i]
            self.teleport(x, y, theta)
            time.sleep(1)

            self.pen(255, 255, 0, 2, 0)
            time.sleep(1)

            self.draw_star(sizes[i])
        
        self.pen(0, 0, 0, 0, 1)
        time.sleep(1)

        self.teleport(0.0, 0.0, 0.0)
        time.sleep(1)

def main():
    rclpy.init()
    node = TurtleSim()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
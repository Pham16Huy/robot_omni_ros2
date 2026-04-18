import math
import yaml
import rclpy
from rclpy.parameter import Parameter
from rclpy.node import Node
from rclpy.action import ActionClient
from nav2_msgs.action import NavigateToPose
from geometry_msgs.msg import PoseStamped
from ament_index_python.packages import get_package_share_directory
import os


class GoToRoom(Node):
    def __init__(self):
        super().__init__('go_to_room')

        self.declare_parameter('room_name', 'room1')
        if not self.has_parameter('use_sim_time'):
            self.declare_parameter('use_sim_time', True)
        self.set_parameters([
            Parameter(
                'use_sim_time',
                Parameter.Type.BOOL,
                True
            )
        ])

        pkg_share = get_package_share_directory('nav2_simple_navigation')
        rooms_file = os.path.join(pkg_share, 'config', 'rooms.yaml')

        with open(rooms_file, 'r') as f:
            self.rooms_data = yaml.safe_load(f)
        
        self.room_name = self.get_parameter('room_name').value
        self.client = ActionClient(self, NavigateToPose, 'navigate_to_pose')

    def send_goal(self):
        rooms = self.rooms_data['rooms']

        if self.room_name not in rooms:
            self.get_logger().error(f'Room {self.room_name} not found')
            return
        room = rooms[self.room_name]

        x = float(room['x'])
        y = float(room['y'])
        yaw = float(room['yaw'])

        frame_id = room.get('frame_id', 'map')
        goal_msg = NavigateToPose.Goal()
        pose = PoseStamped()
        pose.header.frame_id = frame_id
        pose.header.stamp = self.get_clock().now().to_msg()


        pose.pose.position.x = x
        pose.pose.position.y = y
        pose.pose.position.z = 0.0

        pose.pose.orientation.z = math.sin(yaw / 2.0)
        pose.pose.orientation.w = math.cos(yaw / 2.0)

        goal_msg.pose = pose


        self.client.wait_for_server()

        future = self.client.send_goal_async(goal_msg)
        rclpy.spin_until_future_complete(self, future)

        goal_handle = future.result()

        if not goal_handle.accepted:
            self.get_logger().error('Goal rejected')
            return
        self.get_logger().info(f'Goting to {self.room_name}: x={x}, y={y}, yaw={yaw}')
        result_future = goal_handle.get_result_async()
        rclpy.spin_until_future_complete(self, result_future)

        result = result_future.result().result
        self.get_logger().info(f'Navigation finished, error_code={result.error_code}')
def main(args=None):
    rclpy.init(args=args)
    node = GoToRoom()
    node.send_goal()
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
    

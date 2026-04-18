import math
import os

import rclpy
import yaml
from ament_index_python.packages import get_package_share_directory
from geometry_msgs.msg import PoseStamped
from nav2_msgs.action import NavigateToPose
from rclpy.action import ActionClient
from rclpy.node import Node
from rclpy.parameter import Parameter


class GoToRooms(Node):
    def __init__(self):
        super().__init__('go_to_rooms')

        self.declare_parameter('room_sequence', 'room1,room2')
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

        with open(rooms_file, 'r') as file:
            self.rooms_data = yaml.safe_load(file)

        self.room_sequence = self._parse_room_sequence(
            self.get_parameter('room_sequence').value
        )
        self.client = ActionClient(self, NavigateToPose, 'navigate_to_pose')

    def _parse_room_sequence(self, raw_sequence):
        return [room.strip() for room in raw_sequence.split(',') if room.strip()]

    def _build_goal(self, room_name):
        rooms = self.rooms_data.get('rooms', {})
        if room_name not in rooms:
            self.get_logger().error(f'Room {room_name} not found in rooms.yaml')
            return None

        room = rooms[room_name]
        x = float(room['x'])
        y = float(room['y'])
        yaw = float(room['yaw'])
        frame_id = room.get('frame_id', 'map')

        pose = PoseStamped()
        pose.header.frame_id = frame_id
        pose.header.stamp = self.get_clock().now().to_msg()
        pose.pose.position.x = x
        pose.pose.position.y = y
        pose.pose.position.z = float(room.get('z', 0.0))
        pose.pose.orientation.z = math.sin(yaw / 2.0)
        pose.pose.orientation.w = math.cos(yaw / 2.0)

        goal_msg = NavigateToPose.Goal()
        goal_msg.pose = pose
        return goal_msg

    def run_sequence(self):
        if not self.room_sequence:
            self.get_logger().error(
                'room_sequence is empty. Example: room1,room3,room5'
            )
            return

        self.get_logger().info(
            f'Waiting for navigate_to_pose server for route: {self.room_sequence}'
        )
        self.client.wait_for_server()

        total_rooms = len(self.room_sequence)
        for index, room_name in enumerate(self.room_sequence, start=1):
            goal_msg = self._build_goal(room_name)
            if goal_msg is None:
                self.get_logger().error(
                    f'Stopping route because "{room_name}" is invalid'
                )
                return

            self.get_logger().info(
                f'Navigating to {room_name} ({index}/{total_rooms})'
            )
            send_future = self.client.send_goal_async(goal_msg)
            rclpy.spin_until_future_complete(self, send_future)
            goal_handle = send_future.result()

            if goal_handle is None or not goal_handle.accepted:
                self.get_logger().error(
                    f'Goal for {room_name} was rejected, stopping route'
                )
                return

            result_future = goal_handle.get_result_async()
            rclpy.spin_until_future_complete(self, result_future)
            result_response = result_future.result()

            if result_response is None:
                self.get_logger().error(
                    f'No result returned for {room_name}, stopping route'
                )
                return

            error_code = result_response.result.error_code
            if error_code != 0:
                self.get_logger().error(
                    f'Navigation to {room_name} failed with error_code={error_code}'
                )
                return

            self.get_logger().info(f'Arrived at {room_name}')

        self.get_logger().info('Completed all rooms in sequence')


def main(args=None):
    rclpy.init(args=args)
    node = GoToRooms()
    node.run_sequence()
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()

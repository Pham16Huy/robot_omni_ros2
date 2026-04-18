import copy

import rclpy
from action_msgs.msg import GoalStatus
from geometry_msgs.msg import PointStamped, PoseStamped
from nav2_msgs.action import NavigateToPose
from nav_msgs.msg import Path
from rclpy.action import ActionClient
from rclpy.node import Node
from rclpy.parameter import Parameter


class RvizRouteManager(Node):
    def __init__(self):
        super().__init__('rviz_route_manager')

        if not self.has_parameter('use_sim_time'):
            self.declare_parameter('use_sim_time', True)
        self.set_parameters([
            Parameter(
                'use_sim_time',
                Parameter.Type.BOOL,
                True
            )
        ])

        self.route_goals = []
        self.executing = False
        self.current_goal_handle = None

        self.client = ActionClient(self, NavigateToPose, 'navigate_to_pose')

        self.route_goal_sub = self.create_subscription(
            PoseStamped,
            '/route_goal',
            self.on_route_goal,
            10
        )
        self.route_start_sub = self.create_subscription(
            PointStamped,
            '/route_start',
            self.on_route_start,
            10
        )
        self.route_clear_sub = self.create_subscription(
            PointStamped,
            '/route_clear',
            self.on_route_clear,
            10
        )
        self.route_cancel_sub = self.create_subscription(
            PointStamped,
            '/route_cancel',
            self.on_route_cancel,
            10
        )

        self.route_path_pub = self.create_publisher(Path, '/route_queue', 10)
        self.publish_route_queue()

    def publish_route_queue(self):
        path = Path()
        if self.route_goals:
            path.header = copy.deepcopy(self.route_goals[0].header)
            path.poses = [copy.deepcopy(goal) for goal in self.route_goals]
        else:
            path.header.frame_id = 'map'
            path.header.stamp = self.get_clock().now().to_msg()
            path.poses = []

        self.route_path_pub.publish(path)

    def on_route_goal(self, msg):
        goal = copy.deepcopy(msg)
        self.route_goals.append(goal)
        self.publish_route_queue()
        self.get_logger().info(
            f'Added route waypoint #{len(self.route_goals)}'
        )

    def on_route_start(self, _msg):
        if self.executing:
            self.get_logger().warn('Route is already running')
            return

        if not self.route_goals:
            self.get_logger().warn('Route queue is empty')
            return

        self.get_logger().info(
            f'Starting route with {len(self.route_goals)} waypoint(s)'
        )
        self.executing = True

        if not self.client.wait_for_server(timeout_sec=2.0):
            self.get_logger().error('navigate_to_pose action server is not ready')
            self.executing = False
            return

        self.send_next_goal()

    def send_next_goal(self):
        if not self.executing:
            return

        if not self.route_goals:
            self.get_logger().info('Route completed')
            self.current_goal_handle = None
            self.executing = False
            self.publish_route_queue()
            return

        next_pose = self.route_goals.pop(0)
        self.publish_route_queue()

        goal_msg = NavigateToPose.Goal()
        goal_msg.pose = next_pose

        self.get_logger().info(
            f'Sending route waypoint, {len(self.route_goals)} remaining after this'
        )
        send_future = self.client.send_goal_async(goal_msg)
        send_future.add_done_callback(self.on_goal_response)

    def on_goal_response(self, future):
        goal_handle = future.result()

        if goal_handle is None or not goal_handle.accepted:
            self.get_logger().error('Route waypoint was rejected')
            self.executing = False
            self.current_goal_handle = None
            return

        self.current_goal_handle = goal_handle
        result_future = goal_handle.get_result_async()
        result_future.add_done_callback(self.on_goal_result)

    def on_goal_result(self, future):
        result_response = future.result()
        self.current_goal_handle = None

        if result_response is None:
            self.get_logger().error('Route waypoint returned no result')
            self.executing = False
            return

        status = result_response.status
        result = result_response.result
        if status != GoalStatus.STATUS_SUCCEEDED:
            self.get_logger().error(
                f'Route stopped, waypoint finished with status={status}, '
                f'error_code={result.error_code}'
            )
            self.executing = False
            return

        if result.error_code != 0:
            self.get_logger().error(
                f'Route stopped, waypoint failed with error_code={result.error_code}'
            )
            self.executing = False
            return

        self.get_logger().info('Route waypoint reached successfully')
        self.send_next_goal()

    def on_route_clear(self, _msg):
        if self.executing:
            self.get_logger().warn(
                'Route is running. Use Route Cancel to stop current route.'
            )
            return

        self.route_goals.clear()
        self.publish_route_queue()
        self.get_logger().info('Cleared route queue')

    def on_route_cancel(self, _msg):
        self.route_goals.clear()
        self.publish_route_queue()

        if self.current_goal_handle is None:
            self.executing = False
            self.get_logger().info('Canceled route queue')
            return

        cancel_future = self.current_goal_handle.cancel_goal_async()
        cancel_future.add_done_callback(self.on_cancel_done)
        self.get_logger().info('Canceling active route')

    def on_cancel_done(self, _future):
        self.executing = False
        self.current_goal_handle = None
        self.get_logger().info('Active route canceled')


def main(args=None):
    rclpy.init(args=args)
    node = RvizRouteManager()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()

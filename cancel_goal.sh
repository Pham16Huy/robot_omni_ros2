cd /home/huy/Downloads/project
source install/setup.bash
ros2 service call /navigate_to_pose/_action/cancel_goal action_msgs/srv/CancelGoal "{goal_info: {goal_id: {uuid: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]}, stamp: {sec: 0, nanosec: 0}}}"
ros2 topic pub --once /mobile_base_controller/reference geometry_msgs/msg/TwistStamped "{header: {frame_id: 'base_footprint'}, twist: {linear: {x: 0.0, y: 0.0, z: 0.0}, angular: {x: 0.0, y: 0.0, z: 0.0}}}"
ros2 topic pub --once /plan nav_msgs/msg/Path "{header: {frame_id: 'map'}, poses: []}"
ros2 topic pub --once /local_plan nav_msgs/msg/Path "{header: {frame_id: 'odom'}, poses: []}"

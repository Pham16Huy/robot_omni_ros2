
ROOM_NAME=$1
cd /home/huy/Downloads/project 
source install/setup.bash
ros2 run nav2_simple_navigation go_to_room --ros-args -p room_name:=${ROOM_NAME}

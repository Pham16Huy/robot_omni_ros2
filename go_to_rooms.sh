
if [ "$#" -lt 1 ]; then
  echo "Usage: ./go_to_rooms.sh room1 room3 room7"
  exit 1
fi

ROOM_SEQUENCE=$(IFS=, ; echo "$*")

cd /home/huy/Downloads/project
source install/setup.bash
ros2 run nav2_simple_navigation go_to_rooms --ros-args -p room_sequence:="${ROOM_SEQUENCE}"

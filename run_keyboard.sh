cd /home/huy/Downloads/project || exit 1
source install/setup.bash

ros2 run twist_stamper twist_stamper \
  --ros-args \
  -r cmd_vel_in:=/cmd_vel \
  -r cmd_vel_out:=/mobile_base_controller/reference &
STAMPER_PID=$!

cleanup() {
  kill "$STAMPER_PID" 2>/dev/null
}

trap cleanup EXIT INT TERM

ros2 run teleop_twist_keyboard teleop_twist_keyboard

cd /home/huy/Downloads/project 
colcon build --packages-select robot_omni
cd /home/huy/Downloads/project 
source install/setup.bash
ros2 launch robot_omni hopistal_gazebo_control.launch.py
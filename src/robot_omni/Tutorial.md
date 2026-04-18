
Cách chạy:
Mở terminal trong vscode -> bash1: pkill -9 -f 'gz|ruby'
mv ~/.gz ~/.gz_backup_$(date +%s)
./run_robot_omni.sh hospital_full.world

-> +bash2 ->./run_nav2.sh -> +bash3 -> ./render_map.sh(bắt buộc).

Muốn chức năng nào thì chạy chức năng đó:

+ Điều khiển bằng bàn phím.

+bash -> ./run_keyboard.sh
+ Cho robot đi 1 phòng dựa trên rooms.yaml.
Dùng:

+bash -> ./go_to_room.sh room1

+ Cho robot đi chuỗi phòng (đầu vào là nhiều tên phòng).
Dùng:

+bash -> ./go_to_rooms.sh room1 room3 room7

+ Hủy goal đang chạy + dừng robot + clear path.
Dùng:u

+bash -> ./cancel_goal.sh

+ Kill toàn bộ tiến trình ROS/Gazebo/RViz liên quan.can
Dùng:

+bash -> ./stop.sh

Nếu lỗi:
“Permission denied”.

Chạy một lần:
chmod +x go_to_rooms.sh
Rồi dùng:
./go_to_rooms.sh room1 room3 room7


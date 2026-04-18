## Team Members / Thành Viên Nhóm

| # | Name / Tên | Student ID / MSSV |
|---|------------|------------------|
| 1 | Phạm Đức Huy | 23134026 |
| 2 | Vũ Phạm Đức Văn | 23134064 |
| 3 | Trương Hồng Lĩnh | 23134035 |

---
# Autonomous Robot Navigation System in Hospital Environment

## Mục Lục / Table of Contents
1. [Project Overview / Tổng Quan Dự Án](#project-overview)
2. [System Requirements / Yêu Cầu Hệ Thống](#system-requirements)
3. [Installation / Cài Đặt](#installation)
4. [Quick Start / Hướng Dẫn Chạy Nhanh](#quick-start)
5. [Available Commands / Các Lệnh Có Sẵn](#available-commands)
6. [Robot Specifications / Thông Số Kỹ Thuật Robot](#robot-specifications)
7. [Project Structure / Cấu Trúc Dự Án](#project-structure)
8. [Team Members / Thành Viên Nhóm](#team-members)

---
## Project Overview

### English
This project implements an **autonomous robot navigation system** designed for hospital environments using ROS2 (Humble/Jazzy). The system enables a Mecanum wheel omnidirectional robot to:
- Navigate autonomously using the Nav2 navigation stack
- Avoid obstacles and adapt to dynamic environments
- Follow predefined room sequences in hospital layouts
- Respond to keyboard controls for manual operation
- Use SLAM for mapping and localization

The robot is simulated in **Gazebo** with a realistic hospital_full.world environment including dynamic obstacles.

### Tiếng Việt
Dự án này triển khai một **hệ thống điều hướng robot tự động** được thiết kế cho môi trường bệnh viện sử dụng ROS2. Hệ thống cho phép robot bánh xe Mecanum (2 chiều) thực hiện:
- Điều hướng tự động bằng ngăn xếp Nav2
- Tránh chướng ngại vật và thích ứng với môi trường động
- Theo một chuỗi phòng được định nghĩa trước trong bố cục bệnh viện
- Phản ứng với điều khiển bàn phím cho hoạt động thủ công
- Sử dụng SLAM để xây dựng bản đồ và định vị

Robot được mô phỏng trong **Gazebo** với môi trường hospital_full.world thực tế bao gồm các chướng ngại vật động.

---

## System Requirements

### English
- **OS**: Ubuntu 22.04 LTS or higher
- **ROS2**: Jazzy Jalisco (or Humble Hawksbill)
- **Gazebo**: Version 8+ (simulator-gazebo)
- **Python**: 3.10+
- **Required Packages**:
  - `ros2-base`
  - `gazebo`
  - `nav2`
  - `rviz2`
  - `colcon`

### Tiếng Việt
- **OS**: Ubuntu 22.04 LTS hoặc cao hơn
- **ROS2**: Jazzy Jalisco (hoặc Humble Hawksbill)
- **Gazebo**: Phiên bản 8+ (simulator-gazebo)
- **Python**: 3.10+
- **Gói Yêu Cầu**:
  - `ros2-base`
  - `gazebo`
  - `nav2`
  - `rviz2`
  - `colcon`

---

## Installation

### English

1. **Clone the repository**:
   ```bash
   cd ~/Downloads
   git clone <repository-url>
   cd project
   ```

2. **Install ROS2 dependencies**:
   ```bash
   rosdep update
   rosdep install --from-paths src --ignore-src -y
   ```

3. **Build the workspace**:
   ```bash
   colcon build --symlink-install
   source install/local_setup.bash
   ```

4. **Fix Gazebo cache issues** (if needed):
   ```bash
   pkill -9 -f 'gz|ruby'
   mv ~/.gz ~/.gz_backup_$(date +%s)
   ```

### Tiếng Việt

1. **Sao chép kho lưu trữ**:
   ```bash
   cd ~/Downloads
   git clone <repository-url>
   cd project
   ```

2. **Cài đặt các phụ thuộc ROS2**:
   ```bash
   rosdep update
   rosdep install --from-paths src --ignore-src -y
   ```

3. **Xây dựng không gian làm việc**:
   ```bash
   colcon build --symlink-install
   source install/local_setup.bash
   ```

4. **Khắc phục sự cố bộ đệm Gazebo** (nếu cần):
   ```bash
   pkill -9 -f 'gz|ruby'
   mv ~/.gz ~/.gz_backup_$(date +%s)
   ```

---

## Quick Start

### English

To run the complete system, open **4 separate terminals** and execute the following in order:

#### Terminal 1 - Launch Gazebo with Robot
```bash
./run_robot_omni.sh hospital_full.world
```
This starts the Gazebo simulator with the hospital environment and spawns the Mecanum robot.

#### Terminal 2 - Launch Navigation Stack
```bash
./run_nav2.sh
```
This starts the Nav2 navigation stack with the configured controller and planner.

#### Terminal 3 - Launch RViz Visualization
```bash
./render_map.sh
```
This opens RViz to visualize the robot, map, and navigation goals.

#### Terminal 4 (Optional) - Send navigation commands:
```bash
# Navigate to a single room
./go_to_room.sh room1

# Navigate to multiple rooms in sequence
./go_to_rooms.sh room1 room3 room7

# Keyboard control
./run_keyboard.sh
```

#### System Shutdown
To stop all ROS/Gazebo processes:
```bash
./stop.sh
```

### Tiếng Việt

Để chạy hệ thống hoàn chỉnh, hãy mở **4 terminal riêng biệt** và thực thi theo thứ tự sau:

#### Terminal 1 - Khởi động Gazebo với Robot
```bash
./run_robot_omni.sh hospital_full.world
```
Điều này bắt đầu trình mô phỏng Gazebo với môi trường bệnh viện và tạo ra robot Mecanum.

#### Terminal 2 - Khởi động ngăn xếp điều hướng
```bash
./run_nav2.sh
```
Điều này bắt đầu ngăn xếp điều hướng Nav2 với bộ điều khiển và hộp riêng được định cấu hình.

#### Terminal 3 - Khởi động trực quan hóa RViz
```bash
./render_map.sh
```
Cái này mở RViz để trực quan hóa robot, bản đồ và các mục tiêu điều hướng.

#### Terminal 4 (Tùy chọn) - Gửi lệnh điều hướng:
```bash
# Điều hướng đến một phòng
./go_to_room.sh room1

# Điều hướng đến nhiều phòng liên tiếp
./go_to_rooms.sh room1 room3 room7

# Điều khiển bằng bàn phím
./run_keyboard.sh
```

#### Tắt Hệ Thống
Để dừng tất cả các quy trình ROS/Gazebo:
```bash
./stop.sh
```

---

## Available Commands

### English

| Command | Description | Usage |
|---------|-------------|-------|
| `run_robot_omni.sh` | Launch Gazebo simulator with hospital environment | `./run_robot_omni.sh hospital_full.world` |
| `run_nav2.sh` | Start the Nav2 navigation stack | `./run_nav2.sh` |
| `render_map.sh` | Open RViz visualization | `./render_map.sh` |
| `go_to_room.sh` | Navigate to a specific room | `./go_to_room.sh room1` |
| `go_to_rooms.sh` | Navigate to multiple rooms in sequence | `./go_to_rooms.sh room1 room3 room7` |
| `run_keyboard.sh` | Manual keyboard control of robot | `./run_keyboard.sh` |
| `cancel_goal.sh` | Cancel current navigation goal | `./cancel_goal.sh` |
| `run_slam.sh` | Run SLAM for mapping | `./run_slam.sh` |
| `run_control.sh` | Run robot control systems | `./run_control.sh` |
| `run_ekf.sh` | Run Extended Kalman Filter localization | `./run_ekf.sh` |
| `move.sh` | Activate dynamic obstacles for testing | `./move.sh` |
| `save_map.sh` | Save the current map | `./save_map.sh` |
| `debug_pose.sh` | Debug robot pose information | `./debug_pose.sh` |
| `stop.sh` | Kill all ROS/Gazebo processes | `./stop.sh` |

### Tiếng Việt

| Lệnh | Mô Tả | Cách Sử Dụng |
|------|-------|------------|
| `run_robot_omni.sh` | Khởi động trình mô phỏng Gazebo với môi trường bệnh viện | `./run_robot_omni.sh hospital_full.world` |
| `run_nav2.sh` | Khởi động ngăn xếp điều hướng Nav2 | `./run_nav2.sh` |
| `render_map.sh` | Mở trực quan hóa RViz | `./render_map.sh` |
| `go_to_room.sh` | Điều hướng đến một phòng cụ thể | `./go_to_room.sh room1` |
| `go_to_rooms.sh` | Điều hướng đến nhiều phòng liên tiếp | `./go_to_rooms.sh room1 room3 room7` |
| `run_keyboard.sh` | Điều khiển robot bằng bàn phím thủ công | `./run_keyboard.sh` |
| `cancel_goal.sh` | Hủy bỏ mục tiêu điều hướng hiện tại | `./cancel_goal.sh` |
| `run_slam.sh` | Chạy SLAM để xây dựng bản đồ | `./run_slam.sh` |
| `run_control.sh` | Chạy các hệ thống điều khiển robot | `./run_control.sh` |
| `run_ekf.sh` | Chạy bộ lọc Kalman mở rộng để định vị | `./run_ekf.sh` |
| `move.sh` | Kích hoạt các chướng ngại vật động để thử nghiệm | `./move.sh` |
| `save_map.sh` | Lưu bản đồ hiện tại | `./save_map.sh` |
| `debug_pose.sh` | Gỡ lỗi thông tin tư thế robot | `./debug_pose.sh` |
| `stop.sh` | Tắt tất cả các quy trình ROS/Gazebo | `./stop.sh` |

---

## Robot Specifications

### English

**Robot Type**: Omnidirectional Mecanum Wheel Robot
- **Wheels**: 4 Mecanum wheels
- **Drive Type**: Holonomic (can move in any direction)
- **Max Linear Velocity**: 4.0 m/s (configured)
- **Max Angular Velocity**: 1.5 rad/s (configured)
- **Payload**: 20 kg (simulation)
- **Sensors**:
  - 2D LiDAR (scanning range 3.0 m)
  - IMU (accelerometer, gyroscope)
  - Wheel encoders for odometry

**Navigation Stack**: ROS2 Nav2
- **Planner**: GridBased (NavfnPlanner)
- **Controller**: RegulatedPurePursuit (RPPC)
- **Recovery Behaviors**: Spin recovery on obstacles
- **Localization**: EKF with sensor fusion

**Simulation Environment**: Gazebo
- **World**: hospital_full.world with hospital layout
- **Dynamic Obstacles**: Moving patients and staff (PatientWheelChair_1, Scrubs_6)
- **Physics Engine**: ODE solver

### Tiếng Việt

**Loại Robot**: Robot Bánh Xe Mecanum Toàn hướng
- **Bánh xe**: 4 bánh xe Mecanum
- **Loại Lái xe**: Holonomic (có thể di chuyển theo bất kỳ hướng nào)
- **Vận tốc Tuyến tính Tối đa**: 4.0 m/s (được định cấu hình)
- **Vận tốc Góc Tối đa**: 1.5 rad/s (được định cấu hình)
- **Tải trọng**: 20 kg (mô phỏng)
- **Cảm biến**:
  - LiDAR 2D (phạm vi quét 3.0 m)
  - IMU (gia tốc kế, con quay hồi chuyển)
  - Bộ mã hóa bánh xe để đo quãng đường

**Ngăn xếp Điều hướng**: ROS2 Nav2
- **Hộ**: GridBased (NavfnPlanner)
- **Bộ điều khiển**: RegulatedPurePursuit (RPPC)
- **Hành vi Phục hồi**: Khôi phục Spin khi có chướng ngại vật
- **Định vị**: EKF với hợp nhất cảm biến

**Môi trường Mô phỏng**: Gazebo
- **Thế giới**: hospital_full.world với bố cục bệnh viện
- **Chướng ngại vật Động**: Bệnh nhân và nhân viên di chuyển (PatientWheelChair_1, Scrubs_6)
- **Công cụ Vật lý**: Giải pháp ODE

---

## Project Structure

```
project/
├── README.md                                    # This file
├── src/
│   ├── robot_omni/                            # Robot description and control
│   │   ├── launch/                            # Launch files
│   │   │   ├── hopistal_gazebo_control.launch.py
│   │   │   └── ...
│   │   ├── urdf/                              # Robot URDF description
│   │   │   └── omni_base.urdf
│   │   ├── config/                            # Configuration files
│   │   │   ├── bridge_config.yaml
│   │   │   └── configuration.yaml
│   │   ├── worlds/                            # Gazebo world files
│   │   │   └── hospital_full.world
│   │   └── package.xml
│   │
│   └── nav2_simple_navigation/               # Navigation stack
│       ├── launch/                            # Navigation launch files
│       ├── config/                            # Nav2 parameters
│       │   └── nav2_params.yaml
│       ├── behavior_tree/                     # Behavior trees
│       │   └── navigate_smart.xml
│       ├── rviz/                              # RViz configurations
│       └── package.xml
│
├── build/                                      # Compiled binaries
├── install/                                    # Installed packages
├── log/                                        # Build and runtime logs
│
├── run_robot_omni.sh                          # Launch robot in Gazebo
├── run_nav2.sh                                # Launch navigation stack
├── render_map.sh                              # Launch RViz visualization
├── go_to_room.sh                              # Send goal to single room
├── go_to_rooms.sh                             # Send goal to multiple rooms
├── run_keyboard.sh                            # Keyboard control
├── run_slam.sh                                # Run SLAM
├── cancel_goal.sh                             # Cancel navigation goal
├── move.sh                                    # Activate dynamic obstacles
├── save_map.sh                                # Save map
├── debug_pose.sh                              # Debug robot pose
├── stop.sh                                    # Stop all processes
└── ...
```

## Troubleshooting

### English

**Issue**: "Permission denied" when running scripts
**Solution**: Make scripts executable
```bash
chmod +x *.sh
```

**Issue**: Gazebo crashes or responds slowly
**Solution**: Clear Gazebo cache
```bash
pkill -9 -f 'gz|ruby'
mv ~/.gz ~/.gz_backup_$(date +%s)
```

**Issue**: Robot doesn't respond to navigation goals
**Solution**: Ensure all terminals are running and Nav2 stack is healthy
```bash
ros2 topic list | grep nav2
```

### Tiếng Việt

**Vấn đề**: "Permission denied" khi chạy tập lệnh
**Giải pháp**: Làm cho các tập lệnh có thể thực thi
```bash
chmod +x *.sh
```

**Vấn đề**: Gazebo bị sập hoặc phản ứng chậm
**Giải pháp**: Xóa bộ đệm Gazebo
```bash
pkill -9 -f 'gz|ruby'
mv ~/.gz ~/.gz_backup_$(date +%s)
```

**Vấn đề**: Robot không phản ứng với các mục tiêu điều hướng
**Giải pháp**: Đảm bảo tất cả các terminal đang chạy và ngăn xếp Nav2 khỏe mạnh
```bash
ros2 topic list | grep nav2
```

---

## License

This project is distributed under the [MIT License](LICENSE).

---

## Contact / Liên Hệ

For questions or contributions, please contact the team or open an issue in the repository.

---

**Last Updated**: April 2026

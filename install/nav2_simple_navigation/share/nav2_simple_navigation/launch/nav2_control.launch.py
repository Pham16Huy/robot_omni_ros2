from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os


def generate_launch_description():

    # Get package path
    pkg_share = get_package_share_directory('nav2_simple_navigation')
    workspace_root = os.path.abspath(
        os.path.join(pkg_share, '..', '..', '..', '..')
    )

    # Config files
    ekf_config = os.path.join(pkg_share, 'config', 'ekf.yaml')
    nav2_config = os.path.join(pkg_share, 'config', 'nav2_params.yaml')
    rviz_config = os.path.join(pkg_share, 'rviz', 'nav2_navigation.rviz')
    src_rviz_config = os.path.join(
        workspace_root,
        'src',
        'nav2_simple_navigation',
        'rviz',
        'nav2_navigation.rviz'
    )
    if os.path.exists(src_rviz_config):
        rviz_config = src_rviz_config

    # Map file
    map_file = os.path.join(pkg_share, 'config', 'hospital_map.yaml')

    use_rviz = LaunchConfiguration('use_rviz')

    # -------------------------
    # EKF node
    # -------------------------
    ekf_node = Node(
        package='robot_localization',
        executable='ekf_node',
        name='ekf_filter_node',
        output='screen',
        parameters=[ekf_config, {'use_sim_time': True}]
    )

    # -------------------------
    # Nav2 nodes
    # -------------------------
    planner_node = Node(
        package='nav2_planner',
        executable='planner_server',
        name='planner_server',
        output='screen',
        parameters=[nav2_config]
    )

    controller_node = Node(
        package='nav2_controller',
        executable='controller_server',
        name='controller_server',
        output='screen',
        parameters=[nav2_config],
        remappings=[('/cmd_vel', '/mobile_base_controller/reference')]
    )

    recoveries_node = Node(
        package='nav2_behaviors',
        executable='behavior_server',
        name='recoveries_server',
        output='screen',
        parameters=[nav2_config],
    )
    bt_navigator_node = Node(
        package='nav2_bt_navigator',
        executable='bt_navigator',
        name='bt_navigator',
        output='screen',
        parameters=[nav2_config]
    )

    rviz_route_manager_node = Node(
        package='nav2_simple_navigation',
        executable='rviz_route_manager',
        name='rviz_route_manager',
        output='screen',
        parameters=[{'use_sim_time': True}]
    )

    #  Node map server
    map_server_node = Node(
        package='nav2_map_server',
        executable='map_server',
        name='map_server',
        output='screen',
        parameters=[
            {'use_sim_time': True},
            {'yaml_filename': map_file}
        ]
    )

    # Node amcl
    amcl_node = Node(
        package='nav2_amcl',
        executable='amcl',
        name='amcl',
        output='screen',
        parameters=[nav2_config]
    )

    lifecycle_manager_node = Node(
        package='nav2_lifecycle_manager',
        executable='lifecycle_manager',
        name='lifecycle_manager_navigation',
        output='screen',
        parameters=[{
            'use_sim_time': True,
            'autostart': True,
            'node_names': [
                'map_server',
                'amcl',
                'planner_server',
                'controller_server',
                'recoveries_server',
                'bt_navigator'
            ],

            'bond_timeout': 10.0,

            'attempt_respawn_reconnection': True,
            'bond_respawn_max_duration': 10.0
        }]
    )

    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        arguments=['-d', rviz_config],
        parameters=[{'use_sim_time': True}],
        condition=IfCondition(use_rviz)
    )

    
    

    return LaunchDescription([
        DeclareLaunchArgument(
            'use_rviz',
            default_value='false',
            description='Whether to launch RViz'
        ),
        map_server_node,
        amcl_node,
        ekf_node,
        planner_node,
        controller_node,
        recoveries_node,
        bt_navigator_node,
        rviz_route_manager_node,
        lifecycle_manager_node,
        rviz_node
    ])

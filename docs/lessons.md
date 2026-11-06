# From ROS messages to a virtual AMR

Use [the README setup](../README.md#start-here) first. Every terminal must source both the Humble environment and the built workspace, and use the same local simulation environment variables. Commands below run on the development PC.

## 1. Follow a message

Terminal A:

```bash
ros2 launch robotless_lab lesson.launch.py
```

Terminal B:

```bash
ros2 node list
ros2 topic list -t
ros2 topic info /robotless/lesson --verbose
ros2 topic echo /robotless/lesson
```

Find the publisher, subscriber, message type and changing sequence number. Read [lesson.py](../src/robotless_lab/robotless_lab/lesson.py): the timer publishes; the subscription callback receives. Change the sentence or timer period, rebuild, and observe the effect. Stop the launch with Ctrl+C.

## 2. Services and parameters without Gazebo

Run these in separate terminals:

```bash
ros2 run turtlesim turtlesim_node
```

```bash
ros2 run turtlesim turtle_teleop_key
```

Then inspect and change the virtual turtle's pen:

```bash
ros2 service list -t
ros2 interface show turtlesim/srv/SetPen
ros2 service call /turtle1/set_pen turtlesim/srv/SetPen \
  '{r: 40, g: 170, b: 220, width: 4, off: 0}'
ros2 param list /turtlesim
ros2 param get /turtlesim background_r
```

A service returns a response to a request. A topic is a stream. Navigation later introduces an action: a long-running request with feedback and a result. Stop turtlesim before the next lesson.

## 3. Read a virtual robot

```bash
ros2 launch robotless_lab simulation.launch.py
```

Wait for Burger to appear in the original warehouse. In another terminal:

```bash
ros2 topic hz /scan
ros2 topic echo /odom --once
ros2 run tf2_ros tf2_echo odom base_footprint
ros2 topic echo /clock --once
```

`/scan` is virtual LiDAR; `/odom` is the differential-drive estimate; TF connects coordinate frames; `/clock` is simulation time. Inspect the [original world geometry](../src/robotless_lab/worlds/learning_warehouse.world) and [its schematic](assets/warehouse.svg). A sketch is not a sensor measurement.

Keyboard control, in a separate terminal using the same environment:

```bash
ros2 run turtlebot3_teleop teleop_keyboard
```

Follow the keyboard's displayed controls. Keep speeds low for learning; use its stop key before exiting. These instructions are for the virtual robot. Do not bridge this ROS session to physical equipment.

## 4. Build and save a map

Leave simulation running. Start mapping:

```bash
ros2 launch robotless_lab mapping.launch.py
```

Open RViz in another terminal:

```bash
ros2 run rviz2 rviz2 --ros-args -p use_sim_time:=true
```

Set **Fixed Frame** to `map`. Add a **Map** display using `/map`, a **LaserScan** display using `/scan`, and **TF**. Drive the virtual robot slowly with teleop, visiting the aisles and looking at shelves from several sides. Check that scans align with obstacles; unexplored gray areas are not free space. If a display reports incompatible QoS, select the sensor's best-effort reliability for that display.

When a useful map exists:

```bash
mkdir -p ~/robotless_ws/maps
ros2 run nav2_map_server map_saver_cli \
  -f ~/robotless_ws/maps/learning_warehouse \
  --ros-args -p use_sim_time:=true
ls ~/robotless_ws/maps/learning_warehouse.*
```

Confirm that the YAML and referenced image exist. Stop teleop after stopping the robot. Stop the mapping launch with Ctrl+C before starting saved-map navigation. Leave Gazebo running. Map files are learner-generated output and are ignored by Git when stored in a `maps/` folder.

## 5. Navigate with Nav2

```bash
ros2 launch robotless_lab navigation.launch.py \
  map:=$HOME/robotless_ws/maps/learning_warehouse.yaml
```

The launch opens RViz, loads your map and uses the installed TurtleBot3 Humble Burger navigation parameters. It does not send a goal.

1. In RViz, use **2D Pose Estimate** to place the robot at its current location on the saved map, with the correct heading. Use the Gazebo scene and visible obstacles as references.
2. Verify that the laser scan aligns with the map, `/amcl_pose` is being published and the `map -> odom -> base_footprint` TF chain exists.
3. Use **Nav2 Goal** to select a free, mapped location. Observe the planned path, feedback and final action status.

The SDF world coordinates and the SLAM map coordinates need not have the same origin. Do not copy the world spawn coordinates into an initial pose without verifying their relationship.

Inspect the action interface:

```bash
ros2 action list -t
ros2 interface show nav2_msgs/action/NavigateToPose
```

As an alternative to RViz, the following is an example action request. Replace `(0.0, 1.0)` with a verified free location in **your map** and set the orientation you want. Run it only after the initial localization above:

```bash
ros2 action send_goal /navigate_to_pose nav2_msgs/action/NavigateToPose \
  '{pose: {header: {frame_id: map}, pose: {position: {x: 0.0, y: 1.0, z: 0.0}, orientation: {x: 0.0, y: 0.0, z: 0.0, w: 1.0}}}}' \
  --feedback
```

No automatic retry is included. If navigation fails, inspect the action result, localization, TF and costmaps before sending another goal. Use RViz's Nav2 controls to cancel an active goal; terminating a command-line action client alone does not guarantee cancellation. Shut down navigation and simulation after the exercise.

## 6. Understand position error

While localization is active, run the read-only reporter with the same goal you actually selected:

```bash
ros2 run robotless_lab pose_report --ros-args \
  -p use_sim_time:=true \
  -p goal_x:=0.0 -p goal_y:=1.0 -p goal_yaw_deg:=0.0
```

It reports the incoming `map` frame timestamp, configured goal, AMCL coordinates, signed `dx_mm` and `dy_mm`, Euclidean `xy_mm`, and wrapped yaw difference. Parameters are read at startup; restart the reporter to compare a different goal. Invalid quaternions, nonfinite positions and other frames are rejected.

For example, an estimate 3 mm right and 4 mm below a goal has `dx_mm=3`, `dy_mm=-4`, and `xy_mm=5`. That is a calculation, not a measured project result.

The reporter only emits output when a pose arrives. Check the timestamp and topic freshness yourself; an old line is not a fresh observation. It does not decide whether the robot has stopped, whether Nav2 succeeded, or whether localization is correct. AMCL and odometry are estimates; neither is independent metrology. **Physical +/-1 mm accuracy is not proven yet.**

## Troubleshooting

| Symptom | Check |
| --- | --- |
| `Package 'robotless_lab' not found` | Build from `~/robotless_ws`, then source `install/setup.bash` in that terminal. |
| No messages between terminals | Match `ROS_DOMAIN_ID`, `ROS_LOCALHOST_ONLY`, ROS distribution and sourced workspace. |
| Gazebo GUI is unavailable | Use `gui:=false` for sensor-based development, or run on a desktop with working graphics. |
| No `/scan` or `/odom` | Inspect the simulation launch output for spawn and Gazebo plugin errors; confirm Burger actually spawned. |
| SLAM has no map | Confirm advancing `/clock`, `/scan` and `odom -> base_footprint`; move only the virtual robot to gather views. |
| Nav2 waits for localization | Set and verify the initial pose on the saved map. Do not guess a pose to silence the wait. |
| Wrong map or unknown space | Stop and load the correct saved map; inspect its YAML image path and resolution. |
| Missing package on apt | Confirm Ubuntu 22.04 and the official Humble apt source; use the upstream Humble instructions rather than mixing distributions. |

For the underlying architecture and source repositories, see [references](references.md). For executed versus unexecuted checks, see [validation](validation.md).

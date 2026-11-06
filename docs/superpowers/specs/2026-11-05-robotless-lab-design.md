# ROS without robots: project design

## Intent and scope

Build a public, beginner-friendly ROS 2 learning and AMR simulation repository for Ubuntu 22.04 and ROS 2 Humble. The user selected this scope over a new navigation research algorithm. The deliverable includes executable original examples, an original warehouse world, English and Tamil instructions, an original architecture illustration, citations, licensing information, and runnable checks.

## Approaches

1. Use official TurtleBot3, Gazebo, SLAM Toolbox and Nav2 as installed dependencies, with original lessons and a primitive-geometry warehouse world. Selected implementation choice: this uses the user's reference ecosystem and keeps upstream robot assets with their original distributors.
2. Fork and redistribute complete upstream repositories. This increases maintenance and asset-specific licensing work without adding learning value.
3. Build a new simulator or navigation algorithm. This exceeds the selected learning-project scope and would conceal the ROS ecosystem the learner wants to study.

## Architecture

A single ament_python package, `robotless_lab`, provides a topic publisher/subscriber lesson and a read-only localization error reporter. Four launch files cover the lesson, Gazebo simulation, SLAM mapping and saved-map navigation. The simulation uses the installed TurtleBot3 Burger model, an original SDF warehouse, and an optional GUI. Mapping and navigation run separately against that simulation. Navigation requires a user-created map and an operator-selected initial pose; launch does not send a goal. Goals are taught through RViz and the official ROS action CLI rather than a second navigation implementation.

The reporter compares an AMCL pose and a configured goal in the `map` frame, reports signed dx/dy in millimeters, Euclidean XY error in millimeters, and wrapped yaw error in degrees. It rejects nonfinite inputs and wrong frames. It is a comparison of localization and goal, not independent accuracy metrology. There is no physical +/-1 mm claim.

## Interfaces and defaults

- Lesson topic: `/robotless/lesson`, message `std_msgs/msg/String`, one message per second.
- Pose input: `/amcl_pose`, message `geometry_msgs/msg/PoseWithCovarianceStamped`; expected frame `map`.
- Reporter parameters: `goal_x`, `goal_y` in meters; `goal_yaw_deg` in degrees. Goals are set at startup.
- Simulation: Burger; spawn `(0, -3)` meters; no motion on startup; `gui:=false` supports CI.
- Mapping: SLAM Toolbox online async, `/scan`, `base_footprint`, `odom`, `map`, 0.05 m map resolution.
- Navigation: Nav2 bringup with the installed Humble Burger parameters; required `map:=/absolute/path/map.yaml`; optional RViz GUI; simulation time enabled.
- Shell session instructions set `ROS_DOMAIN_ID=42`, `ROS_LOCALHOST_ONLY=1`, and `TURTLEBOT3_MODEL=burger` in every terminal. This is a local simulation convention, not a safety isolation guarantee.

## Authorship and licensing

Original project code, prose, SVG and SDF are Apache-2.0. No paper PDF, abstract, third-party screenshot, logo, mesh, texture, upstream implementation or parameter file is vendored. Cite both papers and link upstream sources. Upstream packages keep their own licenses; Nav2 has package-specific mixed licensing. Explain that free download and a public GitHub page do not themselves authorize redistributing every image or paper. Do not promise freedom from every possible copyright claim.

## Validation and limits

Use dependency-free Python unit tests for error geometry and quaternion conversion, XML parsing and packaging checks locally. Run the real package in GitHub Actions using a Humble/Jammy container, a colcon build, an actual ROS publisher/subscriber smoke check, launch argument loading, and a headless Gazebo check for advancing `/clock`, `/scan` and finite `/odom`. Do not substitute mocks for those runtime checks. Navigation through a user-mapped scene and GUI interaction remain unverified unless actually exercised. Public visibility is verified through repository metadata and an unauthenticated fetch.

## Builder-owned choices

File organization, readable lesson wording, warehouse primitive colors, test implementation and CI plumbing are implementation decisions. No GUI app, custom controller, production deployment, hardware actuation, custom planner or performance claim is required. The explicit user instruction already authorizes upload and public publication of this new project after its content and licenses are reviewed.

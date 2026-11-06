# Validation and boundaries

The [CI workflow](../.github/workflows/ci.yml) is the executable record. Check the run at the commit you use; a workflow definition or badge image alone is not proof that a check passed.

## Checks provided

| Check | What it exercises | What it does not establish |
| --- | --- | --- |
| Python unit tests | Signed metric conversion, Euclidean distance, yaw wrap, quaternion normalization, nonfinite/invalid values | ROS middleware or physical accuracy |
| Source/project checks | Python parsing, package/world/SVG XML parsing, required files and local documentation links | Simulator semantics or online link availability |
| Humble colcon build | Actual ROS package installation and resource packaging | A completed simulation mission |
| Real ROS smoke | Original publisher/subscriber delivery and sequence; reporter frame rejection and known numeric output through ROS messages | Gazebo, SLAM or path following |
| Launch argument/resource checks | Installed upstream launch resources and required navigation-map argument loading | A loaded user-generated map or correctly initialized AMCL |
| Headless Gazebo smoke | Original warehouse starts with virtual Burger; clock advances, scan has finite returns and odometry has expected frames and finite values | GUI appearance, full TF consistency, map quality, navigation success or endurance |

## Local verification commands

From the repository root:

```bash
PYTHONPATH=src/robotless_lab python3 -m unittest discover -s tests -p 'test_*.py' -v
python3 -m compileall -q src tests tools
python3 tools/check_project.py
```

After a Humble build and sourcing the workspace:

```bash
python3 tests/ros_smoke.py
ros2 launch robotless_lab simulation.launch.py gui:=false
# In another identically configured terminal:
python3 tests/simulation_smoke.py
```

The smoke scripts are bounded and fail with a nonzero exit code on missing evidence. The Gazebo check only subscribes; it does not publish velocity commands.

## Interactive acceptance still needed

Follow [lessons 4 and 5](lessons.md#4-build-and-save-a-map) to create a map, set and verify the initial pose, choose a free goal and inspect its final action result. Record the distribution, installed dependency versions, map, goal, timestamps, localization and final action status. The automated checks do not perform that complete exercise or verify a native desktop GUI.

No physical robot was used to develop these examples. Real hardware suitability, safety functions, production readiness, endurance and physical +/-1 mm accuracy are **not proven yet**. A goal-versus-AMCL error is an estimator comparison. Absolute accuracy would require independent calibrated measurement, consistent frames and repeated trials with stated uncertainty.

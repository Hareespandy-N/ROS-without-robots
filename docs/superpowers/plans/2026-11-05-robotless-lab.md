# Robotless Lab Implementation Plan

> **For agentic workers:** Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox syntax for tracking.

**Goal:** Publish an original ROS 2 Humble learning and warehouse simulation project with real runtime checks and explicit source attribution.

**Architecture:** One Python ROS package composes installed TurtleBot3, Gazebo, SLAM Toolbox and Nav2. Original examples and an original world sit above those dependencies.

**Tech Stack:** Ubuntu 22.04, ROS 2 Humble, Python 3.10+, ament_python, Gazebo Classic, GitHub Actions.

**Spec:** `docs/superpowers/specs/2026-11-05-robotless-lab-design.md`

## Global constraints

- Original project code, prose, SVG and SDF are Apache-2.0; no upstream papers, images or code are vendored.
- Burger simulation only; spawn `(0, -3)`; no goal is sent at startup.
- Navigation needs a saved map and explicit initial localization; simulation clock is enabled.
- No physical robot access and no absolute accuracy claim.

## Review focus

- Nonfinite pose values must not produce apparently valid errors.
- Yaw across +/-180 degrees must report the short rotation.
- Quaternion input with zero norm must be rejected, and scaled valid input normalized.
- Launch files must resolve installed resources and the required saved-map argument.
- A successful build must not be mistaken for a running Gazebo or a completed navigation mission.

## Task 1: Original lessons and error reporter

Files: `src/robotless_lab/{package.xml,setup.py,setup.cfg,resource/robotless_lab,robotless_lab/*.py}`, `tests/test_geometry.py`, `tests/ros_smoke.py`.

Interfaces: `pose_error(goal, actual)` returns dx_mm, dy_mm, xy_mm and yaw_deg; `quaternion_yaw(x,y,z,w)` returns radians. `LessonPublisher` and `LessonSubscriber` exchange real ROS String messages. Reporter consumes AMCL only.

- [ ] Write geometry tests using literal expected errors, wrap boundaries, finite checks and invalid quaternion inputs; run and observe missing-feature failure.
- [ ] Implement geometry, lesson nodes and reporter; run `python -m unittest discover -s tests -p 'test_*.py' -v` and compilation checks.
- [ ] Add a real ROS smoke script for lesson communication and reporter output; exercise it in Humble CI.

## Task 2: Warehouse simulation and ROS composition

Files: `src/robotless_lab/{launch/*.launch.py,worlds/learning_warehouse.world,config/slam.yaml}`.

Interfaces: simulation exposes `/clock`, `/scan`, `/odom` and TF; mapping consumes those; navigation consumes a required map file and installed Burger parameters.

- [ ] Write headless runtime smoke assertions for moving clock, nonempty scan and finite odometry.
- [ ] Implement an original primitive warehouse and launch composition with `gui:=false` support.
- [ ] In CI, colcon-build, load launch arguments and run the headless runtime smoke script against Gazebo.

## Task 3: Usable documentation and publication

Files: `README.md`, `docs/{README.ta.md,lessons.md,references.md,validation.md,assets/architecture.svg}`, `LICENSE`, `NOTICE`, `THIRD_PARTY_NOTICES.md`, `.github/workflows/ci.yml`, `.gitignore`.

- [ ] Document install/build, every-terminal environment, lessons, mapping and map saving, Nav2 initial pose and goals, troubleshooting, and measured-error limits.
- [ ] Add citations and license provenance; review original assets, relative links, package data and staged diff.
- [ ] Obtain a fresh whole-project review, fix consequential findings, and re-run affected checks.
- [ ] Push the reviewed project, observe CI, switch the authorized repository to public, and verify public access and content at the published commit.

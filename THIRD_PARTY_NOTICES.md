# Third-party references and provenance

Checked on 2026-11-05. This repository distributes its original Python lessons, launch composition, minimal mapping configuration, SDF primitive warehouse, SVG drawings and explanatory prose. It does not vendor upstream implementation files, navigation parameters, robot models, meshes, textures, paper PDFs, abstracts or third-party screenshots.

The project's [Apache-2.0 license](LICENSE) covers its original contributions. It does not replace the licenses of installed dependencies or relicense the referenced papers.

## Separately installed dependencies

| Source | License evidence | Use / provenance |
| --- | --- | --- |
| ROBOTIS TurtleBot3 simulations, `humble` | [Apache-2.0 LICENSE](https://github.com/ROBOTIS-GIT/turtlebot3_simulations/blob/humble/LICENSE) | Burger simulation assets and spawn/state-publisher launch interfaces are resolved from the installed package. No assets or upstream source copied into this repo. |
| ROBOTIS TurtleBot3 navigation, `humble` | [Package manifest: Apache 2.0](https://github.com/ROBOTIS-GIT/turtlebot3/blob/humble/turtlebot3_navigation2/package.xml) | Parameters and RViz configuration remain in the installed upstream package. |
| Navigation2, `humble` | [Root licensing overview](https://github.com/ros-navigation/navigation2/blob/humble/LICENSE) | Mixed licensing includes LGPL-2.1-or-later, Apache-2.0, BSD-3-Clause and combined entries. Consult each package and file; do not treat the whole source tree as one license. |
| SLAM Toolbox, `humble` | [Manifest declaring LGPL](https://github.com/SteveMacenski/slam_toolbox/blob/humble/package.xml) | Installed mapping implementation; consult upstream files for detailed terms. No implementation copied here. |
| ROS tutorials / turtlesim, `humble` | [Manifest declaring BSD](https://github.com/ros/ros_tutorials/blob/humble/turtlesim/package.xml) | Installed tutorial program invoked in the lessons. |
| ROS 2 and Gazebo ROS packages | [ROS 2 source organizations](https://github.com/ros2), [Gazebo ROS packages](https://github.com/ros-simulation/gazebo_ros_pkgs) | System dependencies with package/file-specific notices supplied by their distributors. |

The above is a source/provenance inventory, not an exhaustive license inventory for every transitive apt dependency. If redistributing a binary image or upstream source in the future, audit and preserve that distribution's full dependency licenses and notices separately.

## Papers and artwork

The two papers are cited in [references](docs/references.md); their text, figures and PDFs are not included. Free reading access does not automatically authorize republication. [arXiv's official reuse guidance](https://info.arxiv.org/help/license/reuse.html) describes checking the assigned license and contacting the relevant rightsholder when needed.

`docs/assets/architecture.svg` and `docs/assets/warehouse.svg` are original vector drawings created for this project, with no upstream logos or traced paper figures. `learning_warehouse.world` is original primitive geometry without external artwork. The installed TurtleBot3 robot remains an upstream asset, even when rendered by the simulator.

The standard Apache-2.0 license text in `LICENSE` is published by the [Apache Software Foundation](https://www.apache.org/licenses/LICENSE-2.0.txt). Names such as ROS, Gazebo and TurtleBot3 identify the dependencies and do not imply ownership of their trademarks or endorsement.

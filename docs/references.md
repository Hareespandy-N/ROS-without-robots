# Papers and upstream sources

Sources checked on 2026-11-05. The notes below are original learning summaries. They do not reproduce paper text or figures and do not claim a new research result.

## ROS 2 architecture

Steve Macenski, Tully Foote, Brian Gerkey, Chris Lalancette and William Woodall. **Robot Operating System 2: Design, Architecture, and Uses In The Wild.** *Science Robotics*, 2022. DOI: [10.1126/scirobotics.abm6074](https://doi.org/10.1126/scirobotics.abm6074). [arXiv record](https://arxiv.org/abs/2211.07752) · [Author-uploaded PDF](https://arxiv.org/pdf/2211.07752).

Study how a robot can be split into independently running processes with explicit communication interfaces. In this lab, start with two small nodes and inspect discovery, message types and QoS before introducing a simulator. The lesson demonstrates one communication pattern; it does not reproduce the paper's experiments or establish industrial reliability.

Reading exercise: draw which process owns sensing, state estimation, planning and visualization in your running ROS graph. Explain what happens if one process stops publishing.

## Nav2 architecture

Steve Macenski, Francisco Martín, Ruffin White and Jonatan Ginés Clavero. **The Marathon 2: A Navigation System.** IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS), 2020. DOI: [10.1109/IROS45743.2020.9341207](https://doi.org/10.1109/IROS45743.2020.9341207). [arXiv record](https://arxiv.org/abs/2003.00368) · [Author-uploaded PDF](https://arxiv.org/pdf/2003.00368).

Study how navigation coordinates several responsibilities rather than relying on a single movement command. Nav2 separates planning, following a path and higher-level task orchestration. In this lab, inspect an action's feedback, the path and the costmaps while the installed Nav2 stack handles a virtual goal. The repository adds no new planner and does not reproduce the paper's marathon evaluation.

Reading exercise: distinguish a goal rejected before execution from a path-following task that begins and later fails. Identify the evidence you would record for each.

## Official implementation sources

| Component | Official source | How this project uses it |
| --- | --- | --- |
| ROS 2 Humble | [Installation](https://docs.ros.org/en/humble/Installation/Ubuntu-Install-Debs.html), [Tutorials](https://docs.ros.org/en/humble/Tutorials.html) | Runtime and learning APIs |
| TurtleBot3 simulations | [Humble branch](https://github.com/ROBOTIS-GIT/turtlebot3_simulations/tree/humble), [simulation manual](https://emanual.robotis.com/docs/en/platform/turtlebot3/simulation/) | Installed Burger model, spawn and robot state launch interfaces |
| TurtleBot3 navigation | [Humble package](https://github.com/ROBOTIS-GIT/turtlebot3/tree/humble/turtlebot3_navigation2) | Installed Burger Nav2 parameters and RViz configuration |
| Nav2 | [Humble branch](https://github.com/ros-navigation/navigation2/tree/humble), [official documentation](https://docs.nav2.org/) | Installed saved-map navigation stack |
| SLAM Toolbox | [Humble branch](https://github.com/SteveMacenski/slam_toolbox/tree/humble) | Installed online mapping node |
| turtlesim | [Official Humble tutorials source](https://github.com/ros/ros_tutorials/tree/humble) | Service and parameter exercises |

The older `ros-planning/navigation2` reference redirects to the current `ros-navigation/navigation2` organization. This project targets the Humble branch and distribution, not upstream development branches.

## Reuse boundaries

Public access is not the same as permission to republish every component. [arXiv's reuse guidance](https://info.arxiv.org/help/license/reuse.html) explains that the article's assigned license controls figure and text reuse. This repository links the papers, uses original explanations and drawings, and does not redistribute their PDFs, figures or abstracts. See [third-party notices](../THIRD_PARTY_NOTICES.md) for the checked software licenses.

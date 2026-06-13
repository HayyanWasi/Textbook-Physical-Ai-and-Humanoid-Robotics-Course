# Research: Module 2 — The Digital Twin (Gazebo & Unity)

**Branch**: `002-digital-twin` | **Date**: 2026-06-13
**Phase**: 0 — Research & Unknowns Resolution

## Research Question 1: Gazebo Versions and ROS 2 Integration (Classic vs. Ignition/Gz)

**Decision**: Refer to "Gazebo" generically as the physics simulation environment, without locking to
Classic (Gazebo 11) or Ignition/Gz (Gazebo Fortress/Garden/Harmonic). Content must remain valid
across versions.

**Rationale**: The Gazebo ecosystem has two major branches — Gazebo Classic (deprecated after
Gazebo 11, last supported on ROS 2 Humble) and Ignition/Gz (the modern successor, branded Gazebo
Fortress onward). As of 2024, Gazebo Harmonic is the default for ROS 2 Iron/Jazzy. The pedagogical
content (world files, URDF/SDF concepts, physics parameters) is largely version-agnostic. Using the
generic term "Gazebo" with a parenthetical note in Chapter 5 that the current release is named "Gz
Harmonic" is sufficient for a conceptual textbook.

**ROS 2 Bridge topics** (standard across versions):
- Gazebo publishes sensor data directly onto ROS 2 topics via `ros_gz_bridge` (Ignition) or
  `gazebo_ros_pkgs` (Classic). The bridge maps simulation topics to standard ROS 2 message types.
- IMU: publishes on `/imu/data` using `sensor_msgs/Imu`
- LiDAR: publishes on `/scan` or `/lidar/scan` using `sensor_msgs/LaserScan` or
  `sensor_msgs/PointCloud2`
- Depth camera: publishes on `/camera/depth/image_rect_raw` using `sensor_msgs/Image` and
  `/camera/depth/camera_info` using `sensor_msgs/CameraInfo`
- Odometry / ground truth: publishes on `/odom` using `nav_msgs/Odometry`
- Joint states: publishes on `/joint_states` using `sensor_msgs/JointState`

**Alternatives considered**:
- Lock to Gazebo Classic: version is deprecated; would be misleading for new students.
- Lock to Gz Harmonic: too specific; students using ROS 2 Humble/Iron may use different Gz versions.
- Use Gazebo generically: chosen. The bridge concept and topic structure are stable across versions.

---

## Research Question 2: Unity ROS 2 Integration Pipeline

**Decision**: Describe the Unity Robotics Hub (Unity-Technologies/ROS-TCP-Connector) as the
integration layer, framed conceptually as a "ROS–Unity bridge" without requiring students to
install anything.

**Rationale**: The Unity Robotics Hub is the official Unity package for ROS/ROS 2 communication.
It operates via a ROS TCP Endpoint — a ROS 2 node that accepts WebSocket/TCP connections from
Unity, forwarding ROS 2 messages in both directions. This architecture means:

- Gazebo owns physics simulation (deterministic, runs alongside ROS 2)
- Unity owns rendering (receives robot state from the ROS 2 graph, renders it visually)
- ROS 2 is the shared communication bus between them

The data flow is: Gazebo → ROS 2 topics → Unity (via bridge) → rendered scene. The robot's
URDF description (from Module 1, Chapter 4) is imported into Unity as the visual mesh, while
Gazebo maintains the physics ground truth.

**Use cases that require Unity** (not possible in Gazebo alone):
- Photorealistic rendering of outdoor environments for computer vision training datasets
- Human avatar simulation for human-robot interaction (HRI) research
- Accessibility evaluation (simulating humans with varying mobility in a robot's environment)
- Training reinforcement learning agents with realistic visual observations

**Alternatives considered**:
- O3DE: the AWS-backed open-source alternative with better physics; less adoption than Unity.
- Unreal Engine: photorealistic; used in AirSim; larger learning curve than Unity for roboticists.
- Unity chosen: most widely adopted in robotics education and the Unity Robotics Hub is maintained
  by Unity Technologies directly.

---

## Research Question 3: Gazebo World File Format (SDF vs URDF)

**Decision**: Distinguish SDF (Simulation Description Format) from URDF in Chapter 6. SDF is the
native format for Gazebo world files; URDF describes robot structure (taught in Module 1, Ch. 4).
Gazebo accepts URDF for the robot model but uses SDF for the world (environment).

**Rationale**: Students who completed Module 1 know URDF. Chapter 6 introduces SDF to describe
the physics environment (gravity, ground plane, objects). The key teaching point is:
- **URDF** → describes the robot (joint limits, visual/collision geometry, inertia — Module 1)
- **SDF** → describes the world (gravity, friction, ambient light, physics engine parameters)

The `<gravity>` element in SDF accepts an XYZ vector in m/s² (e.g., `<gravity>0 0 -9.8</gravity>`
for Earth). No derivation needed — the student just needs to understand what changing this value
means physically.

**Alternatives considered**:
- Teach only URDF: insufficient — URDF cannot describe a simulation world, only a robot body.
- Teach URDF extensions (xacro): out of scope; advanced tooling beyond a conceptual chapter.

---

## Research Question 4: Standard Simulated Sensor ROS 2 Topic and Message Type Table

**Decision**: Document the following sensor-to-topic mapping as the canonical reference for
Chapter 8. All topic names and message types are standard ROS 2 conventions; Gazebo plugins
publish to these topics automatically when correctly configured.

| Sensor Type | Topic Name | ROS 2 Message Type | Established In |
|---|---|---|---|
| 2D LiDAR | `/scan` or `/lidar/scan` | `sensor_msgs/LaserScan` | Module 2, Ch. 8 |
| 3D LiDAR / Point Cloud | `/points` or `/lidar/points` | `sensor_msgs/PointCloud2` | Module 2, Ch. 8 |
| Depth Camera (color) | `/camera/image_raw` | `sensor_msgs/Image` | Module 1, Ch. 2 reference |
| Depth Camera (depth) | `/camera/depth/image_raw` | `sensor_msgs/Image` | Module 2, Ch. 8 |
| IMU | `/imu/data` | `sensor_msgs/Imu` | Module 2, Ch. 8 |
| Odometry | `/odom` | `nav_msgs/Odometry` | Module 2, Ch. 8 |
| Joint States | `/joint_states` | `sensor_msgs/JointState` | Module 2, Ch. 8 |

Cross-reference to Module 1: `/camera/image_raw` and `/lidar/scan` were introduced in Chapter 2
as example topic names. Chapter 8 deepens this by showing simulated plugins produce identical
message types.

**Rationale**: Using standard ROS 2 topic naming conventions ensures content accuracy and prepares
students to read real ROS 2 robot documentation without confusion.

---

## Research Question 5: MDX Component Import Pattern for Module 2

**Decision**: Continue the per-file import pattern established in Module 1 implementation
(`import RagChatbot from '@site/src/components/RagChatbot';`) rather than switching to global
registration mid-project.

**Rationale**: The Module 1 chapters use per-file imports and build successfully. The research
decision to use global registration (documented in Module 1 research.md) was not implemented —
the actual files use per-file imports. Consistency requires Module 2 to follow the same pattern.
Switching to global registration mid-project requires swizzling `@theme/MDXComponents`, which is
a more complex change and outside the scope of a content feature.

**Resolution**: Each Module 2 chapter includes:
```mdx
import RagChatbot from '@site/src/components/RagChatbot';
```
at the top, and uses `<RagChatbot context="module-2" />` at the bottom.

---

## Research Question 6: Docusaurus Sidebar — Appending Module 2

**Decision**: Append a Module 2 category object to the existing `tutorialSidebar` array in
`frontend/sidebars.ts`, after the existing Module 1 category.

**Rationale**: Confirmed by inspecting `frontend/sidebars.ts`. The file currently exports a
`SidebarsConfig` with a single `tutorialSidebar` key containing the Module 1 category. Module 2
is appended as a second item in that array. The doc ID format is `module-2/chapter-N-slug`.

**Module 2 sidebar addition**:
```typescript
{
  type: 'category',
  label: 'Module 2: The Digital Twin',
  collapsed: false,
  items: [
    'module-2/chapter-5-digital-twin-gazebo',
    'module-2/chapter-6-physics-collisions',
    'module-2/chapter-7-unity-rendering',
    'module-2/chapter-8-sensor-simulation',
  ],
},
```

---

## Summary of All Resolutions

| Unknown | Resolution | Artifact |
|---|---|---|
| Gazebo version specificity | Use "Gazebo" generically; note Gz Harmonic parenthetically | `plan.md`, Ch. 5 |
| Unity integration architecture | ROS TCP bridge; Gazebo = physics, Unity = render | Ch. 7 |
| SDF vs URDF distinction | SDF for world, URDF for robot; teach both briefly | `contracts/`, Ch. 6 |
| Sensor topic mapping | Standard ROS 2 convention table (7 sensors) | `data-model.md`, Ch. 8 |
| MDX import pattern | Per-file import (consistent with Module 1 actuals) | `quickstart.md` |
| Sidebar append pattern | Append to `tutorialSidebar` array in `sidebars.ts` | `quickstart.md` |

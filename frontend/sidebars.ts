import type {SidebarsConfig} from '@docusaurus/plugin-content-docs';

const sidebars: SidebarsConfig = {
  tutorialSidebar: [
    {
      type: 'category',
      label: 'Module 1: The Robotic Nervous System',
      collapsed: false,
      items: [
        'module-1/chapter-1-middleware',
        'module-1/chapter-2-nodes-topics',
        'module-1/chapter-3-rclpy',
        'module-1/chapter-4-urdf',
      ],
    },
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
    {
      type: 'category',
      label: 'Module 3: The AI-Robot Brain',
      collapsed: false,
      items: [
        'module-3/chapter-9-advanced-perception',
        'module-3/chapter-10-isaac-sim-synthetic-data',
        'module-3/chapter-11-isaac-ros-vslam',
        'module-3/chapter-12-nav2-bipedal-planning',
      ],
    },
    {
      type: 'category',
      label: 'Module 4: Vision-Language-Action',
      collapsed: false,
      items: [
        'module-4/chapter-13-vla-convergence',
        'module-4/chapter-14-voice-whisper',
        'module-4/chapter-15-cognitive-llm-planning',
        'module-4/chapter-16-capstone-autonomous-humanoid',
      ],
    },
  ],
};

export default sidebars;

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
  ],
};

export default sidebars;

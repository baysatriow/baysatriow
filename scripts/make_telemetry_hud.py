#!/usr/bin/env python3
"""
Generate an Autonomous Vehicle Telemetry HUD status strip SVG:
- Matches width 860px exactly
- Glowing active status indicator
- Live system status, sensor health, and ROS 2 Jazzy pipeline metrics
- Strictly ZERO Mdash
"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "av-telemetry.svg")

W, H = 860, 48
FRAME = "#30363d"
BG = "#0d1117"
BG2 = "#111722"
MUTED = "#7d8590"
GREEN = "#39d353"
CYAN = "#22d3ee"
AMBER = "#f59e0b"
TEXT = "#e6edf3"

svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace">
  <defs>
    <linearGradient id="tbg" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="{BG2}"/>
      <stop offset="50%" stop-color="{BG}"/>
      <stop offset="100%" stop-color="{BG2}"/>
    </linearGradient>
  </defs>
  <rect width="{W}" height="{H}" rx="8" fill="url(#tbg)"/>
  <rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="8" fill="none" stroke="{FRAME}" stroke-width="1"/>

  <!-- Pulsing green status beacon -->
  <circle cx="28" cy="24" r="5" fill="{GREEN}">
    <animate attributeName="opacity" values="1;0.3;1" dur="2s" repeatCount="indefinite"/>
  </circle>
  <circle cx="28" cy="24" r="9" fill="none" stroke="{GREEN}" stroke-width="1.2" opacity="0.6">
    <animate attributeName="r" values="6;13" dur="2s" repeatCount="indefinite"/>
    <animate attributeName="opacity" values="0.8;0" dur="2s" repeatCount="indefinite"/>
  </circle>

  <!-- Telemetry text segments (strictly NO Mdash) -->
  <text x="48" y="28" font-size="11.5" font-weight="700">
    <tspan fill="{MUTED}">[SYS]</tspan> <tspan fill="{GREEN}">AV-CORE: ONLINE</tspan>
    <tspan fill="{MUTED}">  ::  </tspan>
    <tspan fill="{MUTED}">[SENSORS]</tspan> <tspan fill="{CYAN}">LiDAR 360&#176;</tspan><tspan fill="{MUTED}"> | </tspan><tspan fill="{CYAN}">STEREO 60FPS</tspan><tspan fill="{MUTED}"> | </tspan><tspan fill="{CYAN}">RADAR 77GHz</tspan>
    <tspan fill="{MUTED}">  ::  </tspan>
    <tspan fill="{MUTED}">[PERCEPTION]</tspan> <tspan fill="{AMBER}">POINTCLOUD + EKF FUSION</tspan>
    <tspan fill="{MUTED}">  ::  </tspan>
    <tspan fill="{MUTED}">[FRAME]</tspan> <tspan fill="{TEXT}">ROS 2</tspan>
  </text>
</svg>"""

with open(OUT, "w", encoding="utf-8") as f:
    f.write(svg)
print(f"wrote {OUT} ({len(svg)} bytes)")

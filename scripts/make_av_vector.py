#!/usr/bin/env python3
"""
Generate an ultra-crisp, animated Vector LiDAR & AV Perception Simulator terminal SVG:
- Replaces blurry/noisy ASCII with high-tech vector graphics
- Rotating 360-degree LiDAR radar sweep
- Ego-vehicle with forward stereo camera FOV cone
- Detected 3D obstacle bounding boxes & point cloud clusters
- Animated dynamic trajectory planning path
- Corner telemetry stats + bottom rviz2 command line
- Symmetrical with info-card.svg: W=480, H=395
- Strictly ZERO Mdash
"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "av-perception.svg")

W, H = 480, 395
PAD = 20
TITLEBAR_H = 30
STATUS_H = 32

BG = "#0d1117"
BG2 = "#111722"
FRAME = "#30363d"
MUTED = "#7d8590"
TEXT = "#c9d1d9"
CYAN = "#22d3ee"
BLUE = "#38bdf8"
GREEN = "#3fb950"
AMBER = "#f59e0b"
RED = "#f43f5e"

# Center of radar display
CX = W / 2       # 240
CY = (TITLEBAR_H + (H - STATUS_H)) / 2 + 18  # ~215

svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace">
  <defs>
    <!-- Background Gradient -->
    <linearGradient id="vbg" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="{BG2}"/>
      <stop offset="100%" stop-color="{BG}"/>
    </linearGradient>

    <!-- Camera FOV Cone Gradient -->
    <linearGradient id="fovGrad" x1="0" y1="1" x2="0" y2="0">
      <stop offset="0%" stop-color="{CYAN}" stop-opacity="0.35"/>
      <stop offset="100%" stop-color="{CYAN}" stop-opacity="0.02"/>
    </linearGradient>

    <!-- Rotating LiDAR Sweep Gradient -->
    <linearGradient id="sweepGrad" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="{CYAN}" stop-opacity="0"/>
      <stop offset="100%" stop-color="{CYAN}" stop-opacity="0.38"/>
    </linearGradient>

    <!-- Radar Clip to stay inside display -->
    <clipPath id="radarClip">
      <rect x="12" y="{TITLEBAR_H + 4}" width="{W - 24}" height="{H - TITLEBAR_H - STATUS_H - 8}" rx="8"/>
    </clipPath>
  </defs>

  <!-- Terminal Window Base -->
  <rect width="{W}" height="{H}" rx="12" fill="url(#vbg)"/>
  <rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="12" fill="none" stroke="{FRAME}" stroke-width="1"/>
  <line x1="0" y1="{TITLEBAR_H}" x2="{W}" y2="{TITLEBAR_H}" stroke="{FRAME}"/>

  <!-- Titlebar Window Controls -->
  <circle cx="{PAD}" cy="{TITLEBAR_H/2}" r="5" fill="#ff5f56"/>
  <circle cx="{PAD + 16}" cy="{TITLEBAR_H/2}" r="5" fill="#ffbd2e"/>
  <circle cx="{PAD + 32}" cy="{TITLEBAR_H/2}" r="5" fill="#27c93f"/>
  <text x="{W/2}" y="{TITLEBAR_H/2 + 4}" fill="{MUTED}" font-size="12" text-anchor="middle">baysatriow@github: ~/rviz2_perception.sh</text>

  <!-- Radar & Perception Display (Clipped) -->
  <g clip-path="url(#radarClip)">
    <!-- Range Rings (50m, 100m, 150m) -->
    <circle cx="{CX}" cy="{CY}" r="45" fill="none" stroke="{FRAME}" stroke-width="1" stroke-dasharray="3,3"/>
    <circle cx="{CX}" cy="{CY}" r="90" fill="none" stroke="{FRAME}" stroke-width="1" stroke-dasharray="3,3"/>
    <circle cx="{CX}" cy="{CY}" r="135" fill="none" stroke="{FRAME}" stroke-width="1" stroke-dasharray="4,4" opacity="0.6"/>

    <!-- Crosshair Axes -->
    <line x1="{CX - 150}" y1="{CY}" x2="{CX + 150}" y2="{CY}" stroke="{FRAME}" stroke-width="0.8" stroke-dasharray="2,4"/>
    <line x1="{CX}" y1="{CY - 145}" x2="{CX}" y2="{CY + 110}" stroke="{FRAME}" stroke-width="0.8" stroke-dasharray="2,4"/>

    <!-- Range Ring Labels -->
    <text x="{CX + 48}" y="{CY - 4}" fill="{MUTED}" font-size="8.5">25m</text>
    <text x="{CX + 93}" y="{CY - 4}" fill="{MUTED}" font-size="8.5">50m</text>
    <text x="{CX + 138}" y="{CY - 4}" fill="{MUTED}" font-size="8.5">75m</text>

    <!-- Forward Camera FOV Vision Cone (110 deg) -->
    <polygon points="{CX},{CY} {CX - 95},{CY - 145} {CX + 95},{CY - 145}" fill="url(#fovGrad)"/>
    <line x1="{CX}" y1="{CY}" x2="{CX - 95}" y2="{CY - 145}" stroke="{CYAN}" stroke-width="1" stroke-dasharray="3,3" opacity="0.5"/>
    <line x1="{CX}" y1="{CY}" x2="{CX + 95}" y2="{CY - 145}" stroke="{CYAN}" stroke-width="1" stroke-dasharray="3,3" opacity="0.5"/>

    <!-- 360-degree Rotating LiDAR Beam -->
    <g transform="translate({CX},{CY})">
      <path d="M 0 0 L 150 -40 A 155 155 0 0 0 150 40 Z" fill="url(#sweepGrad)">
        <animateTransform attributeName="transform" type="rotate" from="0" to="360" dur="3.6s" repeatCount="indefinite"/>
      </path>
    </g>

    <!-- Point Cloud Clusters (LiDAR road & curbs) -->
    <g fill="{CYAN}" opacity="0.75">
      <!-- Left lane boundary points -->
      <circle cx="{CX - 50}" cy="{CY - 20}" r="1.5"/>
      <circle cx="{CX - 54}" cy="{CY - 45}" r="1.5"/>
      <circle cx="{CX - 57}" cy="{CY - 70}" r="1.5"/>
      <circle cx="{CX - 59}" cy="{CY - 95}" r="1.5"/>
      <circle cx="{CX - 62}" cy="{CY - 120}" r="1.5"/>
      <!-- Right lane boundary points -->
      <circle cx="{CX + 50}" cy="{CY - 20}" r="1.5"/>
      <circle cx="{CX + 54}" cy="{CY - 45}" r="1.5"/>
      <circle cx="{CX + 57}" cy="{CY - 70}" r="1.5"/>
      <circle cx="{CX + 59}" cy="{CY - 95}" r="1.5"/>
      <circle cx="{CX + 62}" cy="{CY - 120}" r="1.5"/>
    </g>

    <!-- Planned Trajectory Path (Smooth Bezier with animated flow) -->
    <path d="M {CX} {CY} Q {CX - 4} {CY - 60} {CX + 8} {CY - 135}" fill="none" stroke="{GREEN}" stroke-width="2.5" stroke-linecap="round" stroke-dasharray="6,4">
      <animate attributeName="stroke-dashoffset" values="0;-20" dur="0.8s" repeatCount="indefinite"/>
    </path>

    <!-- Detected Obstacle 1: Lead Vehicle Ahead (3D Bounding Box) -->
    <!-- Detected Obstacle 1: Lead Vehicle Ahead (Full Vector Car + 3D Bounding Box) -->
    <g transform="translate({CX + 5},{CY - 105})">
      <!-- 3D Bounding Box Wireframe -->
      <rect x="-16" y="-22" width="32" height="44" rx="3" fill="{GREEN}" fill-opacity="0.08" stroke="{GREEN}" stroke-width="1.2" stroke-dasharray="3,2"/>
      
      <!-- Lead Car Model (Top View) -->
      <!-- Wheels -->
      <rect x="-18" y="-18" width="4" height="8" rx="1" fill="{MUTED}"/>
      <rect x="14" y="-18" width="4" height="8" rx="1" fill="{MUTED}"/>
      <rect x="-18" y="8" width="4" height="8" rx="1" fill="{MUTED}"/>
      <rect x="14" y="8" width="4" height="8" rx="1" fill="{MUTED}"/>
      <!-- Chassis -->
      <rect x="-13" y="-20" width="26" height="38" rx="5" fill="#161b22" stroke="{GREEN}" stroke-width="1.2"/>
      <!-- Windshields -->
      <path d="M -9 -10 L 9 -10 L 7 -3 L -7 -3 Z" fill="{GREEN}" fill-opacity="0.25"/>
      <path d="M -8 5 L 8 5 L 7 11 L -7 11 Z" fill="{GREEN}" fill-opacity="0.2"/>
      <!-- Red Taillights -->
      <circle cx="-9" cy="17" r="2" fill="#ef4444"/>
      <circle cx="9" cy="17" r="2" fill="#ef4444"/>
      <!-- Front Lights -->
      <circle cx="-9" cy="-19" r="1.5" fill="{CYAN}"/>
      <circle cx="9" cy="-19" r="1.5" fill="{CYAN}"/>

      <!-- Velocity / Heading Vector Arrow -->
      <line x1="0" y1="-20" x2="0" y2="-32" stroke="{GREEN}" stroke-width="1.5"/>
      <polygon points="0,-35 -3,-30 3,-30" fill="{GREEN}"/>

      <!-- Track Tag Label -->
      <rect x="-30" y="-46" width="60" height="10" rx="2" fill="{BG}" stroke="{GREEN}" stroke-width="0.8"/>
      <text x="0" y="-38" fill="{GREEN}" font-size="7.5" font-weight="700" text-anchor="middle">CAR #01 : 42m</text>
    </g>

    <!-- Detected Obstacle 2: Pedestrian / Obstacle on Right -->
    <g transform="translate({CX + 75},{CY - 50})">
      <circle cx="0" cy="0" r="8" fill="{AMBER}" fill-opacity="0.15" stroke="{AMBER}" stroke-width="1.2">
        <animate attributeName="r" values="7;10;7" dur="1.5s" repeatCount="indefinite"/>
      </circle>
      <rect x="-18" y="-18" width="36" height="9" rx="2" fill="{BG}" stroke="{AMBER}" stroke-width="0.8"/>
      <text x="0" y="-11" fill="{AMBER}" font-size="7" font-weight="700" text-anchor="middle">PED : 28m</text>
    </g>

    <!-- Ego-Vehicle (Self-Driving Car at Center) -->
    <g transform="translate({CX},{CY})">
      <!-- Wheels -->
      <rect x="-16" y="-18" width="5" height="10" rx="1.5" fill="{MUTED}"/>
      <rect x="11" y="-18" width="5" height="10" rx="1.5" fill="{MUTED}"/>
      <rect x="-16" y="8" width="5" height="10" rx="1.5" fill="{MUTED}"/>
      <rect x="11" y="8" width="5" height="10" rx="1.5" fill="{MUTED}"/>
      <!-- Chassis -->
      <rect x="-12" y="-22" width="24" height="44" rx="6" fill="#161b22" stroke="{CYAN}" stroke-width="1.5"/>
      <!-- Windshield & Glass -->
      <path d="M -9 -10 L 9 -10 L 7 -2 L -7 -2 Z" fill="{CYAN}" fill-opacity="0.25"/>
      <path d="M -8 8 L 8 8 L 7 14 L -7 14 Z" fill="{CYAN}" fill-opacity="0.2"/>
      <!-- Roof LiDAR Sensor Puck with pulsing wave -->
      <circle cx="0" cy="3" r="4.5" fill="{BLUE}" stroke="{TEXT}" stroke-width="1"/>
      <circle cx="0" cy="3" r="8" fill="none" stroke="{CYAN}" stroke-width="1" opacity="0.7">
        <animate attributeName="r" values="4.5;14" dur="1.6s" repeatCount="indefinite"/>
        <animate attributeName="opacity" values="0.9;0" dur="1.6s" repeatCount="indefinite"/>
      </circle>
      <!-- Forward Headlight Beams -->
      <polygon points="-9,-22 -16,-34 -7,-34 -6,-22" fill="{CYAN}" fill-opacity="0.3"/>
      <polygon points="9,-22 16,-34 7,-34 6,-22" fill="{CYAN}" fill-opacity="0.3"/>
    </g>

    <!-- Corner Telemetry Overlay HUD Badges -->
    <g font-size="9" font-weight="700">
      <!-- Top Left: Node Status -->
      <rect x="20" y="{TITLEBAR_H + 12}" width="118" height="18" rx="4" fill="{BG}" fill-opacity="0.85" stroke="{FRAME}" stroke-width="0.8"/>
      <circle cx="28" cy="{TITLEBAR_H + 21}" r="3" fill="{GREEN}"/>
      <text x="36" y="{TITLEBAR_H + 24}" fill="{TEXT}">LiDAR: <tspan fill="{GREEN}">20Hz LOCK</tspan></text>

      <!-- Top Right: Perception Track Count -->
      <rect x="{W - 138}" y="{TITLEBAR_H + 12}" width="118" height="18" rx="4" fill="{BG}" fill-opacity="0.85" stroke="{FRAME}" stroke-width="0.8"/>
      <text x="{W - 130}" y="{TITLEBAR_H + 24}" fill="{TEXT}">TRACKS: <tspan fill="{CYAN}">2 OBJECTS</tspan></text>

      <!-- Bottom Left: Autonomous Mode -->
      <rect x="20" y="{H - STATUS_H - 26}" width="124" height="18" rx="4" fill="{BG}" fill-opacity="0.85" stroke="{FRAME}" stroke-width="0.8"/>
      <text x="28" y="{H - STATUS_H - 14}" fill="{TEXT}">MODE: <tspan fill="{CYAN}">AUTONOMOUS</tspan></text>

      <!-- Bottom Right: Latency & Fusion -->
      <rect x="{W - 128}" y="{H - STATUS_H - 26}" width="108" height="18" rx="4" fill="{BG}" fill-opacity="0.85" stroke="{FRAME}" stroke-width="0.8"/>
      <text x="{W - 120}" y="{H - STATUS_H - 14}" fill="{TEXT}">LATENCY: <tspan fill="{GREEN}">11.2ms</tspan></text>
    </g>
  </g>

  <!-- Bottom Command Status Bar -->
  <line x1="0" y1="{H - STATUS_H}" x2="{W}" y2="{H - STATUS_H}" stroke="{FRAME}"/>
  <text x="{PAD}" y="{H - 12}" fill="{MUTED}" font-size="11.5">
    baysatriow@github:~$ <tspan fill="{GREEN}">rviz2</tspan> <tspan fill="{CYAN}">-d perception.rviz</tspan>
  </text>
  <rect x="{PAD + 215}" y="{H - 23}" width="7" height="13" fill="{CYAN}">
    <animate attributeName="opacity" values="1;1;0;0" keyTimes="0;0.5;0.51;1" dur="1s" repeatCount="indefinite"/>
  </rect>
</svg>"""

with open(OUT, "w", encoding="utf-8") as f:
    f.write(svg)
print(f"wrote {OUT} ({len(svg)} bytes; {W} x {H})")

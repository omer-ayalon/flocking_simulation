# 🐦 Boids Simulation

A 2D **Boids Simulation** in Python using **NumPy** and **Pygame**.  
Each boid is represented as a small triangle that moves according to simple steering rules, producing realistic flocking behavior.

---
## DEMO
![](demo/demo.gif)

---

## ✨ Features

### 🪶 Core Flocking Behaviors
- **Cohesion** → Boids steer toward the average position of nearby neighbors.  
- **Alignment** → Boids align their velocity with nearby neighbors.  
- **Separation** → Boids steer away from neighbors that are too close to avoid collisions.

### 🌍 Environment Constraints
- **Avoid Borders** → Boids steer away from simulation edges with strength increasing near the border.  
- **Enforce Bounds** → Hard constraint ensuring boids never leave the simulation window.  
- **Barrier Avoidance** → Boids steer around obstacles:
  - Force increases *exponentially* when close.  
  - Adjustable radius of influence (`BERIER_RADIUS`).  

### 🖱️ Interactivity
- **Follow Mouse** → Boids steer their *heading* toward the mouse cursor.  
  - Heading correction is stronger when closer.  
  - Speed remains constant (only direction changes).  

### 🎨 Visualization
- Boids are rendered as **triangles** pointing in their direction of travel.  

---

## ⚙️ Parameters

Tune these parameters to change the simulation behavior using the sliders:

| Parameter             | Description                               |
|-----------------------|-------------------------------------------|
| `Cohesion force`      | Strength of cohesion force                |
| `Alignment force`     | Strength of alignment force               |
| `Separation force`    | Strength of separation force              |
| `Berier avoid force`  | Strength of avoiding the placed beriers   |
| `Mouse follow force`  | Strength of following the mouse cursor    |
| `Cohesion raduis`     | Raduis of cohesion force                  |
| `Alignment raduis`    | Raduis of alignment force                 |
| `Separation raduis`   | Raduis of separation force                |
| `Berier avoid radius` | Radius of barrier influence               |

---

## 🏃 Run the Simulation

1. Install dependencies:<br>
    pip install pygame numpy
2. Run:<br>
    python flocking_simulation.py
3. Controls:<br>
    * Right click and move the mouse → boids will follow.
    * Left click to add barriers → boids will avoid them.
import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
import pygame
import numpy as np


class Boid():
    def __init__(self, pos, velocity, acceleration, screen_size):
        self.position = pos
        self.velocity = velocity
        self.acceleration = acceleration
        self.screen_size = screen_size

        # Perception radius
        self.cohesion_radius = 50
        self.alignment_radius = 30
        self.separation_radius = 50
        self.avoidance_radius = 20

        # Maximum force
        self.cohesion_force_limit = 0.3
        self.alignment_force_limit = 0.1
        self.separation_force_limit = 0.3
        self.desired_speed = 5.0
        self.avoidance_force_limit = 0.01
   
    def flock(self, boids):
        self.cohesion(boids)
        self.alignment(boids)
        self.separation(boids)
        self.speed()

    def update(self):
        # Update velocity
        self.velocity += self.acceleration
        # Update position
        self.position += self.velocity
        self.position = self.position % np.array(self.screen_size)  # Wrap around screen edges
        # Reset acceleration
        self.acceleration = np.zeros(2)

    def cohesion(self, boids):
        # Calculate the average position of nearby boids (the center of mass)
        positions = np.array([b.position for b in boids])
        dists = np.linalg.norm(positions - self.position, axis=1)
        mask = dists < self.cohesion_radius
        if np.any(mask):
            center_of_mass = positions[mask].mean(axis=0)
            cohesion_force = np.clip(center_of_mass - self.position, -self.cohesion_force_limit, self.cohesion_force_limit)
            self.acceleration += cohesion_force

    def alignment(self, boids):
        # Align velocity with nearby boids
        positions = np.array([b.position for b in boids])
        velocities = np.array([b.velocity for b in boids])
        dists = np.linalg.norm(positions - self.position, axis=1)
        mask = dists < self.alignment_radius
        if np.any(mask):
            center_of_heading = velocities[mask].mean(axis=0)
            alignment_force = np.clip(center_of_heading - self.velocity, -self.alignment_force_limit, self.alignment_force_limit)
            self.acceleration += alignment_force

    def separation(self, boids):
        # Avoid crowding nearby boids
        positions = np.array([b.position for b in boids])
        dists = np.linalg.norm(positions - self.position, axis=1)
        mask = (dists < self.separation_radius) & (dists > 1e-8)
        if np.any(mask):
            diff = self.position - positions[mask]
            diff /= dists[mask][:, np.newaxis]  # Weight by distance
            separation_force = np.sum(diff, axis=0)
            separation_force = np.clip(separation_force, -self.separation_force_limit, self.separation_force_limit)  # Limit the force
            self.acceleration += separation_force

    def avoid(self, barriers):
        # Avoid barriers with stronger force as boid gets closer
        positions = np.array([b.position for b in barriers])
        dists = np.linalg.norm(positions - self.position, axis=1)
        mask = (dists < self.avoidance_radius) & (dists > 1e-8)
        if np.any(mask):
            diff = self.position - positions[mask]
            # Weight by 1/distance (stronger when closer)
            weights = 1.0 / dists[mask][:, np.newaxis]
            diff = diff * weights
            avoidance_force = np.sum(diff, axis=0)
            avoidance_force = avoidance_force*0.05 + self.velocity
            avoidance_force = np.clip(avoidance_force, -self.avoidance_force_limit, self.avoidance_force_limit)  # Limit the force
            self.acceleration += avoidance_force

    def speed(self):
        # Boids want to maintain a certain speed (magnitude), not direction
        current_speed = np.linalg.norm(self.velocity)
        if current_speed == 0:
            return
        desired_velocity = self.velocity / current_speed * self.desired_speed
        diff_velocity = desired_velocity - self.velocity
        self.acceleration += diff_velocity * 0.01  # Adjust factor as needed
        

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 255, 255), self.position.astype(int), 5)
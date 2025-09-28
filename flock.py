import numpy as np
import pygame


class Flock():
    def __init__(self, num_boids, screen_size):
        self.COHESION_RADIUS = 50
        self.ALIGNMENT_RADIUS = 100
        self.SEPARATION_RADIUS = 100

        self.COHESION_DAMP = 0.12
        self.ALIGNMENT_DAMP = 0.1
        self.SEPARATION_DAMP = 0.1
        self.OLD_VELOCITY_DAMP = 0.5

        self.positions = []
        self.velocities = []
        self.accelerations = []

        self.num_boids = num_boids
        self.screen_size = screen_size[::-1]

        self.base_triangle = np.array([
            [10,  0],    # tip pointing up
            [-15, -5],   # bottom-left
            [-15,  5],   # bottom-right
        ], dtype=float)

        self.initialize_boids()

    def initialize_boids(self):
        self.positions = np.random.rand(self.num_boids, 2) * self.screen_size
        self.velocities = np.random.uniform(0.5, 3, (self.num_boids, 2))
        self.accelerations = np.zeros((self.num_boids, 2))

    def update(self):
        cohesion_force = self.cohesion()
        alignment_force = self.alignment()
        separation_force = self.separation()

        # Weighted sum
        desired =   (cohesion_force * self.COHESION_DAMP +
                     alignment_force * self.ALIGNMENT_DAMP +
                     separation_force * self.SEPARATION_DAMP)
        
        # desired =   (cohesion_force * self.COHESION_DAMP)
        # desired =   (alignment_force * self.ALIGNMENT_DAMP)
        # desired =   (separation_force * self.SEPARATION_DAMP)

        desired = self.OLD_VELOCITY_DAMP * desired + (1-self.OLD_VELOCITY_DAMP) * self.velocities

        # Rescale to current speed
        speeds = np.linalg.norm(self.velocities, axis=1, keepdims=True)
        desired_norm = np.linalg.norm(desired, axis=1, keepdims=True)
        desired_unit = desired / np.maximum(desired_norm, 1e-8)
        desired_velocity = desired_unit * speeds

        self.velocities = desired_velocity

        # speed = np.linalg.norm(velocities, axis=1)
        # sum_speed = np.sum(speed)
        # print(sum_speed / self.num_boids)

        self.positions += self.velocities

        # Wrap boids around the screen
        self.positions %= self.screen_size

    def cohesion(self):
        """
        Boids steer toward the center of mass of nearby boids.
        Steering is limited by COHESION_MAX_FORCE to avoid acceleration spikes.
        """
        # Pairwise differences and distances
        diffs = self.positions[:, None, :] - self.positions[None, :, :]  # (N, N, 2)
        dists = np.linalg.norm(diffs, axis=2)                            # (N, N)

        # Mask neighbors within cohesion radius (exclude self)
        mask = (dists > 0) & (dists < self.COHESION_RADIUS)
        mask_exp = mask[:, :, None]  # expand for broadcasting

        # Average neighbor positions
        masked_positions = self.positions[None, :, :] * mask_exp # (N, N, 2)
        sum_neighbors = masked_positions.sum(axis=1)             # (N, 2)
        num_neighbors = mask_exp.sum(axis=1)                     # (N, 1)
        num_neighbors[num_neighbors == 0] = 1                    # avoid division by zero
        avg_neighbors = sum_neighbors / num_neighbors            # (N, 2)

        # Desired direction toward neighbors
        direction = avg_neighbors - self.positions               # (N, 2)
        norms = np.linalg.norm(direction, axis=1, keepdims=True) # (N, 1)
        norms[norms == 0] = 1                                    # avoid division by zero
        unit_dir = direction / norms                             # unit vector, preserves heading

        return unit_dir

    def alignment(self):
        """
        Boids steer toward the average heading of nearby boids.
        Preserves original speed (no acceleration creep).
        """
        diffs = self.positions[:, None, :] - self.positions[None, :, :]
        dists = np.linalg.norm(diffs, axis=2)

        # Find neighbors
        mask = dists < self.ALIGNMENT_RADIUS
        mask_expanded = mask[:, :, None]

        # Normalize velocities to unit headings
        speeds = np.linalg.norm(self.velocities, axis=1, keepdims=True)  # (N,1)
        speeds[speeds == 0] = 1e-8
        unit_headings = self.velocities / speeds

        # Mask neighbors
        masked_headings = unit_headings[None, :, :] * mask_expanded
        sum_neighbors = np.sum(masked_headings, axis=1)
        num_neighbors = np.sum(mask, axis=1, keepdims=True)
        num_neighbors[num_neighbors == 0] = 1

        # Average neighbor heading
        avg_heading = sum_neighbors / num_neighbors

        # Normalize to unit vector
        avg_heading_norm = np.linalg.norm(avg_heading, axis=1, keepdims=True)
        avg_heading_unit = avg_heading / np.maximum(avg_heading_norm, 1e-8)

        return avg_heading_unit

    def separation(self):
        """
        Compute separation vectors for all boids.
        Steers boids away from neighbors without changing their speed.
        """
        # Pairwise vectors and distances
        diffs = self.positions[:, None, :] - self.positions[None, :, :]  # (N, N, 2)
        dists = np.linalg.norm(diffs, axis=2)                             # (N, N)

        # Mask neighbors that are too close (exclude self)
        mask = (dists > 0) & (dists < self.SEPARATION_RADIUS)
        mask_expanded = mask[:, :, None]  # (N, N, 1)

        # Compute repulsion vectors: inversely proportional to distance
        repulsion = diffs / np.maximum(dists[:, :, None]**2, 1e-8)
        masked_repulsion = repulsion * mask_expanded

        # Sum repulsion vectors for each boid
        separation_vectors = masked_repulsion.sum(axis=1)  # (N, 2)

        # If all neighbors are far, vector can be zero
        norms = np.linalg.norm(separation_vectors, axis=1, keepdims=True)
        norms[norms == 0] = 1  # avoid division by zero

        # Normalize to unit vector (preserve heading only)
        unit_vectors = separation_vectors / norms

        return unit_vectors

    def rotate(self):
        """
        Rotate a base polygon around origin and place it at each center.
        Returns array of shape (N, M, 2) where M = number of vertices.
        """
        # Convert angles to radians
        rad = np.arctan2(self.velocities[:,1], self.velocities[:,0]) # shape: (N, 2)

        # Compute cos/sin
        cos_a, sin_a = np.cos(rad), np.sin(rad) # shape: (N, 2)

        # Build rotation matrices for all triangles: shape (N, 2, 2)
        rot_mats = np.zeros((self.num_boids, 2, 2))
        rot_mats[:, 0, 0] = cos_a
        rot_mats[:, 0, 1] = -sin_a
        rot_mats[:, 1, 0] = sin_a
        rot_mats[:, 1, 1] = cos_a

        # Repeat base triangle for all centers: shape (N, M, 2)
        points = np.broadcast_to(self.base_triangle, (self.num_boids, *self.base_triangle.shape))

        # Rotate all points: use matmul
        # transpose last two axes of rot_mats to align multiplication
        rotated = np.matmul(points, np.transpose(rot_mats, (0, 2, 1)))

        # Shift all triangles to their centers
        return rotated + self.positions[:, None, :]

    def draw(self, screen):
        # Rotate the shapes according to the velocity
        rotated_polygons = self.rotate()
        # Shift the positions array to pygame positions
        rotated_polygons = rotated_polygons[:, :, ::-1]
        # Draw polygons
        for poly in rotated_polygons:
            pygame.draw.polygon(screen, (255,255,255), poly)
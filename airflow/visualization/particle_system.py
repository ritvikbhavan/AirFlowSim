from __future__ import annotations

import numpy as np
import pyvista as pv


class ParticleSystem:
    def __init__(self, max_particles: int = 120) -> None:
        self.max_particles = max_particles
        self.positions = np.zeros((max_particles, 3), dtype=float)
        self.velocities = np.zeros((max_particles, 3), dtype=float)
        self._initialize()
        self.mesh = pv.PolyData(self.positions)
        self.actor = None

    def _initialize(self) -> None:
        for i in range(self.max_particles):
            self.positions[i] = (0.0, 0.0, 8.6)
            self.velocities[i] = (0.0, 0.0, -2.0)

    def update(self, dt: float) -> None:
        angles = np.linspace(0.0, 2 * np.pi, self.max_particles)
        self.positions[:, 2] -= 1.4 * dt * 10.0
        self.positions[:, 0] += np.cos(angles) * 0.045
        self.positions[:, 1] += np.sin(angles) * 0.045
        self.positions[:, 2] += np.sin(angles) * 0.03
        self.positions[:, 0] += np.clip(np.sin(angles + 0.5), -0.2, 0.2) * 0.02
        self.positions[:, 1] += np.clip(np.cos(angles + 0.5), -0.2, 0.2) * 0.02
        self.positions[self.positions[:, 2] < 0.0] = (0.0, 0.0, 8.6)
        self.mesh = pv.PolyData(self.positions)

    def vectors(self) -> np.ndarray:
        angles = np.linspace(0.0, 2 * np.pi, self.max_particles)
        directions = np.column_stack([
            np.cos(angles) * 0.8,
            np.sin(angles) * 0.8,
            -1.8 + np.sin(angles) * 0.15,
        ])
        return directions

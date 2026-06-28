"""
ParticleCloud

A high-performance, vectorized particle storage class for AirFlowSim.

Instead of storing one Python object per particle, all particle
properties are stored in contiguous NumPy arrays for maximum
performance.

This class is intentionally independent of rendering. Rendering
systems consume the positions array but never modify it directly.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray


FloatArray = NDArray[np.float64]
BoolArray = NDArray[np.bool_]


@dataclass(slots=True)
class ParticleCloud:
    """
    Stores all particles in contiguous NumPy arrays.

    Attributes
    ----------
    capacity
        Maximum number of particles.

    positions
        Particle positions (N x 3).

    velocities
        Particle velocities (N x 3).

    ages
        Current particle ages in seconds.

    lifetimes
        Maximum lifetime for each particle.

    alive
        Boolean mask indicating active particles.
    """

    capacity: int

    def __post_init__(self) -> None:
        self.positions: FloatArray = np.zeros((self.capacity, 3), dtype=np.float64)
        self.velocities: FloatArray = np.zeros((self.capacity, 3), dtype=np.float64)

        self.ages: FloatArray = np.zeros(self.capacity, dtype=np.float64)
        self.lifetimes: FloatArray = np.zeros(self.capacity, dtype=np.float64)

        self.alive: BoolArray = np.zeros(self.capacity, dtype=bool)

    @property
    def active_count(self) -> int:
        """Return number of active particles."""
        return int(np.count_nonzero(self.alive))

    @property
    def inactive_indices(self) -> NDArray[np.int64]:
        """Return indices of inactive particles."""
        return np.flatnonzero(~self.alive)

    @property
    def active_indices(self) -> NDArray[np.int64]:
        """Return indices of active particles."""
        return np.flatnonzero(self.alive)

    def spawn(
        self,
        position: FloatArray,
        velocity: FloatArray,
        lifetime: float,
        count: int = 1,
    ) -> int:
        """
        Spawn one or more particles.

        Parameters
        ----------
        position
            Initial particle position (3,)

        velocity
            Initial particle velocity (3,)

        lifetime
            Particle lifetime in seconds.

        count
            Number of particles to spawn.

        Returns
        -------
        int
            Number of particles successfully spawned.
        """

        available = self.inactive_indices

        if available.size == 0:
            return 0

        count = min(count, available.size)

        indices = available[:count]

        self.positions[indices] = position
        self.velocities[indices] = velocity

        self.ages[indices] = 0.0
        self.lifetimes[indices] = lifetime
        self.alive[indices] = True

        return count

    def kill(self, indices: NDArray[np.int64]) -> None:
        """
        Deactivate particles.
        """
        self.alive[indices] = False

    def advance(self, dt: float) -> None:
        """
        Advance particle positions using simple Euler integration.
        """

        if not np.any(self.alive):
            return

        active = self.alive

        self.positions[active] += self.velocities[active] * dt
        self.ages[active] += dt

        expired = active & (self.ages >= self.lifetimes)

        if np.any(expired):
            self.alive[expired] = False

    def clear(self) -> None:
        """
        Remove every particle.
        """

        self.positions.fill(0.0)
        self.velocities.fill(0.0)

        self.ages.fill(0.0)
        self.lifetimes.fill(0.0)

        self.alive.fill(False)

    def resize(self, new_capacity: int) -> None:
        """
        Resize the particle cloud while preserving existing particles.
        """

        if new_capacity == self.capacity:
            return

        old_capacity = self.capacity

        positions = np.zeros((new_capacity, 3), dtype=np.float64)
        velocities = np.zeros((new_capacity, 3), dtype=np.float64)

        ages = np.zeros(new_capacity, dtype=np.float64)
        lifetimes = np.zeros(new_capacity, dtype=np.float64)

        alive = np.zeros(new_capacity, dtype=bool)

        keep = min(old_capacity, new_capacity)

        positions[:keep] = self.positions[:keep]
        velocities[:keep] = self.velocities[:keep]

        ages[:keep] = self.ages[:keep]
        lifetimes[:keep] = self.lifetimes[:keep]

        alive[:keep] = self.alive[:keep]

        self.capacity = new_capacity

        self.positions = positions
        self.velocities = velocities

        self.ages = ages
        self.lifetimes = lifetimes

        self.alive = alive
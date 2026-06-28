from __future__ import annotations

import numpy as np

from airflow.physics.integrator import EulerIntegrator
from airflow.physics.velocity_field import VelocityField


class SimulationEngine:
    """
    Coordinates the airflow simulation.

    During the migration to ParticleCloud this engine supports both

    1. Legacy ParticleSystem
    2. New ParticleCloud

    Once the migration is complete the legacy update path can be removed.
    """

    def __init__(self, velocity_field: VelocityField):
        self.velocity_field = velocity_field
        self.integrator = EulerIntegrator()

    def update(self, particle_system, dt: float) -> None:
        """
        Advance the simulation.

        This method automatically detects whether the particle system is
        using the legacy particle list or the new ParticleCloud.
        """

        if hasattr(particle_system, "cloud"):
            self._update_cloud(particle_system, dt)
        else:
            self._update_legacy(particle_system, dt)

    def _update_legacy(self, particle_system, dt: float) -> None:
        """
        Existing particle update path.

        This remains unchanged so the simulator behaves exactly as before
        until ParticleSystem is migrated.
        """

        for particle in particle_system.particles:

            velocity = self.velocity_field.sample(particle.position)

            particle.position = self.integrator.integrate(
                particle.position,
                velocity,
                dt,
            )

        particle_system.sync_mesh()

    def _update_cloud(self, particle_system, dt: float) -> None:
        """
        Update the new vectorized ParticleCloud.

        This method will become the primary simulation path once the
        migration is complete.
        """

        cloud = particle_system.cloud

        if cloud.active_count == 0:
            return

        active = cloud.alive

        positions = cloud.positions[active]

        velocities = np.array(
            [self.velocity_field.sample(position) for position in positions],
            dtype=np.float64,
        )

        cloud.velocities[active] = velocities

        cloud.advance(dt)

        particle_system.sync_mesh()
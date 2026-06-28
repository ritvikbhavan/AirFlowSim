from __future__ import annotations

import numpy as np

from airflow.physics.integrator import EulerIntegrator
from airflow.physics.velocity_field import VelocityField


class SimulationEngine:
    """
    Coordinates the physics simulation.

    The engine computes particle motion. Rendering classes should only
    display particle positions.
    """

    def __init__(self, velocity_field: VelocityField):
        self.velocity_field = velocity_field
        self.integrator = EulerIntegrator()

    def update(self, particle_system, dt: float) -> None:
        """
        Advance the simulation by dt seconds.
        """

        for particle in particle_system.particles:

            velocity = self.velocity_field.sample(particle.position)

            particle.position = self.integrator.integrate(
                particle.position,
                velocity,
                dt,
            )

        particle_system.sync_mesh()
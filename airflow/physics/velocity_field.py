from __future__ import annotations

import numpy as np

from airflow.physics.fan_model import FanModel


class VelocityField:
    """
    Represents the velocity field within the room.

    Initially it is simply the sum of all fan contributions.

    Later it will include:

    - pressure
    - turbulence
    - obstacle influence
    - HVAC
    - Navier-Stokes solver
    """

    def __init__(self):

        self._fans: list[FanModel] = []

    def add_fan(
        self,
        fan: FanModel,
    ):

        self._fans.append(fan)

    def sample(
        self,
        position: np.ndarray,
    ) -> np.ndarray:

        velocity = np.zeros(
            3,
            dtype=float,
        )

        for fan in self._fans:

            velocity += fan.velocity_at(position)

        return velocity
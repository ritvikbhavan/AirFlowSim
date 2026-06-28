from __future__ import annotations

import math

import numpy as np


class FanModel:
    """
    Simplified ceiling fan model.

    Produces a downward jet with a slight rotational component.
    """

    def __init__(
        self,
        center: tuple[float, float, float],
        diameter: float,
        rpm: float,
        max_velocity: float = 6.0,
    ):

        self.center = np.asarray(center, dtype=float)

        self.radius = diameter / 2.0

        self.rpm = rpm

        self.max_velocity = max_velocity

    def velocity_at(
        self,
        position: np.ndarray,
    ) -> np.ndarray:

        dx = position[0] - self.center[0]
        dy = position[1] - self.center[1]
        dz = self.center[2] - position[2]

        # Ignore particles above the fan.
        if dz < 0:
            return np.zeros(3)

        r = math.sqrt(dx * dx + dy * dy)

        influence_radius = self.radius * 4.0

        if r > influence_radius:
            return np.zeros(3)

        radial_factor = math.exp(-(r / influence_radius) ** 2)

        vertical_decay = math.exp(-dz / 8.0)

        vz = -self.max_velocity * radial_factor * vertical_decay

        if r > 1e-4:

            tx = -dy / r
            ty = dx / r

            swirl = (
                0.15
                * self.max_velocity
                * radial_factor
            )

            vx = swirl * tx
            vy = swirl * ty

        else:

            vx = 0.0
            vy = 0.0

        return np.array(
            [
                vx,
                vy,
                vz,
            ],
            dtype=float,
        )
from __future__ import annotations

import numpy as np


class EulerIntegrator:
    """
    Simple Euler integrator.

    Later this can be replaced with RK4 or Verlet without
    changing any rendering code.
    """

    @staticmethod
    def integrate(
        position: np.ndarray,
        velocity: np.ndarray,
        dt: float,
    ) -> np.ndarray:

        return position + velocity * dt
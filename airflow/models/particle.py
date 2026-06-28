from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(slots=True)
class Particle:
    position: np.ndarray
    velocity: np.ndarray
    age: float
    lifetime: float
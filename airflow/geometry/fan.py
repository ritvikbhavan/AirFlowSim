from __future__ import annotations
from airflow.config import settings

import numpy as np
import pyvista as pv


class Fan:
    def __init__(self) -> None:
        self.radius = settings.FAN_RADIUS
        self.height = settings.FAN_HEIGHT
        self.center = settings.FAN_CENTER
        self.mesh = pv.Cylinder(center=self.center, direction=(0.0, 0.0, 1.0), radius=self.radius / 2.0, height=self.height)
        self.blades = []
        for angle in [0, 120, 240]:
            blade = pv.Cylinder(center=(self.center[0], self.center[1], self.center[2]), direction=(0.0, 0.0, 1.0), radius=0.05, height=2.2)
            blade.rotate_z(angle, point=self.center, inplace=True)
            self.blades.append(blade)
        self.blades = pv.MultiBlock(self.blades)

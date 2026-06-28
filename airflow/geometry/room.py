from __future__ import annotations
from airflow.config import settings

import pyvista as pv


class Room:
    def __init__(self) -> None:
        self.length = settings.ROOM_LENGTH
        self.width = settings.ROOM_WIDTH
        self.height = settings.ROOM_HEIGHT
        self.mesh = pv.Box(bounds=(-self.length / 2.0, self.length / 2.0, -self.width / 2.0, self.width / 2.0, 0.0, self.height))
        self.floor = pv.Box(bounds=(-self.length / 2.0, self.length / 2.0, -self.width / 2.0, self.width / 2.0, -0.05, 0.05))
        self.columns = self._build_columns()

    def _build_columns(self) -> list[pv.DataObject]:
        positions = [(-22.0, 0.0, 3.5), (22.0, 0.0, 3.5)]
        columns = []
        for x, y, z in positions:
            columns.append(
                pv.Cylinder(
                    center=(x, y, z),
                    direction=(0.0, 0.0, 1.0),
                    radius=1.6,
                    height=7.0,
                )
            )
        return columns

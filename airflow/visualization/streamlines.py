from __future__ import annotations

import numpy as np
import pyvista as pv

from airflow.physics.velocity_field import VelocityField


class StreamlineVisualization:
    def __init__(
        self,
        velocity_field: VelocityField,
        bounds: tuple[float, float, float, float, float, float],
        seed_center: tuple[float, float, float],
        seed_radius: float,
    ) -> None:
        self.velocity_field = velocity_field
        self.bounds = bounds
        self.seed_center = np.asarray(seed_center, dtype=float)
        self.seed_radius = seed_radius
        self.mesh = self._build_streamlines()
        self.actor = None

    def _build_streamlines(self) -> pv.PolyData:
        grid = self._build_velocity_grid()
        seeds = self._build_seed_points()

        if seeds.n_points == 0:
            return pv.PolyData()

        return grid.streamlines_from_source(
            seeds,
            vectors="velocity",
            integration_direction="forward",
            initial_step_length=0.2,
            max_step_length=0.6,
            max_steps=400,
            max_length=18.0,
            terminal_speed=0.01,
        )

    def _build_velocity_grid(self) -> pv.ImageData:
        xmin, xmax, ymin, ymax, zmin, zmax = self.bounds
        dimensions = (31, 31, 15)
        spacing = (
            (xmax - xmin) / (dimensions[0] - 1),
            (ymax - ymin) / (dimensions[1] - 1),
            (zmax - zmin) / (dimensions[2] - 1),
        )

        grid = pv.ImageData(
            dimensions=dimensions,
            spacing=spacing,
            origin=(xmin, ymin, zmin),
        )
        grid.point_data["velocity"] = np.array(
            [self.velocity_field.sample(point) for point in grid.points],
            dtype=float,
        )
        return grid

    def _build_seed_points(self) -> pv.PolyData:
        xmin, xmax, ymin, ymax, zmin, zmax = self.bounds
        radii = np.linspace(0.0, self.seed_radius, 5)
        angles = np.linspace(0.0, 2.0 * np.pi, 24, endpoint=False)
        points = []

        for radius in radii:
            for angle in angles:
                point = self.seed_center.copy()
                point[0] += radius * np.cos(angle)
                point[1] += radius * np.sin(angle)
                point[2] = min(max(point[2], zmin), zmax)

                if xmin <= point[0] <= xmax and ymin <= point[1] <= ymax:
                    points.append(point)

        return pv.PolyData(np.array(points, dtype=float))

from __future__ import annotations

import numpy as np
import pyvista as pv

from airflow.physics.velocity_field import VelocityField


class VelocityVectorVisualization:
    def __init__(
        self,
        velocity_field: VelocityField,
        bounds: tuple[float, float, float, float, float, float],
        dimensions: tuple[int, int, int] = (7, 7, 6),
        scale_factor: float = 0.35,
        min_magnitude: float = 0.05,
    ) -> None:
        self.velocity_field = velocity_field
        self.bounds = bounds
        self.dimensions = dimensions
        self.scale_factor = scale_factor
        self.min_magnitude = min_magnitude
        self.mesh = self._build_vectors()
        self.actor = None

    def _build_vectors(self) -> pv.PolyData:
        points = self._sample_points()
        velocities = np.array(
            [self.velocity_field.sample(point) for point in points],
            dtype=float,
        )
        magnitudes = np.linalg.norm(velocities, axis=1)
        active = magnitudes > self.min_magnitude

        if not np.any(active):
            return pv.PolyData()

        vector_points = points[active]
        vector_values = velocities[active]
        vector_magnitudes = magnitudes[active]

        point_cloud = pv.PolyData(vector_points)
        point_cloud["velocity"] = vector_values
        point_cloud["magnitude"] = vector_magnitudes

        return point_cloud.glyph(
            orient="velocity",
            scale="magnitude",
            factor=self.scale_factor,
            geom=pv.Arrow(),
        )

    def _sample_points(self) -> np.ndarray:
        xmin, xmax, ymin, ymax, zmin, zmax = self.bounds
        x_count, y_count, z_count = self.dimensions

        x_values = np.linspace(xmin, xmax, x_count)
        y_values = np.linspace(ymin, ymax, y_count)
        z_values = np.linspace(zmin, zmax, z_count)

        xx, yy, zz = np.meshgrid(
            x_values,
            y_values,
            z_values,
            indexing="ij",
        )
        return np.column_stack(
            [
                xx.ravel(),
                yy.ravel(),
                zz.ravel(),
            ]
        )

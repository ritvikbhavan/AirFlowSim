from __future__ import annotations

import numpy as np
import pyvista as pv

from airflow.geometry.room import Room
from airflow.geometry.fan import Fan
from airflow.visualization.particle_system import ParticleSystem


class RoomScene:
    def __init__(self, plotter) -> None:
        self.plotter = plotter
        self.room = Room()
        self.fan = Fan()
        self.particles = ParticleSystem()

    def build(self) -> None:
        self.plotter.add_mesh(self.room.mesh, color="lightblue", opacity=0.15, style="wireframe")
        self.plotter.add_mesh(self.room.floor, color="darkslategray", opacity=0.95)
        for column in self.room.columns:
            self.plotter.add_mesh(column, color="dimgray")
        self.plotter.add_mesh(self.fan.mesh, color="lightgray")
        self.plotter.add_mesh(self.fan.blades, color="orange")
        self.particles.actor = self.plotter.add_mesh(self.particles.mesh, color="lightblue", point_size=4)
        self.vector_actor = self.plotter.add_arrows(
            self.particles.positions[:25],
            self.particles.vectors()[:25],
            mag=2.2,
            color="cyan",
            opacity=0.75,
            point_size=0.0,
        )
        self.plotter.camera_position = 'iso'
        self.plotter.camera.azimuth = 45
        self.plotter.camera.elevation = 20
        self.plotter.camera.roll = 0
        self.plotter.reset_camera()

    def update(self, dt: float) -> None:
        self.particles.update(dt)
        if self.particles.actor is not None:
            self.plotter.remove_actor(self.particles.actor)
            self.particles.actor = None
        self.particles.actor = self.plotter.add_mesh(self.particles.mesh, color="lightblue", point_size=4)
        if hasattr(self, "vector_actor") and self.vector_actor is not None:
            self.plotter.remove_actor(self.vector_actor)
        self.vector_actor = self.plotter.add_arrows(
            self.particles.positions[:25],
            self.particles.vectors()[:25],
            mag=2.2,
            color="cyan",
            opacity=0.75,
            point_size=0.0,
        )

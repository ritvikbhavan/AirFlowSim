from __future__ import annotations

from airflow.config import settings
from airflow.geometry.room import Room
from airflow.geometry.fan import Fan
from airflow.physics.fan_model import FanModel
from airflow.physics.velocity_field import VelocityField
from airflow.visualization.particle_system import ParticleSystem
from airflow.visualization.streamlines import StreamlineVisualization


class RoomScene:
    def __init__(self, plotter) -> None:
        self.plotter = plotter
        self.room = Room()
        self.fan = Fan()
        self.particles = ParticleSystem()
        self.velocity_field = VelocityField()
        self.velocity_field.add_fan(
            FanModel(
                center=self.fan.center,
                diameter=self.fan.radius * 2.0,
                rpm=settings.FAN_RPM,
            )
        )
        self.streamlines: StreamlineVisualization | None = None
        self.streamlines_visible = False

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

    def set_streamlines_visible(self, visible: bool) -> None:
        self.streamlines_visible = visible
        self._sync_streamlines()

    def _sync_streamlines(self) -> None:
        if self.streamlines is None:
            if not self.streamlines_visible:
                return

            self.streamlines = StreamlineVisualization(
                velocity_field=self.velocity_field,
                bounds=self.room.mesh.bounds,
                seed_center=self.fan.center,
                seed_radius=self.fan.radius * 3.0,
            )

        if self.streamlines.mesh.n_points == 0:
            return

        if self.streamlines.actor is None:
            self.streamlines.actor = self.plotter.add_mesh(
                self.streamlines.mesh,
                color="deepskyblue",
                line_width=2,
                opacity=0.85,
            )

        self.streamlines.actor.SetVisibility(self.streamlines_visible)

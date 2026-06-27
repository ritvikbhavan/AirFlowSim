from __future__ import annotations

import math
import random
from typing import List

from config import ROOM_LENGTH, ROOM_WIDTH
from vtkmodules.vtkCommonColor import vtkNamedColors
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkRenderingCore import vtkActor, vtkPolyDataMapper, vtkRenderer


class ParticleSystem:
    def __init__(
        self,
        center: tuple[float, float, float] | None = None,
        radius: float = 1.0,
        speed: float = 4.0,
        max_particles: int = 120,
    ) -> None:
        self.center = center or (0.0, 0.0, 8.6)
        self.radius = radius
        self.speed = speed
        self.max_particles = max_particles
        self.colors = vtkNamedColors()
        self.particles: List[dict[str, object]] = []
        self.actors: List[vtkActor] = []
        self._initialize_particles()

    def create_actors(self, renderer: vtkRenderer) -> List[vtkActor]:
        self.actors = []
        self.particles = []

        for _ in range(self.max_particles):
            source = vtkSphereSource()
            source.SetRadius(0.08)
            source.SetThetaResolution(12)
            source.SetPhiResolution(12)

            mapper = vtkPolyDataMapper()
            mapper.SetInputConnection(source.GetOutputPort())

            actor = vtkActor()
            actor.SetMapper(mapper)
            actor.GetProperty().SetColor(self.colors.GetColor3d("LightSkyBlue"))
            actor.GetProperty().SetOpacity(0.95)
            actor.GetProperty().SetPointSize(2)
            renderer.AddActor(actor)

            self.actors.append(actor)
            self.particles.append(
                {
                    "position": self._random_position(),
                    "velocity": self._initial_velocity(),
                    "actor": actor,
                }
            )

        return self.actors

    def _initialize_particles(self) -> None:
        self.particles = []
        for _ in range(self.max_particles):
            self.particles.append(
                {
                    "position": self._random_position(),
                    "velocity": self._initial_velocity(),
                    "actor": None,
                }
            )

    def update(self, dt: float) -> None:
        for particle in self.particles:
            position = particle["position"]
            velocity = particle["velocity"]
            assert isinstance(position, tuple)
            assert isinstance(velocity, tuple)

            new_position = (
                position[0] + velocity[0] * dt,
                position[1] + velocity[1] * dt,
                position[2] + velocity[2] * dt,
            )
            new_velocity = (
                velocity[0] + random.uniform(-0.03, 0.03),
                velocity[1] + random.uniform(-0.03, 0.03),
                velocity[2] + random.uniform(-0.02, 0.02),
            )

            if (
                new_position[2] < -0.5
                or abs(new_position[0]) > ROOM_LENGTH / 2.0 + 5.0
                or abs(new_position[1]) > ROOM_WIDTH / 2.0 + 5.0
            ):
                particle["position"] = self._random_position()
                particle["velocity"] = self._initial_velocity()
            else:
                particle["position"] = new_position
                particle["velocity"] = new_velocity

            actor = particle["actor"]
            if actor is not None:
                actor.SetPosition(*particle["position"])

    def _random_position(self) -> tuple[float, float, float]:
        angle = random.uniform(0.0, 2.0 * math.pi)
        radius = random.uniform(0.0, self.radius)
        return (
            self.center[0] + radius * math.cos(angle),
            self.center[1] + radius * math.sin(angle),
            self.center[2] + random.uniform(-0.2, 0.2),
        )

    def _initial_velocity(self) -> tuple[float, float, float]:
        angle = random.uniform(0.0, 2.0 * math.pi)
        radial = random.uniform(0.0, 0.35)
        return (
            radial * math.cos(angle),
            radial * math.sin(angle),
            -self.speed + random.uniform(-0.2, 0.2),
        )

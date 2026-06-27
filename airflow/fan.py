from __future__ import annotations

from typing import List

from config import FAN_DIAMETER, FAN_HEIGHT, FAN_POSITION_Z
from vtkmodules.vtkCommonColor import vtkNamedColors
from vtkmodules.vtkFiltersSources import vtkCubeSource, vtkCylinderSource
from vtkmodules.vtkRenderingCore import vtkActor, vtkPolyDataMapper, vtkRenderer


class CeilingFan:
    def __init__(self, center: tuple[float, float, float] | None = None) -> None:
        self.center = center or (0.0, 0.0, FAN_POSITION_Z)
        self.colors = vtkNamedColors()

    def create_actors(self, renderer: vtkRenderer) -> List[vtkActor]:
        actors: List[vtkActor] = []

        motor = self._make_motor_actor()
        renderer.AddActor(motor)
        actors.append(motor)

        for blade_index in range(3):
            blade = self._make_blade_actor(blade_index)
            renderer.AddActor(blade)
            actors.append(blade)

        return actors

    def _make_motor_actor(self) -> vtkActor:
        source = vtkCylinderSource()
        source.SetResolution(24)
        source.SetRadius(0.7)
        source.SetHeight(FAN_HEIGHT)

        mapper = vtkPolyDataMapper()
        mapper.SetInputConnection(source.GetOutputPort())

        actor = vtkActor()
        actor.SetMapper(mapper)
        actor.SetPosition(self.center[0], self.center[1], self.center[2])
        actor.GetProperty().SetColor(self.colors.GetColor3d("LightGray"))
        return actor

    def _make_blade_actor(self, blade_index: int) -> vtkActor:
        source = vtkCubeSource()
        source.SetXLength(FAN_DIAMETER)
        source.SetYLength(0.18)
        source.SetZLength(0.06)

        mapper = vtkPolyDataMapper()
        mapper.SetInputConnection(source.GetOutputPort())

        actor = vtkActor()
        actor.SetMapper(mapper)
        actor.SetPosition(self.center[0], self.center[1], self.center[2])
        actor.RotateZ(blade_index * 120.0)
        actor.GetProperty().SetColor(self.colors.GetColor3d("DarkOrange"))
        return actor

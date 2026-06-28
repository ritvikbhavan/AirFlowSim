from __future__ import annotations

import os
from datetime import datetime

from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QAction, QImage, QPixmap
from PySide6.QtWidgets import QLabel, QMainWindow, QVBoxLayout, QWidget
import pyvista as pv

from airflow.scene.room_scene import RoomScene


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("AirFlowSim")
        self.resize(800, 600)
        self._setup_ui()

    def _setup_ui(self) -> None:
        container = QWidget(self)
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)

        self.image_label = QLabel("Initializing airflow scene…", self)
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setMinimumSize(640, 480)
        self.image_label.setStyleSheet("background-color: #111; color: white;")
        layout.addWidget(self.image_label)

        container.setLayout(layout)
        self.setCentralWidget(container)

        self.plotter = pv.Plotter(off_screen=True, window_size=(800, 600))
        self.room_scene = RoomScene(self.plotter)
        self.room_scene.build()
        self._setup_toolbar()
        self._render_scene()
        self._save_screenshot("startup")

        self._timer = QTimer(self)
        self._timer.timeout.connect(self._animate)
        self._timer.start(16)

    def _setup_toolbar(self) -> None:
        toolbar = self.addToolBar("Visualization")
        toolbar.setMovable(False)

        self.streamlines_action = QAction("Streamlines", self)
        self.streamlines_action.setCheckable(True)
        self.streamlines_action.toggled.connect(self._toggle_streamlines)
        toolbar.addAction(self.streamlines_action)

        self.velocity_vectors_action = QAction("Velocity Vectors", self)
        self.velocity_vectors_action.setCheckable(True)
        self.velocity_vectors_action.toggled.connect(self._toggle_velocity_vectors)
        toolbar.addAction(self.velocity_vectors_action)

    def _toggle_streamlines(self, checked: bool) -> None:
        self.room_scene.set_streamlines_visible(checked)
        self._render_scene()

    def _toggle_velocity_vectors(self, checked: bool) -> None:
        self.room_scene.set_velocity_vectors_visible(checked)
        self._render_scene()

    def _render_scene(self) -> None:
        image = self.plotter.screenshot(return_img=True)
        height, width, channel = image.shape
        qimage = QImage(image.data, width, height, width * channel, QImage.Format_RGB888)
        self.image_label.setPixmap(QPixmap.fromImage(qimage))

    def _animate(self) -> None:
        self.room_scene.update(0.016)
        self._render_scene()
        self._save_screenshot("frame")

    def _save_screenshot(self, tag: str) -> None:
        output_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "images")
        os.makedirs(output_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        path = os.path.join(output_dir, f"{tag}_{timestamp}.png")
        self.plotter.screenshot(path)

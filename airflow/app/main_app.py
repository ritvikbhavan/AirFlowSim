from __future__ import annotations

import os
import sys
import signal

from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QApplication

from airflow.gui.main_window import MainWindow


def _install_signal_handlers() -> None:
    def _handle_signal(signum, _frame) -> None:
        raise KeyboardInterrupt

    signal.signal(signal.SIGINT, _handle_signal)
    signal.signal(signal.SIGTERM, _handle_signal)


def main() -> int:
    if "QT_QPA_PLATFORM" not in os.environ:
        if os.name == "nt":
            os.environ["QT_QPA_PLATFORM"] = "windows"
        elif os.environ.get("DISPLAY"):
            os.environ["QT_QPA_PLATFORM"] = "xcb"
        else:
            os.environ["QT_QPA_PLATFORM"] = "offscreen"

    _install_signal_handlers()

    app = QApplication.instance() or QApplication(sys.argv)
    window = MainWindow()
    window.show()

    if os.environ.get("AIRFLOWSIM_HEADLESS") == "1":
        QTimer.singleShot(100, app.quit)

    try:
        return app.exec()
    except KeyboardInterrupt:
        app.quit()
        return 130

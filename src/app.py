"""Application bootstrap — creates QApplication, main window, and launches."""

import os
import sys

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QApplication

from src.controller.app_controller import AppController
from src.ui.main_window import MainWindow


def run():
    app = QApplication(sys.argv)
    app.setApplicationName("iSlide Clone")
    app.setOrganizationName("iSlideClone")

    # Default font
    font = QFont("Microsoft YaHei", 9)
    app.setFont(font)

    # Load stylesheet
    qss_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "resources", "styles", "theme.qss"
    )
    try:
        with open(qss_path, 'r', encoding='utf-8') as f:
            app.setStyleSheet(f.read())
    except Exception:
        pass  # OK if stylesheet missing

    # Create controller and window
    controller = AppController()
    window = MainWindow(controller)
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    run()

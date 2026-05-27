"""Application bootstrap — creates QApplication, main window, and launches."""

import os
import sys

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QApplication

from src import bundle_dir
from src.controller.app_controller import AppController
from src.ui.main_window import MainWindow


def run():
    app = QApplication(sys.argv)
    app.setApplicationName("SlideKit")
    app.setOrganizationName("SlideKit")

    # Default font
    font = QFont("Microsoft YaHei", 9)
    app.setFont(font)

    # Load stylesheet
    qss_path = os.path.join(bundle_dir(), "resources", "styles", "theme.qss")
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

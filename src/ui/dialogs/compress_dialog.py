"""CompressDialog — configure compression level and execute."""

from PyQt6.QtWidgets import (
    QComboBox, QDialog, QDialogButtonBox, QFormLayout, QLabel, QVBoxLayout
)

from src.controller.app_controller import AppController


class CompressDialog(QDialog):
    """Dialog for configuring PPT compression."""

    def __init__(self, controller: AppController, parent=None):
        super().__init__(parent)
        self._controller = controller
        self.setWindowTitle("Compress Presentation")
        self.setMinimumWidth(350)

        layout = QVBoxLayout(self)

        layout.addWidget(QLabel(
            "Compress your presentation by reducing image resolution\n"
            "and removing unused slide masters."
        ))

        form = QFormLayout()
        self._level = QComboBox()
        self._level.addItems(["Light (220 DPI)", "Normal (150 DPI)", "Aggressive (96 DPI)"])
        self._level.setCurrentIndex(1)
        form.addRow("Compression Level:", self._level)

        if controller.context:
            form.addRow(QLabel(f"File: {controller.context.name}"))
            form.addRow(QLabel(f"Slides: {controller.context.slide_count}"))

        layout.addLayout(form)

        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(self._apply)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def _apply(self):
        level_map = {0: "light", 1: "normal", 2: "aggressive"}
        level = level_map.get(self._level.currentIndex(), "normal")
        self._controller.execute_feature("compress", level=level)
        self.accept()

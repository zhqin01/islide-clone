"""CircularLayoutDialog — configure and apply circular/radial layout."""

from PyQt6.QtWidgets import (
    QCheckBox, QComboBox, QDialog, QDialogButtonBox, QDoubleSpinBox,
    QFormLayout, QLabel, QVBoxLayout
)

from src.controller.app_controller import AppController


class CircularLayoutDialog(QDialog):
    """Dialog for configuring circular layout parameters."""

    def __init__(self, controller: AppController, parent=None):
        super().__init__(parent)
        self._controller = controller
        self.setWindowTitle("Circular Layout")
        self.setMinimumWidth(350)

        layout = QVBoxLayout(self)
        form = QFormLayout()

        sel_count = controller.context.get_selected_shape_count() if controller.context else 0
        if sel_count > 0:
            form.addRow(QLabel(f"Selected shapes: {sel_count}"))

        self._radius = QDoubleSpinBox()
        self._radius.setRange(10, 1000)
        self._radius.setValue(controller.defaults.get("layout", {}).get("circular_default_radius", 200))
        self._radius.setSuffix(" pt")
        form.addRow("Radius:", self._radius)

        self._start_angle = QDoubleSpinBox()
        self._start_angle.setRange(0, 360)
        self._start_angle.setValue(controller.defaults.get("layout", {}).get("circular_default_start_angle", 0))
        self._start_angle.setSuffix(" °")
        form.addRow("Start Angle:", self._start_angle)

        self._direction = QComboBox()
        self._direction.addItems(["Clockwise", "Counterclockwise"])
        form.addRow("Direction:", self._direction)

        self._rotate = QCheckBox("Rotate shapes toward center")
        form.addRow(self._rotate)

        layout.addLayout(form)

        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(self._apply)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def _apply(self):
        self._controller.execute_feature(
            "circular_layout",
            radius=self._radius.value(),
            start_angle=self._start_angle.value(),
            clockwise=self._direction.currentIndex() == 0,
            rotate_shapes=self._rotate.isChecked(),
        )
        self.accept()

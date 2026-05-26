"""MatrixLayoutDialog — configure and apply matrix/grid layout."""

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QDialog, QDialogButtonBox, QFormLayout, QLabel, QSpinBox, QDoubleSpinBox, QVBoxLayout
)

from src.controller.app_controller import AppController


class MatrixLayoutDialog(QDialog):
    """Dialog for configuring matrix layout parameters."""

    def __init__(self, controller: AppController, parent=None):
        super().__init__(parent)
        self._controller = controller
        self.setWindowTitle("Matrix Layout")
        self.setMinimumWidth(350)

        layout = QVBoxLayout(self)

        form = QFormLayout()

        sel_count = controller.context.get_selected_shape_count() if controller.context else 0
        if sel_count > 0:
            form.addRow(QLabel(f"Selected shapes: {sel_count}"))

        self._columns = QSpinBox()
        self._columns.setRange(1, 20)
        self._columns.setValue(controller.defaults.get("layout", {}).get("matrix_default_columns", 3))
        form.addRow("Columns:", self._columns)

        self._h_gap = QDoubleSpinBox()
        self._h_gap.setRange(0, 500)
        self._h_gap.setValue(controller.defaults.get("layout", {}).get("matrix_default_h_gap", 20))
        self._h_gap.setSuffix(" pt")
        form.addRow("Horizontal Gap:", self._h_gap)

        self._v_gap = QDoubleSpinBox()
        self._v_gap.setRange(0, 500)
        self._v_gap.setValue(controller.defaults.get("layout", {}).get("matrix_default_v_gap", 20))
        self._v_gap.setSuffix(" pt")
        form.addRow("Vertical Gap:", self._v_gap)

        layout.addLayout(form)

        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(self._apply)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def _apply(self):
        self._controller.execute_feature(
            "matrix_layout",
            columns=self._columns.value(),
            h_gap=self._h_gap.value(),
            v_gap=self._v_gap.value(),
        )
        self.accept()

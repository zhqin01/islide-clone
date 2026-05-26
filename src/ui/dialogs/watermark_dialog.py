"""WatermarkDialog — configure and apply text or image watermark."""

from PyQt6.QtWidgets import (
    QCheckBox, QColorDialog, QComboBox, QDialog, QDialogButtonBox,
    QDoubleSpinBox, QFileDialog, QFormLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QSpinBox, QVBoxLayout,
)

from src.controller.app_controller import AppController


class WatermarkDialog(QDialog):
    """Dialog for configuring watermark parameters."""

    def __init__(self, controller: AppController, parent=None):
        super().__init__(parent)
        self._controller = controller
        self.setWindowTitle("Add Watermark")
        self.setMinimumWidth(420)

        layout = QVBoxLayout(self)

        form = QFormLayout()

        self._text = QLineEdit()
        defaults = controller.defaults.get("watermark", {})
        self._text.setText(defaults.get("default_text", "Confidential"))
        form.addRow("Watermark Text:", self._text)

        self._font_name = QComboBox()
        self._font_name.addItems(["Microsoft YaHei", "SimHei", "Arial", "Times New Roman"])
        form.addRow("Font:", self._font_name)

        self._font_size = QDoubleSpinBox()
        self._font_size.setRange(8, 144)
        self._font_size.setValue(36)
        self._font_size.setSuffix(" pt")
        form.addRow("Font Size:", self._font_size)

        self._opacity = QSpinBox()
        self._opacity.setRange(1, 100)
        self._opacity.setValue(defaults.get("default_opacity", 30))
        self._opacity.setSuffix(" %")
        form.addRow("Opacity:", self._opacity)

        self._rotation = QDoubleSpinBox()
        self._rotation.setRange(-180, 180)
        self._rotation.setValue(defaults.get("default_rotation", -45))
        self._rotation.setSuffix(" °")
        form.addRow("Rotation:", self._rotation)

        # Color picker
        color_row = QHBoxLayout()
        self._color_btn = QPushButton()
        self._color_btn.setFixedSize(30, 30)
        self._color_btn.setStyleSheet("background-color: #999999;")
        self._color_btn.clicked.connect(self._pick_color)
        color_row.addWidget(self._color_btn)
        self._color_hex = "999999"
        color_row.addWidget(QLabel("#999999"))
        self._color_label = color_row.itemAt(1).widget()
        color_row.addStretch()
        form.addRow("Color:", color_row)

        layout.addLayout(form)

        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(self._apply)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def _pick_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self._color_hex = color.name().lstrip('#')
            self._color_btn.setStyleSheet(f"background-color: #{self._color_hex};")
            self._color_label.setText(f"#{self._color_hex}")

    def _apply(self):
        self._controller.execute_feature(
            "add_watermark",
            text=self._text.text(),
            font_name=self._font_name.currentText(),
            font_size=self._font_size.value(),
            opacity=self._opacity.value(),
            rotation=self._rotation.value(),
            color_hex=self._color_hex,
        )
        self.accept()

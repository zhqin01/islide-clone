"""ExportDialog — export slides as images or long image."""

import os
from typing import List, Optional

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QCheckBox, QComboBox, QDialog, QDialogButtonBox, QFileDialog,
    QFormLayout, QHBoxLayout, QLabel, QListWidget, QListWidgetItem,
    QPushButton, QSpinBox, QVBoxLayout,
)

from src.controller.app_controller import AppController


class ExportDialog(QDialog):
    """Dialog for configuring image export."""

    def __init__(self, controller: AppController, parent=None, long_image_mode: bool = False):
        super().__init__(parent)
        self._controller = controller
        self._long_image_mode = long_image_mode

        title = "Export Long Image" if long_image_mode else "Export Slides to Images"
        self.setWindowTitle(title)
        self.setMinimumWidth(450)
        self.setMinimumHeight(400)

        layout = QVBoxLayout(self)

        # Format and DPI
        form = QFormLayout()

        if not long_image_mode:
            self._fmt = QComboBox()
            self._fmt.addItems(["PNG", "JPG"])
            form.addRow("Format:", self._fmt)

        self._dpi = QComboBox()
        self._dpi.addItems(["96", "150", "300"])
        self._dpi.setCurrentIndex(1)
        form.addRow("DPI:", self._dpi)

        layout.addLayout(form)

        # Slide selection
        layout.addWidget(QLabel("<b>Slides to export:</b>"))
        self._slide_list = QListWidget()
        ctx = controller.context
        if ctx:
            for i in range(ctx.slide_count):
                name = f"Slide {i + 1}"
                item = QListWidgetItem(name)
                item.setData(Qt.ItemDataRole.UserRole, i)
                item.setSelected(True)
                self._slide_list.addItem(item)

        # Select all / deselect all
        btn_row = QHBoxLayout()
        btn_all = QPushButton("Select All")
        btn_all.clicked.connect(lambda: self._slide_list.selectAll())
        btn_none = QPushButton("Deselect All")
        btn_none.clicked.connect(lambda: self._slide_list.clearSelection())
        btn_row.addWidget(btn_all)
        btn_row.addWidget(btn_none)
        btn_row.addStretch()
        layout.addLayout(btn_row)
        layout.addWidget(self._slide_list)

        # Output path
        path_row = QHBoxLayout()
        path_row.addWidget(QLabel("Output:"))
        self._path_label = QLabel("(not set)")
        path_row.addWidget(self._path_label, 1)
        btn_browse = QPushButton("Browse…")
        btn_browse.clicked.connect(self._browse_path)
        path_row.addWidget(btn_browse)
        layout.addLayout(path_row)

        # Buttons
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(self._apply)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def _browse_path(self):
        if self._long_image_mode:
            path, _ = QFileDialog.getSaveFileName(self, "Save Long Image", "", "PNG Files (*.png);;JPG Files (*.jpg)")
        else:
            path = QFileDialog.getExistingDirectory(self, "Select Output Directory")
        if path:
            self._path_label.setText(path)

    def _apply(self):
        output = self._path_label.text()
        if output == "(not set)" or not output:
            return

        dpi = int(self._dpi.currentText())

        # Get selected slides
        slides = [
            self._slide_list.item(i).data(Qt.ItemDataRole.UserRole)
            for i in range(self._slide_list.count())
            if self._slide_list.item(i).isSelected()
        ]

        if self._long_image_mode:
            self._controller.execute_feature(
                "export_long_image",
                output_path=output,
                fmt=self._fmt.currentText() if hasattr(self, '_fmt') else "PNG",
                dpi=dpi,
                slides=slides,
            )
        else:
            self._controller.execute_feature(
                "export_images",
                output_dir=output,
                fmt=self._fmt.currentText() if hasattr(self, '_fmt') else "PNG",
                dpi=dpi,
                slides=slides,
            )
        self.accept()

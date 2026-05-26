"""RibbonGroup — a labeled vertical group of controls within a RibbonTab."""

from typing import Callable, Optional

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QComboBox, QDoubleSpinBox, QFrame, QHBoxLayout, QLabel, QPushButton,
    QSpinBox, QToolButton, QVBoxLayout, QWidget,
)


class RibbonGroup(QWidget):
    """A labeled group of related controls (buttons, combos, spinners)."""

    def __init__(self, title: str, parent=None):
        super().__init__(parent)
        self.setObjectName("ribbonGroup")
        self._main_layout = QVBoxLayout(self)
        self._main_layout.setContentsMargins(2, 2, 2, 2)
        self._main_layout.setSpacing(2)

        # Controls row - can be multi-line
        self._controls_layout = QVBoxLayout()
        self._controls_layout.setSpacing(2)
        self._main_layout.addLayout(self._controls_layout)

        # Title label at bottom
        self._title_label = QLabel(title)
        self._title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._title_label.setStyleSheet("font-size: 10px; color: #777;")
        self._main_layout.addWidget(self._title_label)

    def add_button(self, text: str, callback: Callable[[], None]) -> QPushButton:
        btn = QPushButton(text)
        btn.clicked.connect(callback)
        btn.setFixedHeight(28)
        self._add_control(btn)
        return btn

    def add_tool_button(self, text: str, callback: Callable[[], None]) -> QToolButton:
        btn = QToolButton()
        btn.setText(text)
        btn.clicked.connect(callback)
        btn.setFixedSize(32, 28)
        self._add_control(btn)
        return btn

    def add_label(self, text: str) -> QLabel:
        lbl = QLabel(text)
        lbl.setStyleSheet("font-size: 10px; color: #555;")
        lbl.setFixedHeight(16)
        self._add_control(lbl)
        return lbl

    def add_combo(self, items: list, callback: Optional[Callable[[str], None]] = None) -> QComboBox:
        combo = QComboBox()
        combo.addItems(items)
        combo.setFixedHeight(26)
        if callback:
            combo.currentTextChanged.connect(callback)
        self._add_control(combo)
        return combo

    def add_spinbox(self, min_val: float, max_val: float, default: float, step: float = 1.0) -> QDoubleSpinBox:
        spin = QDoubleSpinBox()
        spin.setRange(min_val, max_val)
        spin.setValue(default)
        spin.setSingleStep(step)
        spin.setFixedHeight(26)
        spin.setFixedWidth(70)
        self._add_control(spin)
        return spin

    def add_separator(self):
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        self._add_control(line)

    def _add_control(self, widget: QWidget):
        self._controls_layout.addWidget(widget, alignment=Qt.AlignmentFlag.AlignLeft)

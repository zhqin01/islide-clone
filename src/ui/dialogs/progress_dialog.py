"""ProgressDialog — modal dialog with progress bar for long operations."""

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QDialog, QLabel, QProgressBar, QPushButton, QVBoxLayout
)


class ProgressDialog(QDialog):
    """Non-modal progress dialog with cancel support."""

    def __init__(self, title: str = "Processing…", cancelable: bool = False, parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setFixedSize(400, 120)
        self.setWindowFlags(Qt.WindowType.Dialog | Qt.WindowType.WindowTitleHint)
        self._cancelled = False

        layout = QVBoxLayout(self)

        self._label = QLabel("Please wait…")
        self._label.setWordWrap(True)
        layout.addWidget(self._label)

        self._progress = QProgressBar()
        self._progress.setRange(0, 100)
        self._progress.setValue(0)
        layout.addWidget(self._progress)

        if cancelable:
            btn = QPushButton("Cancel")
            btn.clicked.connect(self._on_cancel)
            layout.addWidget(btn)

    def set_progress(self, percent: int, message: str = ""):
        self._progress.setValue(percent)
        if message:
            self._label.setText(message)

    @property
    def cancelled(self) -> bool:
        return self._cancelled

    def _on_cancel(self):
        self._cancelled = True
        self.close()

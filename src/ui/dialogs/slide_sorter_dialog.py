"""SlideSorterDialog — manage slides: reorder, delete, duplicate."""

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QDialog, QDialogButtonBox, QHBoxLayout, QLabel, QListWidget,
    QListWidgetItem, QMessageBox, QPushButton, QVBoxLayout,
)

from src.controller.app_controller import AppController


class SlideSorterDialog(QDialog):
    """Dialog for batch slide management operations."""

    def __init__(self, controller: AppController, parent=None):
        super().__init__(parent)
        self._controller = controller
        self.setWindowTitle("Slide Manager")
        self.setMinimumSize(400, 500)

        layout = QVBoxLayout(self)

        ctx = controller.context
        if ctx:
            layout.addWidget(QLabel(f"<b>{ctx.name}</b> — {ctx.slide_count} slides"))
        layout.addWidget(QLabel("Select slides, then use the buttons below:"))

        self._list = QListWidget()
        self._list.setSelectionMode(QListWidget.SelectionMode.ExtendedSelection)
        if ctx:
            for proxy in ctx.get_slide_proxies():
                name = proxy.name or f"Slide {proxy.index + 1}"
                item = QListWidgetItem(f"  {proxy.index + 1}. {name}")
                item.setData(Qt.ItemDataRole.UserRole, proxy.index)
                self._list.addItem(item)
        layout.addWidget(self._list)

        # Button row
        btn_row = QHBoxLayout()
        btn_delete = QPushButton("Delete Selected")
        btn_delete.setStyleSheet("color: #c0392b;")
        btn_delete.clicked.connect(self._on_delete)
        btn_dup = QPushButton("Duplicate Selected")
        btn_dup.clicked.connect(self._on_duplicate)
        btn_up = QPushButton("Move Up")
        btn_up.clicked.connect(self._on_move_up)
        btn_down = QPushButton("Move Down")
        btn_down.clicked.connect(self._on_move_down)

        btn_row.addWidget(btn_delete)
        btn_row.addWidget(btn_dup)
        btn_row.addWidget(btn_up)
        btn_row.addWidget(btn_down)
        layout.addLayout(btn_row)

        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Close)
        buttons.rejected.connect(self.close)
        layout.addWidget(buttons)

    def _selected_indices(self):
        return [
            self._list.item(i).data(Qt.ItemDataRole.UserRole)
            for i in range(self._list.count())
            if self._list.item(i).isSelected()
        ]

    def _on_delete(self):
        indices = self._selected_indices()
        if not indices:
            return
        reply = QMessageBox.question(
            self, "Delete Slides",
            f"Delete {len(indices)} slide(s)? This cannot be undone.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.Yes:
            self._controller.execute_feature("slide_manager_delete", indices=indices)
            self._refresh()

    def _on_duplicate(self):
        indices = self._selected_indices()
        if indices:
            self._controller.execute_feature("slide_manager_duplicate", indices=indices)
            self._refresh()

    def _on_move_up(self):
        indices = self._selected_indices()
        if len(indices) == 1 and indices[0] > 0:
            self._controller.execute_feature("slide_manager_move", from_index=indices[0], to_index=indices[0] - 1)
            self._refresh()

    def _on_move_down(self):
        indices = self._selected_indices()
        ctx = self._controller.context
        if len(indices) == 1 and ctx and indices[0] < ctx.slide_count - 1:
            self._controller.execute_feature("slide_manager_move", from_index=indices[0], to_index=indices[0] + 2)
            self._refresh()

    def _refresh(self):
        self._list.clear()
        ctx = self._controller.context
        if ctx:
            self._controller.context = ctx  # refresh
            for proxy in ctx.get_slide_proxies():
                name = proxy.name or f"Slide {proxy.index + 1}"
                item = QListWidgetItem(f"  {proxy.index + 1}. {name}")
                item.setData(Qt.ItemDataRole.UserRole, proxy.index)
                self._list.addItem(item)

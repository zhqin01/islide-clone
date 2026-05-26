"""RibbonTab — a single tab page containing RibbonGroups laid out horizontally."""

from PyQt6.QtWidgets import QHBoxLayout, QWidget


class RibbonTab(QWidget):
    """One tab page in the ribbon. Contains groups laid out horizontally."""

    def __init__(self, name: str, parent=None):
        super().__init__(parent)
        self._name = name
        self._layout = QHBoxLayout(self)
        self._layout.setContentsMargins(6, 4, 6, 4)
        self._layout.setSpacing(4)
        self._layout.addStretch()

    @property
    def name(self) -> str:
        return self._name

    def add_group(self, group: "RibbonGroup"):
        # Insert before the stretch
        self._layout.insertWidget(self._layout.count() - 1, group)

"""RibbonWidget — container holding multiple RibbonTab pages via QTabWidget."""

from PyQt6.QtWidgets import QHBoxLayout, QTabWidget, QWidget


class RibbonWidget(QWidget):
    """The full ribbon bar. Hosts tabs in a QTabWidget."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("ribbon")
        self._layout = QHBoxLayout(self)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._tabs = QTabWidget()
        self._tabs.setDocumentMode(True)
        self._layout.addWidget(self._tabs)

    def add_tab(self, tab: "RibbonTab"):
        self._tabs.addTab(tab, tab.name)

    @property
    def tabs(self):
        return self._tabs

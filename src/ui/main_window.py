"""Main window — Ribbon UI shell with tabbed ribbon, slide strip, and status bar."""

from __future__ import annotations

from typing import List

from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QAction, QFont
from PyQt6.QtWidgets import (
    QFileDialog, QHBoxLayout, QLabel, QListWidget, QListWidgetItem,
    QMainWindow, QMessageBox, QSplitter, QStatusBar, QVBoxLayout, QWidget,
)

from src.controller.app_controller import AppController, SessionMode
from src.engine.base import EngineResult
from src.ui.ribbon import RibbonWidget
from src.ui.ribbon_tab import RibbonTab
from src.ui.ribbon_group import RibbonGroup


class MainWindow(QMainWindow):
    """Top-level window hosting the ribbon, slide strip, and status bar."""

    def __init__(self, controller: AppController):
        super().__init__()
        self._controller = controller
        self._slide_names: List[str] = []

        self.setWindowTitle("iSlide Clone")
        self.setMinimumSize(1100, 700)
        self.resize(1200, 800)

        self._setup_ribbon()
        self._setup_central()
        self._setup_statusbar()
        self._setup_menu()
        self._wire_signals()

    # ── ribbon ────────────────────────────────────────────────

    def _setup_ribbon(self):
        self._ribbon = RibbonWidget()

        # ── Home tab ──
        home = RibbonTab("Home")
        session_grp = RibbonGroup("Session")
        self._btn_open = session_grp.add_button("Open PPTX File…", self._on_open_file)
        self._btn_connect = session_grp.add_button("Connect to PowerPoint", self._on_connect_ppt)
        session_grp.add_separator()
        self._btn_save = session_grp.add_button("Save", self._on_save)
        self._btn_save.setEnabled(False)
        home.add_group(session_grp)

        info_grp = RibbonGroup("Info")
        self._lbl_mode = info_grp.add_label("Mode: Disconnected")
        self._lbl_file = info_grp.add_label("No file open")
        home.add_group(info_grp)
        self._ribbon.add_tab(home)

        # ── Design tab ──
        design = RibbonTab("Design")
        font_grp = RibbonGroup("Font")
        font_grp.add_label("Title Font:")
        self._combo_title_font = font_grp.add_combo(["Microsoft YaHei", "SimHei", "SimSun", "Arial", "Times New Roman", "Calibri"], self._on_title_font_changed)
        font_grp.add_label("Body Font:")
        self._combo_body_font = font_grp.add_combo(["Microsoft YaHei", "SimHei", "SimSun", "Arial", "Times New Roman", "Calibri"], self._on_body_font_changed)
        self._btn_font_apply_all = font_grp.add_button("Apply to All Slides", lambda: self._on_font_apply("all"))
        self._btn_font_apply_sel = font_grp.add_button("Apply to Selection", lambda: self._on_font_apply("selection"))
        design.add_group(font_grp)

        para_grp = RibbonGroup("Paragraph")
        para_grp.add_label("Line Spacing (pt):")
        self._spin_line_spacing = para_grp.add_spinbox(0.5, 5.0, 1.2, 0.1)
        para_grp.add_label("Before (pt):")
        self._spin_space_before = para_grp.add_spinbox(0, 100, 0, 1)
        para_grp.add_label("After (pt):")
        self._spin_space_after = para_grp.add_spinbox(0, 100, 6, 1)
        self._btn_para_apply_all = para_grp.add_button("Apply to All Slides", lambda: self._on_para_apply("all"))
        self._btn_para_apply_sel = para_grp.add_button("Apply to Selection", lambda: self._on_para_apply("selection"))
        design.add_group(para_grp)

        align_grp = RibbonGroup("Alignment")
        align_grp.add_button("L", lambda: self._on_align("left"))
        align_grp.add_button("C", lambda: self._on_align("center"))
        align_grp.add_button("R", lambda: self._on_align("right"))
        align_grp.add_separator()
        align_grp.add_button("T", lambda: self._on_align("top"))
        align_grp.add_button("M", lambda: self._on_align("middle"))
        align_grp.add_button("B", lambda: self._on_align("bottom"))
        design.add_group(align_grp)

        dist_grp = RibbonGroup("Distribution")
        dist_grp.add_button("H-Distribute", lambda: self._controller.execute_feature("distribute_h"))
        dist_grp.add_button("V-Distribute", lambda: self._controller.execute_feature("distribute_v"))
        design.add_group(dist_grp)

        size_grp = RibbonGroup("Size")
        size_grp.add_button("Same Width", lambda: self._controller.execute_feature("equal_width"))
        size_grp.add_button("Same Height", lambda: self._controller.execute_feature("equal_height"))
        size_grp.add_button("Same Both", lambda: self._controller.execute_feature("equal_both"))
        design.add_group(size_grp)

        layout_grp = RibbonGroup("Layout")
        layout_grp.add_button("Matrix Layout…", self._on_matrix_layout)
        layout_grp.add_button("Circular Layout…", self._on_circular_layout)
        design.add_group(layout_grp)
        self._ribbon.add_tab(design)

        # ── Tools tab ──
        tools = RibbonTab("Tools")
        edit_grp = RibbonGroup("Edit")
        edit_grp.add_button("Paste in Place", lambda: self._controller.execute_feature("paste_in_place"))
        edit_grp.add_button("Swap Positions", lambda: self._controller.execute_feature("swap_positions"))
        tools.add_group(edit_grp)

        color_grp = RibbonGroup("Color")
        color_grp.add_button("Extract Colors", lambda: self._controller.execute_feature("extract_colors"))
        color_grp.add_button("Apply Color Scheme", lambda: self._controller.execute_feature("apply_color_scheme"))
        tools.add_group(color_grp)

        protect_grp = RibbonGroup("Protect")
        protect_grp.add_button("Add Watermark…", self._on_add_watermark)
        protect_grp.add_button("Remove Watermarks", lambda: self._controller.execute_feature("remove_watermark"))
        protect_grp.add_button("Convert to Images", lambda: self._controller.execute_feature("protection_convert"))
        tools.add_group(protect_grp)

        slide_grp = RibbonGroup("Slides")
        slide_grp.add_button("Slide Manager…", self._on_slide_manager)
        tools.add_group(slide_grp)

        tween_grp = RibbonGroup("Tween")
        tween_grp.add_label("Steps:")
        self._spin_tween_steps = tween_grp.add_spinbox(1, 20, 5, 1)
        tween_grp.add_button("Generate Tween", self._on_tween)
        tools.add_group(tween_grp)
        self._ribbon.add_tab(tools)

        # ── Export tab ──
        export = RibbonTab("Export")
        img_grp = RibbonGroup("Image Export")
        img_grp.add_button("Export Slides to Images…", self._on_export_images)
        img_grp.add_button("Create Long Image…", self._on_export_long_image)
        export.add_group(img_grp)

        comp_grp = RibbonGroup("Compression")
        comp_grp.add_button("Compress PPT…", self._on_compress)
        export.add_group(comp_grp)
        self._ribbon.add_tab(export)

        self.setMenuWidget(self._ribbon)

    # ── central area ──────────────────────────────────────────

    def _setup_central(self):
        splitter = QSplitter(Qt.Orientation.Horizontal)

        # Left sidebar — slide strip
        left = QWidget()
        left_layout = QVBoxLayout(left)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.addWidget(QLabel("<b>Slides</b>"))
        self._slide_list = QListWidget()
        self._slide_list.itemSelectionChanged.connect(self._on_slide_selection_changed)
        left_layout.addWidget(self._slide_list)
        splitter.addWidget(left)

        # Right — placeholder
        right = QWidget()
        right_layout = QVBoxLayout(right)
        self._info_label = QLabel(
            "<h3>Welcome to iSlide Clone</h3>"
            "<p>Open a PPTX file or connect to a running PowerPoint instance to get started.</p>"
            "<p><b>Home Tab:</b> Open files or connect to PowerPoint<br>"
            "<b>Design Tab:</b> Fonts, paragraphs, alignment, layout<br>"
            "<b>Tools Tab:</b> Color, paste, swap, watermark, protection, tween<br>"
            "<b>Export Tab:</b> Export images, compress</p>"
        )
        self._info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._info_label.setWordWrap(True)
        right_layout.addWidget(self._info_label)
        splitter.addWidget(right)

        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 3)
        self.setCentralWidget(splitter)

    # ── status bar ────────────────────────────────────────────

    def _setup_statusbar(self):
        self._status_mode = QLabel("Disconnected")
        self._status_file = QLabel("")
        self._status_slides = QLabel("")

        sb = QStatusBar()
        sb.addWidget(self._status_mode)
        sb.addWidget(QLabel("  |  "))
        sb.addWidget(self._status_file)
        sb.addWidget(QLabel("  |  "))
        sb.addWidget(self._status_slides)
        sb.addPermanentWidget(QLabel("iSlide Clone v1.0"))
        self.setStatusBar(sb)

    # ── menu ──────────────────────────────────────────────────

    def _setup_menu(self):
        file_menu = self.menuBar().addMenu("&File")
        file_menu.addAction(QAction("Open PPTX File…", self, triggered=self._on_open_file))
        file_menu.addAction(QAction("Connect to PowerPoint", self, triggered=self._on_connect_ppt))
        file_menu.addSeparator()
        file_menu.addAction(QAction("Save", self, triggered=self._on_save))
        file_menu.addAction(QAction("Save As…", self, triggered=self._on_save_as))
        file_menu.addSeparator()
        file_menu.addAction(QAction("Exit", self, triggered=self.close))

    # ── signal wiring ─────────────────────────────────────────

    def _wire_signals(self):
        self._controller.session_changed.connect(self._on_session_changed)
        self._controller.operation_completed.connect(self._on_operation_completed)

    # ── slots ─────────────────────────────────────────────────

    def _on_session_changed(self, mode: SessionMode, name: str):
        mode_text = "Live PPT" if mode == SessionMode.LIVE_PPT else \
                    "PPTX File" if mode == SessionMode.PPTX_FILE else "Disconnected"
        self._status_mode.setText(f"Mode: {mode_text}")
        self._status_file.setText(f"File: {name}" if name else "")
        self._lbl_mode.setText(f"Mode: {mode_text}")
        self._lbl_file.setText(f"File: {name}" if name else "No file open")
        self._btn_save.setEnabled(mode != SessionMode.DISCONNECTED)

        has_ctx = mode != SessionMode.DISCONNECTED
        if has_ctx:
            ctx = self._controller.context
            self._status_slides.setText(f"Slides: {ctx.slide_count}" if ctx else "")
            self._refresh_slide_list()

    def _on_operation_completed(self, op_name: str, result: EngineResult):
        if result.success:
            self.statusBar().showMessage(f"✓ {result.message}", 5000)
            if self._controller.context:
                self._refresh_slide_list()
                self._status_slides.setText(f"Slides: {self._controller.context.slide_count}")
        else:
            self.statusBar().showMessage(f"✗ {result.message}", 8000)
            QMessageBox.warning(self, "Operation Failed", result.message)

    # ── actions ───────────────────────────────────────────────

    def _on_open_file(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Open PowerPoint File", "",
            "PowerPoint Files (*.pptx *.ppt);;All Files (*)"
        )
        if path:
            self._controller.open_pptx_file(path)

    def _on_connect_ppt(self):
        if not self._controller.connect_to_powerpoint():
            QMessageBox.warning(
                self, "Connection Failed",
                "Could not connect to PowerPoint.\nMake sure PowerPoint is running."
            )

    def _on_save(self):
        if self._controller.context:
            self._controller.context.save()
            self.statusBar().showMessage("✓ Saved", 3000)

    def _on_save_as(self):
        if self._controller.context:
            path, _ = QFileDialog.getSaveFileName(
                self, "Save As", "", "PowerPoint Files (*.pptx);;All Files (*)"
            )
            if path:
                self._controller.context.save_as(path)
                self.statusBar().showMessage(f"✓ Saved as {path}", 5000)

    def _on_title_font_changed(self, font_name: str):
        self._controller._title_font = font_name

    def _on_body_font_changed(self, font_name: str):
        self._controller._body_font = font_name

    def _on_font_apply(self, scope: str):
        title = self._combo_title_font.currentText()
        body = self._combo_body_font.currentText()
        self._controller.execute_feature("uniform_font", title_font=title, body_font=body, target_scope=scope)

    def _on_para_apply(self, scope: str):
        self._controller.execute_feature("uniform_paragraph",
            line_spacing=self._spin_line_spacing.value(),
            space_before=self._spin_space_before.value(),
            space_after=self._spin_space_after.value(),
            target_scope=scope,
        )

    def _on_align(self, direction: str):
        self._controller.execute_feature(f"align_{direction}")

    def _on_matrix_layout(self):
        from src.ui.dialogs.matrix_layout_dialog import MatrixLayoutDialog
        if not self._controller.context:
            self.statusBar().showMessage("No presentation open", 3000)
            return
        dlg = MatrixLayoutDialog(self._controller, self)
        dlg.exec()

    def _on_circular_layout(self):
        from src.ui.dialogs.circular_layout_dialog import CircularLayoutDialog
        if not self._controller.context:
            self.statusBar().showMessage("No presentation open", 3000)
            return
        dlg = CircularLayoutDialog(self._controller, self)
        dlg.exec()

    def _on_export_images(self):
        from src.ui.dialogs.export_dialog import ExportDialog
        if not self._controller.context:
            self.statusBar().showMessage("No presentation open", 3000)
            return
        dlg = ExportDialog(self._controller, self)
        dlg.exec()

    def _on_export_long_image(self):
        from src.ui.dialogs.export_dialog import ExportDialog
        if not self._controller.context:
            self.statusBar().showMessage("No presentation open", 3000)
            return
        dlg = ExportDialog(self._controller, self, long_image_mode=True)
        dlg.exec()

    def _on_compress(self):
        from src.ui.dialogs.compress_dialog import CompressDialog
        if not self._controller.context:
            self.statusBar().showMessage("No presentation open", 3000)
            return
        dlg = CompressDialog(self._controller, self)
        dlg.exec()

    def _on_add_watermark(self):
        from src.ui.dialogs.watermark_dialog import WatermarkDialog
        if not self._controller.context:
            self.statusBar().showMessage("No presentation open", 3000)
            return
        dlg = WatermarkDialog(self._controller, self)
        dlg.exec()

    def _on_slide_manager(self):
        from src.ui.dialogs.slide_sorter_dialog import SlideSorterDialog
        if not self._controller.context:
            self.statusBar().showMessage("No presentation open", 3000)
            return
        dlg = SlideSorterDialog(self._controller, self)
        dlg.exec()

    def _on_tween(self):
        steps = self._spin_tween_steps.value()
        self._controller.execute_feature("shape_tween", steps=steps)

    def _on_slide_selection_changed(self):
        items = self._slide_list.selectedItems()
        indices = [self._slide_list.row(item) for item in items]
        if self._controller.context:
            self._controller.context.set_selected_slides(indices) if hasattr(self._controller.context, 'set_selected_slides') else None

    # ── helpers ───────────────────────────────────────────────

    def _refresh_slide_list(self):
        ctx = self._controller.context
        if not ctx:
            return
        self._slide_list.clear()
        self._slide_names = []
        for proxy in ctx.get_slide_proxies():
            name = proxy.name or f"Slide {proxy.index + 1}"
            self._slide_names.append(name)
            item = QListWidgetItem(f"  {proxy.index + 1}. {name}")
            self._slide_list.addItem(item)

#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import enum
import os
import re
import sys
import time

from pathlib import Path

try:
    from PyQt6.QtGui import QStandardItemModel, QStandardItem
    from PyQt6.QtWidgets import (
        QApplication,
        QMainWindow,
        QDockWidget,
        QToolBar,
        QFileDialog,
        QMessageBox,
        QProgressBar,
    )
    from PyQt6.QtCore import QSettings, Qt, QDir, QDirIterator, QFileInfo, QModelIndex
except ImportError as e:
    try:
        from PyQt5.QtGui import QStandardItemModel, QStandardItem
        from PyQt5.QtWidgets import (
            QApplication,
            QMainWindow,
            QDockWidget,
            QToolBar,
            QFileDialog,
            QMessageBox,
            QProgressBar,
        )
        from PyQt5.QtCore import (
            QSettings,
            Qt,
            QDir,
            QDirIterator,
            QFileInfo,
            QModelIndex,
        )
    except ImportError:
        from PyQt4.QtGui import (
            QApplication,
            QMainWindow,
            QDockWidget,
            QToolBar,
            QStandardItemModel,
            QStandardItem,
            QFileDialog,
            QMessageBox,
            QProgressBar,
        )
        from PyQt4.QtCore import (
            QSettings,
            Qt,
            QDir,
            QDirIterator,
            QFileInfo,
            QModelIndex,
        )

try:
    QSettings_IniFormat = QSettings.Format.IniFormat
    Qt_UserRole = Qt.ItemDataRole.UserRole
except:
    QSettings_IniFormat = QSettings.IniFormat
    Qt_UserRole = Qt.UserRole

from mainwindow_ui import Ui_MainWindow

from common import get_bytes, pretty_file_size, logger
from config import CONFIG_FILE


# TODO: проверка на исключения: должны ловиться в любом месте и показываться в статус баре по кнопке и
# в messagebox'е (как в tx)
# TODO: action expandall and collapseall


def check_filter_size_eval(pattern: str, size_bytes: int) -> bool:
    """Функция выполнит проверку по шаблону pattern и вернет результат: True или False.

    :type pattern: шаблон фильтра размера, например: '{size} >= %1GB% and {size} <= %3GB%'
    :type size_bytes: размер в байтах, который будет подставляться в {size} pattern. Целое число.
    """

    logger.debug("Pattern: %s.", pattern)
    logger.debug("Size: %s bytes.", size_bytes)

    pattern: str = re.sub(
        r"%(.+?)%",
        lambda m: str(get_bytes(m.group(1))),
        pattern,
    )

    source: str = pattern.format(size=size_bytes)
    logger.debug("After replace. Source eval: %s.", source)

    result: bool = eval(source)
    logger.debug("Result eval: %s.", result)

    return result


class ColumnEnum(enum.Enum):
    NAME = 0, "Name"
    SIZE = 1, "Size"

    def __init__(self, value: int, title: str):
        self._value_ = value
        self.title = title


class RowDataEnum(enum.Enum):
    PATH = Qt_UserRole + 1
    SIZE_BYTES = Qt_UserRole + 2
    SIZE_HUMAN = Qt_UserRole + 3


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Все действия к прикрепляемым окнам поместим в меню
        for dock in self.findChildren(QDockWidget):
            self.ui.menuDockWindow.addAction(dock.toggleViewAction())

        # Все действия к toolbar'ам окнам поместим в меню
        for tool in self.findChildren(QToolBar):
            self.ui.menuTools.addAction(tool.toggleViewAction())

        self.ui.action_about_qt.triggered.connect(QApplication.aboutQt)

        self.model = QStandardItemModel()
        self.clear_model()

        self.ui.treeView.setModel(self.model)

        self.ui.treeView.clicked.connect(
            lambda index: (
                self.show_info_in_status_bar(index),
                self.ui.action_show_in_explorer.setEnabled(True),
            )
        )
        self.ui.treeView.doubleClicked.connect(self.show_in_explorer)

        self.ui.button_select_dir.clicked.connect(self.select_dir)
        self.ui.action_go.triggered.connect(self.fill)
        self.ui.action_show_in_explorer.triggered.connect(
            lambda: self.show_in_explorer()
        )
        self.ui.action_apply_filter.triggered.connect(self.slot_remove_dirs)

        self.ui.action_apply_filter.setEnabled(False)
        self.ui.action_show_in_explorer.setEnabled(False)

        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 0)
        self.progress_bar.hide()
        self.ui.statusbar.addPermanentWidget(self.progress_bar)

        self.read_settings()

    def show_in_explorer(self, index: QModelIndex | None = None):
        if index is None:
            index = self.ui.treeView.currentIndex()
            if index is None:
                return

        row = self.get_row_item_from_index(index)
        if row is None:
            return

        item_name, _ = row
        path: str = item_name.data(RowDataEnum.PATH.value)

        os.startfile(path)

    def select_dir(self):
        dir_path: str = QFileDialog.getExistingDirectory(
            parent=self, caption=None, directory=self.ui.line_edit_dir_path.text()
        )
        if dir_path:
            self.ui.line_edit_dir_path.setText(dir_path)

    def get_row_item_from_index(
        self,
        index: QModelIndex | None = None,
    ) -> tuple[QStandardItem, QStandardItem] | None:
        if index is None or not index.isValid:
            logger.warn("get_row_from_index: invalid index: %s.", index)
            return

        row = index.row()

        item = self.model.itemFromIndex(index)
        if item is None:
            return

        parent = item.parent()
        if parent is None:
            parent = self.model.invisibleRootItem()

        return (
            parent.child(row, ColumnEnum.NAME.value),
            parent.child(row, ColumnEnum.SIZE.value),
        )

    def show_info_in_status_bar(self, index: QModelIndex | None = None):
        row = self.get_row_item_from_index(index)
        if row is None:
            return

        item_name, item_size = row

        dir_path: str = item_name.data(RowDataEnum.PATH.value)
        size_bytes: int = item_name.data(RowDataEnum.SIZE_BYTES.value)
        size_human: str = item_name.data(RowDataEnum.SIZE_HUMAN.value)

        self.ui.statusbar.showMessage(f"{dir_path} ({size_human} / {size_bytes} bytes)")

    def clear_model(self):
        self.model.clear()

        header_labels: list[str] = [item.title for item in ColumnEnum]
        self.model.setColumnCount(len(header_labels))
        self.model.setHorizontalHeaderLabels(header_labels)

    def remove_dirs(self, root: QStandardItem):
        """Удаление элементов, у которых размер не совпадает с фильтром"""

        filter_size: str = self.ui.line_edit_filter.text()

        for row in reversed(range(root.rowCount())):
            item_name = root.child(row, ColumnEnum.NAME.value)
            if not check_filter_size_eval(
                pattern=filter_size,
                size_bytes=item_name.data(RowDataEnum.SIZE_BYTES.value),
            ):
                root.removeRow(item_name.row())
            else:
                self.remove_dirs(item_name)

    def slot_remove_dirs(self):
        self.ui.action_apply_filter.setEnabled(False)
        self.remove_dirs(self.model.invisibleRootItem())

    def fill(self):
        self.clear_model()

        dir_path_value: str = self.ui.line_edit_dir_path.text()
        if not dir_path_value:
            QMessageBox.information(self, "Info", "Choose directory path!")
            return

        dir_path: Path = Path(dir_path_value).resolve()
        if not dir_path.exists():
            QMessageBox.information(self, "Info", "Directory not found!")
            return

        filter_size: str = self.ui.line_edit_filter.text()
        if not filter_size:
            logger.debug("filter_size is empty. Setting default filter_size.")
            filter_size = "{size} >= %1GB%"
            logger.debug("filter_size: %s.", filter_size)

        t: float = time.perf_counter()
        try:
            self.ui.label_root_dir.setText(str(dir_path))

            self.ui.action_go.setEnabled(False)
            self.ui.action_show_in_explorer.setEnabled(False)
            self.ui.line_edit_dir_path.setEnabled(False)
            self.ui.line_edit_filter.setEnabled(False)

            self.progress_bar.show()

            # Соберем список папок
            for path in dir_path.iterdir():
                if path.is_dir():
                    self.dir_size_bytes(str(path), self.model.invisibleRootItem(), filter_size)

            self.ui.action_apply_filter.setEnabled(True)

            if self.ui.check_box_auto_apply_filter.isChecked():
                self.slot_remove_dirs()
                self.ui.action_apply_filter.setEnabled(False)
        finally:
            t = time.perf_counter() - t
            logger.debug(f"Done! Elapsed time {t:.2f} sec.")

            self.ui.action_go.setEnabled(True)
            self.ui.line_edit_dir_path.setEnabled(True)
            self.ui.line_edit_filter.setEnabled(True)

            self.progress_bar.hide()

            QMessageBox.information(self, "Info", f"Done!\n\nElapsed time {t:.2f} sec.")

    def dir_size_bytes(
        self,
        dir_path: str,
        root_item: QStandardItem,
        filter_size: str,
        level: int = 0,
    ) -> int:
        path_short_name: str = Path(dir_path).name

        item_name = QStandardItem(path_short_name)
        item_name.setEditable(False)

        item_size = QStandardItem("-")
        item_size.setEditable(False)

        item_name.setData(dir_path, RowDataEnum.PATH.value)
        item_name.setData(-1, RowDataEnum.SIZE_BYTES.value)
        item_name.setData("-1", RowDataEnum.SIZE_HUMAN.value)

        root_item.appendRow([item_name, item_size])

        sizes: int = 0

        # TODO: Брать из dierctory_sizes.py
        try:
            # NOTE: AllEntries = Dirs | Files | Drives
            filters = (
                QDir.Filter.AllEntries
                | QDir.Filter.NoDotAndDotDot
                | QDir.Filter.Hidden
                | QDir.Filter.System
            )
        except:
            filters = QDir.AllEntries | QDir.NoDotAndDotDot | QDir.Hidden | QDir.System

        it = QDirIterator(dir_path, filters)

        while it.hasNext():
            file_name: str = it.next()
            file = QFileInfo(file_name)

            if file.isDir():
                size: int = self.dir_size_bytes(
                    file_name, item_name, filter_size, level + 1
                )
            else:
                size: int = file.size()

            sizes += size

            QApplication.instance().processEvents()

        text_size: str = pretty_file_size(sizes)
        item_size.setText(text_size)

        item_name.setData(sizes, RowDataEnum.SIZE_BYTES.value)
        item_name.setData(text_size, RowDataEnum.SIZE_HUMAN.value)

        return sizes

    def read_settings(self):
        config = QSettings(CONFIG_FILE, QSettings_IniFormat)
        mainwindow_state = config.value("MainWindow_State")
        if mainwindow_state:
            self.restoreState(mainwindow_state)

        mainwindow_geometry = config.value("MainWindow_Geometry")
        if mainwindow_geometry:
            self.restoreGeometry(mainwindow_geometry)

        dir_path = config.value("Dir_path", None)
        if not dir_path:
            dir_path = "C:\\"
        self.ui.line_edit_dir_path.setText(dir_path)

        filter_size = config.value("Filter_size", None)
        if not filter_size:
            filter_size = "{size} >= %1GB%"
        self.ui.line_edit_filter.setText(filter_size)

        self.ui.check_box_auto_apply_filter.setChecked(
            "true" == config.value("Auto_apply_filter", "true").lower()
        )

    def write_settings(self):
        config = QSettings(CONFIG_FILE, QSettings_IniFormat)
        config.setValue("MainWindow_State", self.saveState())
        config.setValue("MainWindow_Geometry", self.saveGeometry())

        config.setValue("Dir_path", self.ui.line_edit_dir_path.text())
        config.setValue("Filter_size", self.ui.line_edit_filter.text())

        config.setValue(
            "Auto_apply_filter",
            "true" if self.ui.check_box_auto_apply_filter.isChecked() else "false",
        )

    def closeEvent(self, event):
        self.write_settings()
        sys.exit()

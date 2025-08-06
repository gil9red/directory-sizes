#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import os
import os.path
import re
import sys
import time

try:
    from PyQt6.QtGui import QStandardItemModel, QStandardItem
    from PyQt6.QtWidgets import (
        QApplication,
        QMainWindow,
        QDockWidget,
        QToolBar,
        QFileDialog,
        QMessageBox,
    )
    from PyQt6.QtCore import QSettings, Qt, QDir, QDirIterator, QFileInfo
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
        )
        from PyQt5.QtCore import QSettings, Qt, QDir, QDirIterator, QFileInfo
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
        )
        from PyQt4.QtCore import QSettings, Qt, QDir, QDirIterator, QFileInfo

try:
    QSettings_IniFormat = QSettings.Format.IniFormat
    Qt_UserRole = Qt.ItemDataRole.UserRole
except:
    QSettings_IniFormat = QSettings.IniFormat
    Qt_UserRole = Qt.UserRole

from mainwindow_ui import Ui_MainWindow

from common import get_bytes, pretty_file_size, logger
from config import CONFIG_FILE


# TODO: enabled show_in_explorer on active item
# TODO: проверка на исключения: должны ловиться в любом месте и показываться в статус баре по кнопке и
# в messagebox'е (как в tx)
# TODO: action expandall and collapseall


def check_filter_size_eval(pattern, size):
    """Функция выполнит проверку по шаблону pattern и вернет результат: True или False.

    :type pattern: шаблон фильтра размера, например: '{size} >= %1GB% and {size} <= %3GB%'
    :type size: размер в байтах, который будет подставляться в {size} pattern. Целое число.
    """

    logger.debug("Pattern: %s.", pattern)
    logger.debug("Size: %s.", size)

    for match in set(re.findall("%.+?%", pattern)):
        byte_size = get_bytes(match[1:-1])
        pattern = pattern.replace(match, str(byte_size))

    source = pattern.format(size=size)
    logger.debug("After replace. Source eval: %s.", source)

    result = eval(source)
    logger.debug("Result eval: %s.", result)

    return result


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

        self.model = QStandardItemModel()
        self.clear_model()

        self.ui.treeView.setModel(self.model)

        self.ui.treeView.clicked.connect(lambda: self.show_info_in_status_bar)
        self.ui.treeView.doubleClicked.connect(lambda: self.show_in_explorer())

        self.ui.button_select_dir.clicked.connect(self.select_dir)
        self.ui.action_go.triggered.connect(self.fill)
        self.ui.action_show_in_explorer.triggered.connect(
            lambda: self.show_in_explorer()
        )
        self.ui.action_apply_filter.triggered.connect(self.slot_remove_dirs)
        self.ui.label_root_dir.setText(self.ui.line_edit_dir_path.text())

        self.ui.action_apply_filter.setEnabled(False)

        self.read_settings()

    def show_in_explorer(self, index=None):
        if index is None:
            index = self.ui.treeView.currentIndex()
            if index is None:
                return

        row = self.get_row_item_from_index(index)
        if row is None:
            return

        path = row[0].data(Qt_UserRole + 1)

        os.startfile(path)

    def select_dir(self):
        dir_path = QFileDialog.getExistingDirectory(
            self, None, self.ui.line_edit_dir_path.text()
        )
        if dir_path:
            self.ui.line_edit_dir_path.setText(dir_path)

    def get_row_item_from_index(self, index):
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

        return [parent.child(row, i) for i in range(self.model.columnCount())]

    def show_info_in_status_bar(self, index):
        row = self.get_row_item_from_index(index)
        if row is None:
            return

        path, size = row

        # TODO: Лучше дать конкретные константные имена, чем так: Qt.UserRole + 1 / Qt.UserRole + 2
        self.ui.statusbar.showMessage(
            f"{path.data(Qt_UserRole + 1)} ({size.data(Qt_UserRole + 1)} / {size.data(Qt_UserRole + 2)} bytes)"
        )

    def clear_model(self):
        self.model.clear()
        header_labels = ["Name", "Size"]
        self.model.setColumnCount(len(header_labels))
        self.model.setHorizontalHeaderLabels(header_labels)

    def remove_dirs(self, root):
        """Удаление элементов, у которых размер не совпадает с фильтром"""

        for row in reversed(range(root.rowCount())):
            child = root.child(row, 1)
            filter_size = self.ui.line_edit_filter.text()
            if not check_filter_size_eval(
                filter_size, get_bytes(child.data(Qt_UserRole + 1))
            ):
                root.removeRow(child.row())
            else:
                self.remove_dirs(root.child(row, 0))

    def slot_remove_dirs(self):
        self.ui.action_apply_filter.setEnabled(False)
        self.remove_dirs(self.model.invisibleRootItem())

    def fill(self):
        self.ui.action_go.setEnabled(False)
        self.clear_model()

        dir_path = self.ui.line_edit_dir_path.text()
        if not dir_path or not os.path.exists(dir_path):
            QMessageBox.information(self, "Info", "Choose dir path!")
            return

        filter_size = self.ui.line_edit_filter.text()
        if not filter_size:
            logger.debug("filter_size is empty. Setting default filter_size.")
            filter_size = "{size} >= %1GB%"
            logger.debug("filter_size: %s.", filter_size)

        t = time.perf_counter()

        # Соберем список папок
        dir_list = [
            os.path.join(dir_path, entry)
            for entry in os.listdir(dir_path)
            if os.path.isdir(os.path.join(dir_path, entry))
        ]

        for entry in dir_list:
            self.dir_size_bytes(entry, self.model.invisibleRootItem(), filter_size)

        self.ui.action_apply_filter.setEnabled(True)

        if self.ui.check_box_auto_apply_filter.isChecked():
            self.slot_remove_dirs()
            self.ui.action_apply_filter.setEnabled(False)

        t = time.perf_counter() - t
        logger.debug("Done! Elapsed time {:.2f} sec.".format(t))

        self.ui.action_go.setEnabled(True)
        QMessageBox.information(
            self, "Info", "Done!\n\nElapsed time {:.2f} sec.".format(t)
        )

    def dir_size_bytes(self, dir_path, root_item, filter_size, level=0):
        dir_path = QDir.toNativeSeparators(dir_path)

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

        sizes = 0

        path_short_name = os.path.split(dir_path)
        path_short_name = (
            path_short_name[1] if path_short_name[1] else path_short_name[0]
        )
        row = [QStandardItem(path_short_name), QStandardItem("-")]

        row[0].setData(dir_path)
        row[1].setText("-")
        row[1].setData("-")

        row[0].setEditable(False)
        row[1].setEditable(False)

        root_item.appendRow(row)

        while it.hasNext():
            file_name = it.next()
            file = QFileInfo(file_name)

            if file.isDir():
                size = self.dir_size_bytes(file_name, row[0], filter_size, level + 1)
            else:
                size = file.size()

            sizes += size

            QApplication.instance().processEvents()

        text_size: str = pretty_file_size(sizes)
        row[1].setText(text_size)
        row[1].setData(text_size)
        row[1].setData(str(sizes), Qt_UserRole + 2)  # TODO: Qt_UserRole в enum?

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

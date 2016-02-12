#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from PySide.QtGui import *
from PySide.QtCore import *

from mainwindow_ui import Ui_MainWindow
from common import *


logger = get_logger('directory_sizes_gui')


import os.path
import sys

import directory_sizes


# def dir_size_bytes(dir_path, root_item, files=0, dirs=0, level=0, do_indent=True, size_less=directory_sizes.get_bytes('1 GB')):
#     it = QDirIterator(dir_path, '*.*', QDir.AllEntries | QDir.NoDotAndDotDot | QDir.Hidden | QDir.System)
#
#     sizes = 0
#
#     row = [QStandardItem(os.path.normpath(dir_path)), QStandardItem('-')]
#
#     while it.hasNext():
#         file_name = it.next()
#         file = QFileInfo(file_name)
#
#         if file.isDir():
#             # row = [QStandardItem(os.path.normpath(file_name)), QStandardItem('-')]
#             # root_item.appendRow(row)
#
#             dirs += 1
#             size, files, dirs = dir_size_bytes(file_name, row[0], files, dirs, level + 1, do_indent, size_less)
#
#             # row[1].setText(dirs_sizes.pretty_file_size(size)[1])
#         else:
#             files += 1
#             size = file.size()
#
#         sizes += size
#
#         qApp.processEvents()
#
#     if sizes >= size_less:
#         root_item.appendRow(row)
#         row[1].setText(directory_sizes.pretty_file_size(sizes)[1])
#
#         # row[1].setText(dirs_sizes.pretty_file_size(sizes)[1])
#         # root_item.appendRow(row)
#
#         logger.debug(
#             ((' ' * 4 * level) if do_indent else '')
#             + os.path.normpath(dir_path) + ' ' + '{1} ({0} bytes)'.format(*directory_sizes.pretty_file_size(sizes))
#         )
#
#     return sizes, files, dirs


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
        header_labels = ['Name', 'Size']
        self.model.setColumnCount(len(header_labels))
        self.model.setHorizontalHeaderLabels(header_labels)

    # # for drive in QDir.drives():
    # #     drive_name = drive.path()
    # #
    # #     if 'C:' in drive_name:
    # #         row = [QStandardItem(drive.path()), QStandardItem(drive.size())]
    # #         model.appendRow(row)
    # #
    # #         sizes, files, dirs = dir_size_bytes(drive_name, row[0])
    # #         row[1].setText(dirs_sizes.pretty_file_size(sizes)[1])

        self.ui.treeView.setModel(self.model)

    def fill(self):
        # sizes, files, dirs = self.dir_size_bytes(r'C:\\', self.model.invisibleRootItem())
        self.dir_size_bytes(r'C:\Program Files (x86)', self.model.invisibleRootItem())
        # self.dir_size_bytes(r'C:\Users\ipetrash\Desktop\PyScripts', self.model.invisibleRootItem(), size_less=directory_sizes.get_bytes('50 MB'))

        QMessageBox.information(self, 'Info', 'Done!')

    def dir_size_bytes(self, dir_path, root_item, files=0, dirs=0, level=0, do_indent=True, size_less=directory_sizes.get_bytes('1 GB')):
        it = QDirIterator(dir_path, '*.*', QDir.AllEntries | QDir.NoDotAndDotDot | QDir.Hidden | QDir.System)

        sizes = 0

        row = [QStandardItem(os.path.normpath(dir_path)), QStandardItem('-')]

        while it.hasNext():
            file_name = it.next()
            file = QFileInfo(file_name)

            if file.isDir():
                # row = [QStandardItem(os.path.normpath(file_name)), QStandardItem('-')]
                # root_item.appendRow(row)

                dirs += 1
                size, files, dirs = self.dir_size_bytes(file_name, row[0], files, dirs, level + 1, do_indent, size_less)

                # row[1].setText(dirs_sizes.pretty_file_size(size)[1])
            else:
                files += 1
                size = file.size()

            sizes += size

            qApp.processEvents()

        if sizes >= size_less:
            root_item.appendRow(row)
            row[1].setText(directory_sizes.pretty_file_size(sizes)[1])

            # row[1].setText(dirs_sizes.pretty_file_size(sizes)[1])
            # root_item.appendRow(row)

            dir_info = os.path.normpath(dir_path) + ' ' + '{1} ({0} bytes)'.format(*directory_sizes.pretty_file_size(sizes))
            logger.debug(
                ((' ' * 4 * level) if do_indent else '') + dir_info
            )

            self.ui.textEdit.append(dir_info)
            # self.ui.treeView.update(row[0].index())
            # self.model.submit()
            # qApp.processEvents()

        return sizes, files, dirs

    def read_settings(self):
        # TODO: при сложных настройках, лучше перейти на json или yaml
        config = QSettings(CONFIG_FILE, QSettings.IniFormat)
        self.restoreState(config.value('MainWindow_State'))
        self.restoreGeometry(config.value('MainWindow_Geometry'))

    def write_settings(self):
        config = QSettings(CONFIG_FILE, QSettings.IniFormat)
        config.setValue('MainWindow_State', self.saveState())
        config.setValue('MainWindow_Geometry', self.saveGeometry())

    def closeEvent(self, event):
        self.write_settings()

        quit()
        # super().closeEvent(*args, **kwargs)

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


# def dir_size_bytes(dir_path, root_item, files=0, dirs=0, level=0, do_indent=True, min_size=directory_sizes.get_bytes('1 GB')):
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
#             size, files, dirs = dir_size_bytes(file_name, row[0], files, dirs, level + 1, do_indent, min_size)
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
#     if sizes >= min_size:
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
        self.clear_model()

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

        # self.ui.treeView.activated.connect(lambda index: self.ui.statusbar.showMessage(self.model.data(index)))
        # self.ui.treeView.clicked.connect(lambda index: self.ui.statusbar.showMessage(self.model.data(index)))
        self.ui.treeView.clicked.connect(self.show_info_in_status_bar)
        # self.ui.treeView.activated.connect(lambda index: self.ui.statusbar.showMessage(str(index)))
        # self.ui.treeView.clicked.connect(lambda index: self.ui.statusbar.showMessage(str(index)))
        #
        # self.ui.statusbar.showMessage('dfdfdf')

        self.ui.button_select_dir.clicked.connect(self.select_dir)
        self.ui.action_go.triggered.connect(self.fill)

        self.ui.label_root_dir.setText(self.ui.line_edit_dir_path.text())

        self.read_settings()

    def select_dir(self):
        dir_path = QFileDialog.getExistingDirectory(self)
        if dir_path:
            self.ui.line_edit_dir_path.setText(dir_path)

    def show_info_in_status_bar(self, index):
        if index is None or not index.isValid:
            logger.warn('show_info_in_status_bar: invalid index: %s.', index)
            return

        row = index.row()

        parent = self.model.itemFromIndex(index).parent()
        if parent is not None:
            path, size = parent.child(row, 0), parent.child(row, 1)
        else:
            path, size = self.model.item(row, 0), self.model.item(row, 1)

        # self.ui.statusbar.showMessage('{} ({})'.format(path.text(), size.text()))
        self.ui.statusbar.showMessage('{} ({})'.format(path.data(Qt.UserRole + 1), size.data(Qt.UserRole + 1)))

    def clear_model(self):
        self.model.clear()
        header_labels = ['Name', 'Size']
        self.model.setColumnCount(len(header_labels))
        self.model.setHorizontalHeaderLabels(header_labels)

    def fill(self):
        self.clear_model()

        dir_path = self.ui.line_edit_dir_path.text()
        if not dir_path or not os.path.exists(dir_path):
            QMessageBox.information(self, 'Info', 'Choose dir path!')
            return

        min_size = self.ui.line_edit_less_min_size.text()
        if not min_size:
            logger.debug('min_size is empty. Setting default min size.')
            min_size = directory_sizes.get_bytes('1 GB')
            logger.debug('min_size: %s.', min_size)
        
        self.dir_size_bytes(dir_path, self.model.invisibleRootItem(), min_size=directory_sizes.get_bytes(min_size))
        
        # # sizes, files, dirs = self.dir_size_bytes(r'C:\\', self.model.invisibleRootItem())
        # self.dir_size_bytes(r'C:\Program Files (x86)\R.G. Mechanics\Lost Planet - Colonies', self.model.invisibleRootItem())
        # # self.dir_size_bytes(r'C:\Users\ipetrash\Desktop\PyScripts', self.model.invisibleRootItem(), min_size=directory_sizes.get_bytes('50 MB'))

        self.ui.treeView.expandAll()
        self.ui.treeView.resizeColumnToContents(0)
        QMessageBox.information(self, 'Info', 'Done!')

    def dir_size_bytes(self, dir_path, root_item, files=0, dirs=0, level=0, do_indent=True, min_size=directory_sizes.get_bytes('1 GB')):
        it = QDirIterator(dir_path, '*.*', QDir.AllEntries | QDir.NoDotAndDotDot | QDir.Hidden | QDir.System)

        sizes = 0

        path_short_name = os.path.split(dir_path)
        path_short_name = path_short_name[1] if path_short_name[1] else path_short_name[0]
        row = [QStandardItem(path_short_name), QStandardItem('-')]

        # row = [QStandardItem(os.path.normpath(dir_path)), QStandardItem('-')]

        while it.hasNext():
            file_name = it.next()
            file = QFileInfo(file_name)

            if file.isDir():
                # row = [QStandardItem(os.path.normpath(file_name)), QStandardItem('-')]
                # root_item.appendRow(row)

                dirs += 1
                size, files, dirs = self.dir_size_bytes(file_name, row[0], files, dirs, level + 1, do_indent, min_size)

                # row[1].setText(dirs_sizes.pretty_file_size(size)[1])
            else:
                files += 1
                size = file.size()

            sizes += size

            qApp.processEvents()

        if sizes >= min_size:
            root_item.appendRow(row)

            text_size = directory_sizes.pretty_file_size(sizes)[1]

            row[0].setData(dir_path)
            row[1].setText(text_size)
            row[1].setData(text_size)

            # row[0].setToolTip(dir_path)
            # row[1].setToolTip(text_size)
            #
            # row[0].setStatusTip(dir_path)
            # row[1].setStatusTip(text_size)

            row[0].setEditable(False)
            row[1].setEditable(False)

            # for item in row:
            #     item.setData(item.text(), Qt.UserRole + 1)

            # row[0].setToolTip(row[0].text())
            # row[1].setToolTip(row[1].text())

            # row[0].setStatusTip(row[0].text())
            # row[1].setStatusTip(row[1].text())

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

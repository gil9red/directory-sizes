#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import os.path

from PySide.QtGui import *
from PySide.QtCore import *

from mainwindow_ui import Ui_MainWindow
from common import *

import directory_sizes


logger = get_logger('directory_sizes_gui')


# TODO: enabled show_in_explorer on active item
# TODO: memory dockwidget settings
# TODO: fill tree during search
# TODO: более сложный поиск:  возможность указать больше, меньше, равно указанному размеру, а также
# диавпазон


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

        self.ui.treeView.clicked.connect(self.show_info_in_status_bar)
        self.ui.treeView.doubleClicked.connect(self.show_in_explorer)

        self.ui.button_select_dir.clicked.connect(self.select_dir)
        self.ui.action_go.triggered.connect(self.fill)
        self.ui.action_show_in_explorer.triggered.connect(self.show_in_explorer)

        self.ui.label_root_dir.setText(self.ui.line_edit_dir_path.text())

        self.read_settings()

    def update_states(self):
        pass

    def show_in_explorer(self, index=None):
        if index is None:
            index = self.ui.treeView.currentIndex()
            if index is None:
                return

        row = self.get_row_item_from_index(index)
        if row is None:
            return

        # TODO: Qt.UserRole + 1
        path = row[0].data(Qt.UserRole + 1)

        cmd = 'Explorer /n,"{}"'.format(path)
        logger.debug('Command: %s.', cmd)

        os.system(cmd)

    def select_dir(self):
        dir_path = QFileDialog.getExistingDirectory(self)
        if dir_path:
            # dir_path = os.path.normpath(dir_path)
            self.ui.line_edit_dir_path.setText(dir_path)

    def get_row_item_from_index(self, index):
        if index is None or not index.isValid:
            logger.warn('get_row_from_index: invalid index: %s.', index)
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

        # TODO: Qt.UserRole + 1
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

        self.ui.treeView.expandAll()
        self.ui.treeView.resizeColumnToContents(0)
        QMessageBox.information(self, 'Info', 'Done!')

    def dir_size_bytes(self, dir_path, root_item, files=0, dirs=0, level=0, do_indent=True, min_size=directory_sizes.get_bytes('1 GB')):
        dir_path = QDir.toNativeSeparators(dir_path)

        it = QDirIterator(dir_path, '*.*', QDir.AllEntries | QDir.NoDotAndDotDot | QDir.Hidden | QDir.System)

        sizes = 0

        path_short_name = os.path.split(dir_path)
        path_short_name = path_short_name[1] if path_short_name[1] else path_short_name[0]
        row = [QStandardItem(path_short_name), QStandardItem('-')]

        while it.hasNext():
            file_name = it.next()
            file = QFileInfo(file_name)

            if file.isDir():
                dirs += 1
                size, files, dirs = self.dir_size_bytes(file_name, row[0], files, dirs, level + 1, do_indent, min_size)
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

            row[0].setEditable(False)
            row[1].setEditable(False)

            dir_info = dir_path + ' ' + '{1} ({0} bytes)'.format(*directory_sizes.pretty_file_size(sizes))
            logger.debug(
                ((' ' * 4 * level) if do_indent else '') + dir_info
            )

            self.ui.textEdit.append(dir_info)

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

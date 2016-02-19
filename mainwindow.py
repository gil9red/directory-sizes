#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import os.path
import re
import time

from PySide.QtGui import *
from PySide.QtCore import *

from mainwindow_ui import Ui_MainWindow
from common import *

import directory_sizes


logger = get_logger('directory_sizes_gui')


# TODO: enabled show_in_explorer on active item
# TODO: fill tree during search
# TODO: проверка на исключения: должны ловиться в любом месте и показываться в статус баре по кнопке и
# в messagebox'е (как в tx)


def check_filter_size_eval(pattern, size):
    """Функция выполнит проверку по шаблону pattern и вернет результат: True или False.

    :type pattern: шаблон фильтра размера, например: '{size} >= %1GB% and {size} <= %3GB%'
    :type size: размер в байтах, который будет подставляться в {size} pattern. Целое число.
    """

    # logger.debug('Pattern: %s.', pattern)
    # logger.debug('Size: %s.', size)

    for match in set(re.findall('%.+?%', pattern)):
        byte_size = directory_sizes.get_bytes(match[1:-1])
        pattern = pattern.replace(match, str(byte_size))

    source = pattern.format(size=size)
    # logger.debug('After replace. Source eval: %s.', source)

    result = eval(source)
    # logger.debug('Result eval: %s.', result)

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
        dir_path = QFileDialog.getExistingDirectory(self, None, self.ui.line_edit_dir_path.text())
        if dir_path:
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

        filter_size = self.ui.line_edit_filter_size.text()
        if not filter_size:
            logger.debug('filter_size is empty. Setting default filter_size.')
            filter_size = "{size} >= %1GB%"
            logger.debug('filter_size: %s.', filter_size)

        t = time.clock()

        # Соберем список папок
        for entry in [os.path.join(dir_path, entry)
                      for entry in os.listdir(dir_path)
                      if os.path.isdir(os.path.join(dir_path, entry))]:
            self.dir_size_bytes(entry, self.model.invisibleRootItem(), filter_size=filter_size)

        # self.dir_size_bytes(dir_path, self.model.invisibleRootItem(), filter_size=filter_size)

        # Удаление элементов, у которых размер не совпадает с фильтром
        root = self.model.invisibleRootItem()
        for row in reversed(range(root.rowCount())):
            child = root.child(row, 1)
            if child.text() in '-':
                root.removeRow(row)
            else:
                self.ui.treeView.setExpanded(child.index(), True)

        t2 = time.clock() - t
        logger.debug('Done! Elapsed time {:.2f} sec.'.format(t2))
        logger.debug('Root rows: %s.', self.model.invisibleRootItem().rowCount())
        # quit()

        # self.ui.treeView.expandAll()
        # self.ui.treeView.resizeColumnToContents(0)

        QMessageBox.information(self, 'Info', 'Done!\n\nElapsed time {:.2f} sec.'.format(t2))

    def dir_size_bytes(self, dir_path, root_item, files=0, dirs=0, level=0,
                       do_indent=True, filter_size="{size} >= %1GB%"):
        dir_path = QDir.toNativeSeparators(dir_path)

        it = QDirIterator(dir_path, '*.*', QDir.AllEntries | QDir.NoDotAndDotDot | QDir.Hidden | QDir.System)

        sizes = 0

        path_short_name = os.path.split(dir_path)
        path_short_name = path_short_name[1] if path_short_name[1] else path_short_name[0]
        row = [QStandardItem(path_short_name), QStandardItem('-')]

        row[0].setData(dir_path)
        row[1].setText('-')
        row[1].setData('-')

        row[0].setEditable(False)
        row[1].setEditable(False)

        root_item.appendRow(row)

        while it.hasNext():
            file_name = it.next()
            file = QFileInfo(file_name)

            if file.isDir():
                dirs += 1
                size, files, dirs = self.dir_size_bytes(file_name, row[0], files, dirs, level + 1,
                                                        do_indent, filter_size)
            else:
                files += 1
                size = file.size()

            sizes += size

            qApp.processEvents()

        if check_filter_size_eval(filter_size, sizes):
            # root_item.appendRow(row)

            text_size = directory_sizes.pretty_file_size(sizes)[1]

            row[1].setText(text_size)
            row[1].setData(text_size)

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

        dir_path = config.value('Dir_path', None)
        if not dir_path:
            dir_path = "C:\\"
        self.ui.line_edit_dir_path.setText(dir_path)

        filter_size = config.value('Filter_size', None)
        if not filter_size:
            filter_size = "{size} >= %1GB%"
        self.ui.line_edit_filter_size.setText(filter_size)

    def write_settings(self):
        config = QSettings(CONFIG_FILE, QSettings.IniFormat)
        config.setValue('MainWindow_State', self.saveState())
        config.setValue('MainWindow_Geometry', self.saveGeometry())

        config.setValue('Dir_path', self.ui.line_edit_dir_path.text())
        config.setValue('Filter_size', self.ui.line_edit_filter_size.text())

    def closeEvent(self, event):
        self.write_settings()
        quit()

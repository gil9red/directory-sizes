#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import os.path
import sys


from PySide.QtGui import *
from PySide.QtCore import *


if __name__ == '__main__':
    app = QApplication(sys.argv)

    from mainwindow import MainWindow
    mw = MainWindow()
    mw.show()

    # mw.fill()

    # model = QStandardItemModel()
    # header_labels = ['Имя', 'Размер']
    # model.setColumnCount(len(header_labels))
    # model.setHorizontalHeaderLabels(header_labels)
    #
    # # sizes, files, dirs = dir_size_bytes(r'C:\\', model.invisibleRootItem())
    # # row[1].setText(dirs_sizes.pretty_file_size(sizes)[1])
    #
    # # for drive in QDir.drives():
    # #     drive_name = drive.path()
    # #
    # #     if 'C:' in drive_name:
    # #         row = [QStandardItem(drive.path()), QStandardItem(drive.size())]
    # #         model.appendRow(row)
    # #
    # #         sizes, files, dirs = dir_size_bytes(drive_name, row[0])
    # #         row[1].setText(dirs_sizes.pretty_file_size(sizes)[1])
    #
    # button = QPushButton()
    # button.show()
    #
    # tree = QTreeView()
    # tree.setModel(model)
    # tree.setAnimated(False)
    # tree.setIndentation(20)
    # # tree.setSortingEnabled(True)
    #
    # tree.setWindowTitle("Dirs Sizes")
    # tree.resize(640, 480)
    # tree.show()
    #
    # sizes, files, dirs = dir_size_bytes(r'C:\\', model.invisibleRootItem())

    sys.exit(app.exec_())

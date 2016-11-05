#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import sys

# from PySide.QtGui import QApplication
from PyQt4.QtGui import QApplication


# TODO: возможность задать несколько путей поиска

if __name__ == '__main__':
    app = QApplication(sys.argv)

    from mainwindow import MainWindow
    mw = MainWindow()
    mw.show()

    sys.exit(app.exec_())

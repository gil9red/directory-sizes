#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import traceback
import sys

from common import logger

try:
    from PyQt6.QtWidgets import QApplication, QMessageBox
except ImportError:
    try:
        from PyQt5.QtWidgets import QApplication, QMessageBox
    except ImportError:
        from PyQt4.QtGui import QApplication, QMessageBox


def log_uncaught_exceptions(ex_cls, ex, tb):
    text = f"{ex_cls.__name__}: {ex}:\n"
    text += "".join(traceback.format_tb(tb))

    logger.error(text)

    if QApplication.instance():
        QMessageBox.critical(None, "Error", text)

    sys.exit()


sys.excepthook = log_uncaught_exceptions

from mainwindow import MainWindow


if __name__ == "__main__":
    app = QApplication([])

    mw = MainWindow()
    mw.show()

    app.exec()

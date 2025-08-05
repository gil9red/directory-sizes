#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import traceback
import sys

try:
    from PyQt5.QtWidgets import QApplication, QMessageBox

except:
    from PyQt4.QtGui import QApplication, QMessageBox


from mainwindow import MainWindow
from mainwindow import logger


def log_uncaught_exceptions(ex_cls, ex, tb):
    text = f"{ex_cls.__name__}: {ex}:\n"
    text += "".join(traceback.format_tb(tb))

    logger.error(text)
    QMessageBox.critical(None, "Error", text)
    sys.exit()


sys.excepthook = log_uncaught_exceptions


if __name__ == "__main__":
    app = QApplication([])

    mw = MainWindow()
    mw.show()

    app.exec_()

#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import traceback
import sys

from PyQt6.QtWidgets import QApplication, QMessageBox

from directory_sizes.common import log


def log_uncaught_exceptions(ex_cls, ex, tb):
    text = f"{ex_cls.__name__}: {ex}:\n"
    text += "".join(traceback.format_tb(tb))

    log.error(text)

    if QApplication.instance():
        QMessageBox.critical(None, "Error", text)

    sys.exit()


sys.excepthook = log_uncaught_exceptions

from directory_sizes.mainwindow import MainWindow  # noqa: E402


def main() -> None:
    app = QApplication([])

    mw = MainWindow()
    mw.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()

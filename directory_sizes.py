#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import os.path
import time


try:
    from PyQt5.QtWidgets import *
    from PyQt5.QtCore import *

except:
    from PyQt4.QtGui import *
    from PyQt4.QtCore import *


from common import get_logger, get_bytes, pretty_file_size


logger = get_logger("dir_sizes", "dir_sizes.log")


def dir_size_bytes(dir_path, files=0, dirs=0, level=0, do_indent=True, size_less=None):
    if size_less is None:
        size_less = get_bytes("1 GB")

    it = QDirIterator(
        dir_path, QDir.AllEntries | QDir.NoDotAndDotDot | QDir.Hidden | QDir.System
    )

    sizes = 0

    while it.hasNext():
        file_name = it.next()
        file = QFileInfo(file_name)

        if file.isDir():
            dirs += 1
            size, files, dirs = dir_size_bytes(
                file_name, files, dirs, level + 1, do_indent, size_less
            )
        else:
            files += 1
            size = file.size()

        sizes += size

    if sizes > size_less:
        logger.debug(
            ((" " * 4 * level) if do_indent else "")
            + f"{os.path.normpath(dir_path)} {sizes} ({pretty_file_size(sizes)} bytes)"
        )

    return sizes, files, dirs


if __name__ == "__main__":
    dir_name = r"C:\\"

    t = time.clock()
    sizes, files, dirs = dir_size_bytes(
        dir_name, do_indent=False, size_less=get_bytes("2GB")
    )

    logger.debug(
        f"\nsizes = {pretty_file_size(sizes)} ({sizes} bytes), "
        f"files = {files}, dirs = {dirs}"
    )
    logger.debug(f"{time.clock() - t:.2f} sec")

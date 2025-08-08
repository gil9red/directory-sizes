#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import os.path
from PyQt6.QtCore import QDir, QDirIterator, QFileInfo
from common import get_logger, get_bytes, pretty_file_size


logger = get_logger("dir_sizes")


def dir_size_bytes(
    dir_path: str,
    files: int = 0,
    dirs: int = 0,
    level: int = 0,
    do_indent: bool = True,
    size_less: int = get_bytes("1 GB"),
) -> tuple[int, int, int]:
    filters = (
        # NOTE: AllEntries = Dirs | Files | Drives
        QDir.Filter.AllEntries
        | QDir.Filter.NoDotAndDotDot
        | QDir.Filter.Hidden
        | QDir.Filter.System
    )

    it = QDirIterator(dir_path, filters)

    total_bytes: int = 0

    while it.hasNext():
        file_name = it.next()

        # TODO: Где-то тут была ошибка
        file = QFileInfo(file_name)

        if file.isDir():
            dirs += 1
            size, files, dirs = dir_size_bytes(
                file_name, files, dirs, level + 1, do_indent, size_less
            )
        else:
            files += 1
            size = file.size()

        total_bytes += size

    if total_bytes > size_less:
        logger.debug(
            ((" " * 4 * level) if do_indent else "")
            + f"{os.path.normpath(dir_path)} {pretty_file_size(total_bytes)} ({total_bytes} bytes)"
        )

    return total_bytes, files, dirs


if __name__ == "__main__":
    import time
    from common import get_default_path

    dir_name: str = get_default_path()

    t = time.perf_counter()
    sizes, files, dirs = dir_size_bytes(
        dir_name, do_indent=False, size_less=get_bytes("2GB")
    )

    logger.debug(
        f"\nsizes = {pretty_file_size(sizes)} ({sizes} bytes), "
        f"files = {files}, dirs = {dirs}"
    )
    logger.debug(f"{time.perf_counter() - t:.2f} sec")

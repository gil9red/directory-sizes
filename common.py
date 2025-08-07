#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import sys
import logging

from logging.handlers import RotatingFileHandler
from pathlib import Path

import config


def get_logger(file_name: str, dir_name: Path = config.DIR / "logs") -> logging.Logger:
    log = logging.getLogger(file_name)
    log.setLevel(logging.DEBUG)

    dir_name = dir_name.resolve()
    dir_name.mkdir(parents=True, exist_ok=True)

    file_name = Path(file_name).resolve()
    file_name = dir_name / (file_name.name + ".log")

    formatter = logging.Formatter(
        "[%(asctime)s] %(filename)s[LINE:%(lineno)d] %(levelname)-8s %(message)s"
    )

    fh = RotatingFileHandler(
        file_name, maxBytes=10_000_000, backupCount=5, encoding="utf-8"
    )
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)
    log.addHandler(fh)

    ch = logging.StreamHandler(stream=sys.stdout)
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(formatter)
    log.addHandler(ch)

    return log


def get_bytes(text: str, units: str = "BKMGTPE") -> int:
    """Возвращает числовое значение в байтах разбирая строки вида: 1 GB, 50 MB и т.п."""

    # Возможно, мы просто получили число как строку, тогда не делаем с ней каких-то действий манипуляций,
    # а только превращаем в число и возвращаем
    try:
        return int(float(text))
    except:
        pass

    text = text.strip().replace(" ", "").replace(",", ".")

    # NOTE: "766.00 B" -> "766.00", "766.5 GB" -> "766.5 G"
    text = text[:-1]
    try:
        # Если ошибок не случится, значит получили байты (предположительно),
        # Это может быть строка: "766.00 B"
        return int(float(text))
    except:
        pass

    # NOTE: For '54.7G' -> num='54.7' and unit='G'
    num = float(text[:-1])
    unit = text[-1:]

    assert (
        unit in units
    ), f"Unknown unit {unit}, possible: {', '.join(tuple(units))}. Text={text}."

    unit_pow = units.find(unit)
    assert (
        unit_pow >= 0
    ), f"Unit pow should > 0, unit_pow={unit_pow} unit={unit}. Text={text}."

    return int(num * (1024**unit_pow))


def pretty_file_size(n_size: int) -> str:
    i = 0
    size = n_size

    while size >= 1024:
        size /= 1024
        i += 1

    return f"{size:.2f} {'BKMGTPE'[i]}{('B' if i > 0 else '')}"


logger = get_logger("directory_sizes_gui")


if __name__ == "__main__":
    for value in ["1 B", "1 KB", "1 MB", "1 GB"]:
        total_bytes = get_bytes(value)
        print(value, total_bytes, pretty_file_size(total_bytes))

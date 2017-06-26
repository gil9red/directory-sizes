#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


CONFIG_FILE = 'config'


import sys
import logging


def get_logger(name, file='log.txt', encoding='utf8'):
    log = logging.getLogger(name)
    log.setLevel(logging.DEBUG)

    formatter = logging.Formatter('[%(asctime)s] %(filename)s[LINE:%(lineno)d] %(levelname)-8s %(message)s')

    fh = logging.FileHandler(file, encoding=encoding)
    fh.setLevel(logging.DEBUG)

    ch = logging.StreamHandler(stream=sys.stdout)
    ch.setLevel(logging.DEBUG)

    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    log.addHandler(fh)
    log.addHandler(ch)

    return log


def get_bytes(text, units='BKMGTPE'):
    """Возвращает числовое значение в байтах разбирая строки вида: 1 GB, 50 MB и т.п."""

    # Возможно, мы просто получили число как строку, тогда не делаем с ней каких-то действий манипуляций,
    # а только превращаем в число и возвращаем
    try:
        return float(text)
    except:
        pass

    text = text.strip().replace(' ', '').replace(',', '.')

    text = text[:-1]
    try:
        # Если ошибок не случится, значит получили байты (предположительно),
        # Это может быть строка: "766.00 B"
        return int(float(text))
    except:
        pass

    # For '54,7GB' -> num='54,7' and unit='G'
    num, unit = float(text[:-1]), text[-1:]

    # assert len(unit) == 1, 'Len unit should == 1, example G, M. Unit = {}. Text={}.'.format(unit, text)
    assert unit in units, 'Unknown unit {}, possible: {}. Text={}.'.format(unit, ', '.join(tuple(units)), text)

    unit_pow = units.find(unit)
    assert unit_pow >= 0, 'Unit pow should > 0, unit_pow={} unit={}. Text={}.'.format(unit_pow, unit, text)

    return int(num * 1024 ** unit_pow)


def pretty_file_size(n_size):
    i = 0
    size = n_size

    while size >= 1024:
        size /= 1024
        i += 1

    return n_size, '{:.2f}'.format(size) + ' ' + "BKMGTPE"[i] + ('B' if i > 0 else ' ')

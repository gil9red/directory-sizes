#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from pathlib import Path


DIR: Path = Path(__file__).resolve().parent

CONFIG_FILE: str = str(DIR / "config.ini")

"""
:project: markji-py
:author: L-ING
:copyright: (C) 2025 L-ING <hlf01@icloud.com>
:license: MIT, see LICENSE for more details.
"""

import os


class Env:
    def __init__(self):
        self.username: str = os.environ["MARKJI_USERNAME"]
        self.password: str = os.environ["MARKJI_PASSWORD"]


ENV = Env()

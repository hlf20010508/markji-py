"""
:project: markji-py
:author: L-ING
:copyright: (C) 2025 L-ING <hlf01@icloud.com>
:license: MIT, see LICENSE for more details.
"""

from enum import Enum


class FontColor(Enum):
    RED = "!d16056"
    ORANGE = "!dc7705"
    YELLOW = "!eb9e27"
    GREEN = "!36b59d"
    BLUE = "!275bd1"
    PURPLE = "!5c2fa6"
    GRAY = "!90959b"


class BackgroundColor(Enum):
    RED = "!!fbc0bc"
    ORANGE = "!!fedcb6"
    YELLOW = "!!fff895"
    GREEN = "!!c5f1c0"
    BLUE = "!!cfdeff"
    PURPLE = "!!dbc9fb"
    GRAY = "!!e5e6ea"


class FontWrapper:
    def __init__(self, content: str):
        self._content = content
        self._bold: bool = False
        self._color: FontColor = None
        self._background: BackgroundColor = None

    def bold(self):
        self._bold = True

    def color(self, color: FontColor):
        self._color = color.value

    def background(self, color: BackgroundColor):
        self._background = color.value

    def build(self) -> str:
        result = "[T#"
        if self._bold:
            result += "B,"
        if self._color:
            result += f"{self._color},"
        if self._background:
            result += f"{self._background},"
        result.rstrip(",")
        result += f"#{self._content}]"

        return result

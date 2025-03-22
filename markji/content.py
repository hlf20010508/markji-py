"""
:project: markji-py
:author: L-ING
:copyright: (C) 2025 L-ING <hlf01@icloud.com>
:license: MIT, see LICENSE for more details.
"""

from enum import Enum


class FontColor(Enum):
    """
    字体颜色
    """

    RED = "!d16056"
    ORANGE = "!dc7705"
    YELLOW = "!eb9e27"
    GREEN = "!36b59d"
    BLUE = "!275bd1"
    PURPLE = "!5c2fa6"
    GRAY = "!90959b"


class BackgroundColor(Enum):
    """
    背景颜色
    """

    RED = "!!fbc0bc"
    ORANGE = "!!fedcb6"
    YELLOW = "!!fff895"
    GREEN = "!!c5f1c0"
    BLUE = "!!cfdeff"
    PURPLE = "!!dbc9fb"
    GRAY = "!!e5e6ea"


class FontWrapper:
    """
    字体包装器

    示例::
        from markji.content import FontWrapper, FontColor, BackgroundColor

        FontWrapper("Hello, World!").bold().color(FontColor.RED).background(
            BackgroundColor.YELLOW
        ).build()
    """

    def __init__(self, content: str):
        """
        初始化

        :param content: 内容
        """
        self._content = content
        self._bold: bool = False
        self._color: FontColor = None
        self._background: BackgroundColor = None

    def bold(self):
        """
        加粗
        """
        self._bold = True

    def color(self, color: FontColor):
        """
        字体颜色

        :param color: 颜色
        """
        self._color = color.value

    def background(self, color: BackgroundColor):
        """
        背景颜色

        :param color: 颜色
        """
        self._background = color.value

    def build(self) -> str:
        """
        构建

        :return: str
        """
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

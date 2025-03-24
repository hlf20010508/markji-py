# :project: markji-py
# :author: L-ING
# :copyright: (C) 2025 L-ING <hlf01@icloud.com>
# :license: MIT, see LICENSE for more details.

from enum import StrEnum


class FontColor(StrEnum):
    """
    字体颜色

    * RED: 红色
    * ORANGE: 橙色
    * YELLOW: 黄色
    * GREEN: 绿色
    * BLUE: 蓝色
    * PURPLE: 紫色
    * GRAY: 灰色
    """

    RED = "!d16056"
    ORANGE = "!dc7705"
    YELLOW = "!eb9e27"
    GREEN = "!36b59d"
    BLUE = "!275bd1"
    PURPLE = "!5c2fa6"
    GRAY = "!90959b"


class FontBackgroundColor(StrEnum):
    """
    背景颜色

    * RED: 红色
    * ORANGE: 橙色
    * YELLOW: 黄色
    * GREEN: 绿色
    * BLUE: 蓝色
    * PURPLE: 紫色
    * GRAY: 灰色
    """

    RED = "!!fbc0bc"
    ORANGE = "!!fedcb6"
    YELLOW = "!!fff895"
    GREEN = "!!c5f1c0"
    BLUE = "!!cfdeff"
    PURPLE = "!!dbc9fb"
    GRAY = "!!e5e6ea"


class FontScript(StrEnum):
    """
    字体角标

    * UP: 上角标
    * DOWN: 下角标
    """

    UP = "up"
    DOWN = "down"


class FontBuilder:
    """
    字体构建器

    :param str content: 内容

    .. code-block:: python

        from markji.editor import FontBuilder, FontColor, FontBackgroundColor, FontScript

        FontBuilder("Hello, World!").bold().color(FontColor.RED).background(
            FontBackgroundColor.YELLOW
        ).script(FontScript.UP).build()
    """

    def __init__(self, content: str):
        """
        字体构建器

        :param str content: 内容
        """
        self._content = content
        self._bold: bool = False
        self._color: FontColor | None = None
        self._background: FontBackgroundColor | None = None
        self._highlight: bool = False
        self._italics: bool = False
        self._underline: bool = False
        self._script: FontScript | None = None

    def bold(self):
        """
        加粗

        :return: 自身
        :rtype: FontBuilder
        """
        self._bold = True
        return self

    def color(self, color: FontColor):
        """
        字体颜色

        此项会被 highlight 覆盖

        :param FontColor color: 颜色
        :return: 自身
        :rtype: FontBuilder
        """
        if not self._highlight:
            self._color = color
        return self

    def background(self, color: FontBackgroundColor):
        """
        背景颜色

        此项会被 highlight 覆盖

        :param FontBackgroundColor color: 颜色
        :return: 自身
        :rtype: FontBuilder
        """
        if not self._highlight:
            self._background = color
        return self

    def highlight(self):
        """
        高亮 黄底绿字

        此项会覆盖 color 和 background

        :return: 自身
        :rtype: FontBuilder
        """
        self._highlight = True
        self._color = FontColor.YELLOW
        self._background = FontBackgroundColor.GREEN
        return self

    def italics(self):
        """
        斜体

        :return: 自身
        :rtype: FontBuilder
        """
        self._italics = True
        return self

    def underline(self):
        """
        下划线

        :return: 自身
        :rtype: FontBuilder
        """
        self._underline = True
        return self

    def script(self, script: FontScript):
        """
        角标

        :param FontScript script: 角标
        :return: 自身
        :rtype: FontBuilder
        """
        self._script = script
        return self

    def build(self) -> str:
        """
        构建

        :return: 包装后的内容
        :rtype: str
        """
        result = []
        if self._bold:
            result.append("B")
        if self._color:
            result.append(self._color.value)
        if self._background:
            result.append(self._background.value)
        if self._italics:
            result.append("I")
        if self._underline:
            result.append("U")
        if self._script:
            result.append(self._script.value)

        result = f"[T#{",".join(result)}#{self._content}]"

        return result

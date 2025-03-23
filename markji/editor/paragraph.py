# :project: markji-py
# :author: L-ING
# :copyright: (C) 2025 L-ING <hlf01@icloud.com>
# :license: MIT, see LICENSE for more details.

from markji.editor.font import FontBuilder
from markji.editor.cloze import ClozeBuilder


class ParagraphBuilder:
    """
    段落构建器

    纯文字段落

    .. code-block:: python

        from markji.editor import ParagraphBuilder

        ParagraphBuilder("Hello, World!").heading().center().build()

    字体段落

    .. code-block:: python

        from markji.editor import FontBuilder, FontColor, FontBackgroundColor, ParagraphBuilder

        font_builder = FontBuilder("Hello, World!").bold().color(FontColor.RED).background(
            FontBackgroundColor.YELLOW
        )

        ParagraphBuilder(font_builder).heading().center().build()

    完形填空段落

    .. code-block:: python

        from markji.editor import ClozeBuilder, ParagraphBuilder

        cloze_builder = ClozeBuilder("Hello, World!")

        ParagraphBuilder(cloze_builder).heading().build()
    """

    def __init__(self, content: str | FontBuilder | ClozeBuilder):
        """
        初始化

        :param str | FontBuilder content: 内容
        """

        self._content = content
        self._heading: bool = False
        self._center: bool = False
        self._list: bool = False

    def heading(self):
        """
        标题一

        :return: 自身
        :rtype: ParagraphBuilder
        """
        self._heading = True
        return self

    def center(self):
        """
        居中

        :return: 自身
        :rtype: ParagraphBuilder
        """
        self._center = True
        return self

    def list(self):
        """
        无序列表

        :return: 自身
        :rtype: ParagraphBuilder
        """
        self._list = True
        return self

    def build(self) -> str:
        """
        构建

        :return: 包装后的内容
        :rtype: str
        """
        if isinstance(self._content, (FontBuilder, ClozeBuilder)):
            content = self._content.build()
        else:
            content = self._content

        result = []
        if self._heading:
            result.append("H1")
        if self._center:
            result.append("center")
        if self._list:
            result.append("L")

        result = f"[P#{",".join(result)}#{content}]"

        return result

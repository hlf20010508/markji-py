# :project: markji-py
# :author: L-ING
# :copyright: (C) 2025 L-ING <hlf01@icloud.com>
# :license: MIT, see LICENSE for more details.

from markji.editor.media import AudioBuilder
from markji.editor.font import FontBuilder
from markji.editor.cloze import ClozeBuilder
from markji.editor.reference import ReferenceBuilder


class ParagraphBuilder:
    """
    段落构建器
    """

    def __init__(
        self,
        content: str | FontBuilder | ClozeBuilder | AudioBuilder | ReferenceBuilder,
    ):
        """
        段落构建器

        :param str | FontBuilder | ClozeBuilder | AudioBuilder | ReferenceBuilder content: 内容

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

            cloze_builder = ClozeBuilder("Hello, World!", 1)

            ParagraphBuilder(cloze_builder).heading().build()

        音频段落

        .. code-block:: python

            from markji.editor import AudioBuilder, ParagraphBuilder

            audio = await client.upload_file("example.mp3")

            ParagraphBuilder(AudioBuilder(audio.id, "example")).heading().build()

        卡片引用段落

        .. code-block:: python

            from markji.editor import ReferenceBuilder, ParagraphBuilder

            cards, _ = await client.search_cards("Internet", self_only=False)

            ParagraphBuilder(ReferenceBuilder("Hello, World!", cards[0])).heading().build()
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
        if isinstance(
            self._content, (FontBuilder, ClozeBuilder, AudioBuilder, ReferenceBuilder)
        ):
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
        result = ",".join(result)

        return f"[P#{result}#{content}]"

# :project: markji-py
# :author: L-ING
# :copyright: (C) 2025 L-ING <hlf01@icloud.com>
# :license: MIT, see LICENSE for more details.

from markji.types import FileID


class ImageBuilder:
    """
    图片构建器
    """

    def __init__(self, file_id: FileID | str):
        """
        图片构建器

        :param FileID | str file_id: 文件ID

        .. code-block:: python

            from markji.editor import ImageBuilder

            image = await client.upload_file("example.jpeg")

            ImageBuilder(image.id).build()

        增加遮罩

        .. code-block:: python

            from markji.editor import ImageBuilder
            from markji.types import MaskItem

            mask_data = [
                MaskItem(0, 0, 128, 128, 1),
                MaskItem(200, 200, 256, 256, 2),
            ]

            mask = await client.set_mask(mask_data)

            image = await client.upload_file("example.jpeg")

            ImageBuilder(image.id).mask(mask.id).build()
        """
        self._file_id = file_id
        self._mask_id: FileID | str | None = None

    def mask(self, mask_id: FileID | str):
        """
        遮罩

        :param FileID | str mask_id: 遮罩ID
        :return: self
        :rtype: ImageBuilder
        """
        self._mask_id = mask_id
        return self

    def build(self) -> str:
        """
        构建

        :return: 包装后的内容
        :rtype: str
        """
        content = [f"ID/{self._file_id}"]
        if self._mask_id:
            content.append(f"MID/{self._mask_id}")
        result = ",".join(content)

        return f"[Pic#{result}#]"


class AudioBuilder:
    """
    音频构建器
    """

    def __init__(self, file_id: FileID | str, content: str | None = None):
        """
        音频构建器

        :param FileID | str file_id: 文件ID
        :param str | None content: 内容

        本地音频

        .. code-block:: python

            from markji.editor import AudioBuilder

            audio = await client.upload_file("example.mp3")

            AudioBuilder(audio.id).build()

        语音生成

        .. code-block:: python

            from markji.editor import AudioBuilder
            from markji.types import LanguageCode

            word = "example"
            audio = await client.tts(word, LanguageCode.EN_US)

            AudioBuilder(audio.id, word).build()
        """
        self._file_id = file_id
        self._content = content

    def build(self) -> str:
        """
        构建

        :return: 包装后的内容
        :rtype: str
        """
        content = self._content if self._content else ""

        return f"[Audio#A,ID/{self._file_id}#{content}]"

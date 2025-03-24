# :project: markji-py
# :author: L-ING
# :copyright: (C) 2025 L-ING <hlf01@icloud.com>
# :license: MIT, see LICENSE for more details.

from markji.types import FileID


class ImageBuilder:
    """
    图片构建器

    :param FileID | str file_id: 文件ID

    .. code-block:: python

        from markji.editor import ImageBuilder

        image = await client.upload_file("example.jpeg")

        ImageBuilder(image.id).build()
    """

    def __init__(self, file_id: FileID | str):
        """
        图片构建器

        :param FileID | str file_id: 文件ID
        """
        self._file_id = file_id

    def build(self) -> str:
        """
        构建

        :return: 包装后的内容
        :rtype: str
        """
        return f"[Pic#ID/{self._file_id}#]"


class AudioBuilder:
    """
    音频构建器

    :param FileID | str file_id: 文件ID
    :param str | None content: 内容

    .. code-block:: python

        from markji.editor import AudioBuilder

        audio = await client.upload_file("example.mp3")

        AudioBuilder(audio.id, "example").build()
    """

    def __init__(self, file_id: FileID | str, content: str | None = None):
        """
        音频构建器

        :param FileID | str file_id: 文件ID
        :param str | None content: 内容
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

        return f"[Audio#ID/{self._file_id}#{content}]"

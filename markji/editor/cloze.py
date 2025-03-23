# :project: markji-py
# :author: L-ING
# :copyright: (C) 2025 L-ING <hlf01@icloud.com>
# :license: MIT, see LICENSE for more details.


class ClozeBuilder:
    """
    完形填空构建器

    .. code-block:: python

        from markji.editor import ClozeBuilder

        ClozeBuilder("Hello, World!").build(1)
    """

    def __init__(self, content: str):
        """
        初始化

        :param str content: 内容
        """

        self._content = content

    def build(self, group: int = 1) -> str:
        """
        构建

        :param int group: 组号
        :return: 包装后的内容
        :rtype: str
        """
        if group < 1 or not isinstance(group, int):
            raise ValueError("完形填空组号必须为大于 0 的整数")

        return f"[F#{group}#{self._content}]"

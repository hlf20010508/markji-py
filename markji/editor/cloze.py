# :project: markji-py
# :author: L-ING
# :copyright: (C) 2025 L-ING <hlf01@icloud.com>
# :license: MIT, see LICENSE for more details.


class ClozeBuilder:
    """
    完形填空构建器

    组号必须为大于 0 的整数

    :param str content: 内容

    .. code-block:: python

        from markji.editor import ClozeBuilder

        ClozeBuilder("Hello, World!", 1).build()
    """

    def __init__(self, content: str, group: int = 1):
        """
        完形填空构建器

        组号必须为大于 0 的整数

        :param str content: 内容
        :param int group: 组号
        """
        if group < 1 or not isinstance(group, int):
            raise ValueError("完形填空组号必须为大于 0 的整数")

        self._content = content
        self._group = group

    def build(self) -> str:
        """
        构建

        :return: 包装后的内容
        :rtype: str
        """
        return f"[F#{self._group}#{self._content}]"

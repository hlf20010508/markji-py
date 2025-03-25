# :project: markji-py
# :author: L-ING
# :copyright: (C) 2025 L-ING <hlf01@icloud.com>
# :license: MIT, see LICENSE for more details.


class FormulaBuilder:
    """
    公式构建器
    """

    def __init__(self, content: str):
        """
        公式构建器

        使用LaTex语法构建公式

        :param str content: 内容

        .. code-block:: python

            from markji.editor import FormulaBuilder

            FormulaBuilder("E=mc^{2}").build()
        """

        self._content = content

    def build(self) -> str:
        """
        构建

        :return: 包装后的内容
        :rtype: str
        """

        return f"[E##{self._content}]"

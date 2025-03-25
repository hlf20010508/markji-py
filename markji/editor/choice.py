# :project: markji-py
# :author: L-ING
# :copyright: (C) 2025 L-ING <hlf01@icloud.com>
# :license: MIT, see LICENSE for more details.

from typing import Sequence


class ChoiceItem:
    """
    选择题选项
    """

    def __init__(self, content: str, chosen: bool):
        """
        选择题选项

        必须另起一行

        :param str content: 内容
        :param bool chosen: 是否选取
        """
        self._content = content
        self._chosen = chosen

    def __str__(self) -> str:
        if self._chosen:
            result = "*"
        else:
            result = "-"

        return f"{result} {self._content}"


class ChoiceBuilder:
    """
    选择题构建器
    """

    def __init__(self, choices: Sequence[ChoiceItem]):
        """
        选择题构建器

        :param Sequence[ChoiceItem] choices: 选项

        .. code-block:: python

            from markji.editor import ChoiceBuilder, ChoiceItem

            choices = [
                ChoiceItem("dog", True),
                ChoiceItem("cat", True),
                ChoiceItem("horse", False),
                ChoiceItem("bird", False),
            ]

            ChoiceBuilder(choices).build()
        """

        self._choices = choices
        self._multiple = self._check_multiple()
        self._fixed = False

    def _check_multiple(self) -> bool:
        chosen_count = 0
        for choice in self._choices:
            if choice._chosen:
                chosen_count += 1

        if chosen_count > 1:
            return True
        elif chosen_count == 1:
            return False

        raise ValueError("选择题至少需要一个选项")

    def multiple(self):
        """
        多选

        当选项列表中有多个选项被选中时，自动切换为多选，不需要调用此方法

        此方法仅用于将单选题显示为多选题

        :return: 自身
        :rtype: ChoiceBuilder
        """
        self._multiple = True
        return self

    def fixed(self):
        """
        固定

        :return: 自身
        :rtype: ChoiceBuilder
        """
        self._fixed = True
        return self

    def build(self) -> str:
        """
        构建

        :return: 包装后的内容
        :rtype: str
        """
        choices = "\n".join([str(c) for c in self._choices])

        setting = []
        if self._multiple:
            setting.append("multi")
        if self._fixed:
            setting.append("fixed")
        setting = ",".join(setting)

        return f"[Choice#{setting}#\n{choices}\n]"

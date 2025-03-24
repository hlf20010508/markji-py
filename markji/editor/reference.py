# :project: markji-py
# :author: L-ING
# :copyright: (C) 2025 L-ING <hlf01@icloud.com>
# :license: MIT, see LICENSE for more details.

from markji.types import CardRootID
from markji.types.card import Card, CardResult


class ReferenceBuilder:
    """
    卡片引用构建器

    :param str content: 内容
    :param CardResult | Card | CardRootID | str | None card: 被引用的卡片

    .. code-block:: python

        from markji.editor import ReferenceBuilder

        cards, _ = await client.search_cards("Internet", self_only=False)

        ReferenceBuilder("Hello, World!", cards[0]).build()
    """

    def __init__(
        self, content: str, card: CardResult | Card | CardRootID | str | None = None
    ):
        """
        卡片引用构建器

        :param str content: 内容
        :param CardResult | Card | CardRootID | str | None card: 被引用的卡片
        """
        self._content = content
        self._card = card

    def build(self) -> str:
        """
        构建

        :return: 包装后的内容
        :rtype: str
        """
        card_root_id = ""
        if isinstance(self._card, (CardResult, Card)):
            card_root_id = self._card.root_id
        elif isinstance(self._card, str):
            card_root_id = self._card

        result = f"ID/{card_root_id}" if card_root_id else ""

        return f"[Card#{result}#{self._content}]"

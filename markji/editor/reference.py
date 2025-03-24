# :project: markji-py
# :author: L-ING
# :copyright: (C) 2025 L-ING <hlf01@icloud.com>
# :license: MIT, see LICENSE for more details.

from markji import Card
from markji.types import CardRootID


class ReferenceBuilder:
    def __init__(self, content: str, card: Card | CardRootID | str | None = None):
        self._content = content
        self._card = card

    def build(self) -> str:
        card_root_id = ""
        if isinstance(self._card, Card):
            card_root_id = self._card.root_id
        elif isinstance(self._card, str):
            card_root_id = self._card

        result = f"ID/{card_root_id}" if card_root_id else ""

        return f"[Card{result}#{self._content}]"

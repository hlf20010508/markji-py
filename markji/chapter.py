"""
:project: markji-py
:author: L-ING
:copyright: (C) 2025 L-ING <hlf01@icloud.com>
:license: MIT, see LICENSE for more details.
"""

from dataclasses import dataclass
from markji.card import Card

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from markji.deck import Deck


@dataclass
class Chapter:
    """
    Chapter 章节

    :param id: 章节 ID
    :param name: 章节名
    """

    id: str
    name: str
    _cards: dict[str, "Card"]
    _deck: "Deck"

    @property
    def card_count(self):
        """
        卡片数量

        :return: int
        """
        return len(self._cards)

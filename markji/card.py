"""
:project: markji-py
:author: L-ING
:copyright: (C) 2025 L-ING <hlf01@icloud.com>
:license: MIT, see LICENSE for more details.
"""

from dataclasses import dataclass

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from markji.chapter import Chapter


@dataclass
class Card:
    """
    Card 卡片

    :param id: 卡片 ID
    :param content: 卡片内容
    :param root_id: 卡片根 ID
    :param grammar_version: 语法版本
    """

    id: str
    content: str
    root_id: str
    grammar_version: int
    _chapter: "Chapter"

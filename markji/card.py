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
    id: str
    content: str
    root_id: str
    grammar_version: int
    _chapter: "Chapter"

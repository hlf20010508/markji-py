"""
:project: markji-py
:author: L-ING
:copyright: (C) 2025 L-ING <hlf01@icloud.com>
:license: MIT, see LICENSE for more details.
"""

from dataclasses import dataclass
from dataclasses_json import DataClassJsonMixin
from typing import Sequence
from markji.types import Datetime, CardID, ChapterID, ChapterSetID, DeckID, UserID


@dataclass
class Chapter(DataClassJsonMixin):
    """
    Chapter 章节

    :param ChapterID id: 章节ID
    :param DeckID deck_id: 卡组ID
    :param str name: 名称
    :param UserID creator: 创建者
    :param int revision: 修订版本
    :param Sequence[CardID] card_ids: 卡片ID列表
    :param bool is_modified: 是否修改
    :param Datetime created_time: 创建时间
    :param Datetime updated_time: 更新时间
    """

    id: ChapterID
    deck_id: DeckID
    name: str
    creator: UserID
    revision: int
    card_ids: Sequence[CardID]
    is_modified: bool
    created_time: Datetime = Datetime._field()
    updated_time: Datetime = Datetime._field()


@dataclass
class ChapterSet(DataClassJsonMixin):
    """
    章节集合

    :param ChapterSetID id: 章节集合ID
    :param DeckID deck_id: 卡组ID
    :param int revision: 修订版本
    :param Sequence[ChapterID] chapter_ids: 章节ID列表
    :param bool is_modified: 是否修改
    :param Datetime created_time: 创建时间
    :param Datetime updated_time: 更新时间
    """

    id: ChapterSetID
    deck_id: DeckID
    revision: int
    chapter_ids: Sequence[ChapterID]
    is_modified: bool
    created_time: Datetime = Datetime._field()
    updated_time: Datetime = Datetime._field()

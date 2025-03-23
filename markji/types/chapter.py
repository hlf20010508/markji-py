"""
:project: markji-py
:author: L-ING
:copyright: (C) 2025 L-ING <hlf01@icloud.com>
:license: MIT, see LICENSE for more details.
"""

from dataclasses import dataclass
from dataclasses_json import DataClassJsonMixin
from typing import Sequence
from markji.types import _Datetime, CardID, ChapterID, ChapterSetID, DeckID, UserID


@dataclass
class Chapter(DataClassJsonMixin):
    """
    Chapter 章节

    :param id: 章节 ID
    :param deck_id: 卡组 ID
    :param name: 章节名称
    :param creator: 创建者 ID
    :param revision: 修订版本
    :param card_ids: 卡片 ID 列表
    :param is_modified: 是否已修改
    :param created_time: 创建时间
    :param updated_time: 更新时间
    """

    id: ChapterID
    deck_id: DeckID
    name: str
    creator: UserID
    revision: int
    card_ids: Sequence[CardID]
    is_modified: bool
    created_time: _Datetime = _Datetime._field()
    updated_time: _Datetime = _Datetime._field()


@dataclass
class ChapterSet(DataClassJsonMixin):
    """
    章节集合

    :param id: 章节集合ID
    :param deck_id: 卡组ID
    :param revision: 修订版本
    :param chapter_ids: 章节ID列表
    :param is_modified: 是否修改
    :param created_time: 创建时间
    :param updated_time: 更新时间
    """

    id: ChapterSetID
    deck_id: DeckID
    revision: int
    chapter_ids: Sequence[ChapterID]
    is_modified: bool
    created_time: _Datetime = _Datetime._field()
    updated_time: _Datetime = _Datetime._field()

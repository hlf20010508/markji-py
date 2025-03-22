"""
:project: markji-py
:author: L-ING
:copyright: (C) 2025 L-ING <hlf01@icloud.com>
:license: MIT, see LICENSE for more details.
"""

from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from typing import Sequence, Type, cast
from markji.types import CardID, ChapterID, ChapterSetID, DeckID, UserID


@dataclass
class Chapter:
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
    created_time: datetime
    updated_time: datetime

    @classmethod
    def _from_json(cls: Type[Chapter], data: dict) -> Chapter:
        id = cast(ChapterID, data.get("id"))
        deck_id = cast(DeckID, data.get("deck_id"))
        name = cast(str, data.get("name"))
        creator = cast(UserID, data.get("creator"))
        revision = cast(int, data.get("revision"))
        card_ids = cast(Sequence[CardID], data.get("card_ids"))
        is_modified = cast(bool, data.get("is_modified"))
        created_time = datetime.fromisoformat(cast(str, data.get("created_time")))
        updated_time = datetime.fromisoformat(cast(str, data.get("updated_time")))

        return cls(
            id=id,
            deck_id=deck_id,
            name=name,
            creator=creator,
            revision=revision,
            card_ids=card_ids,
            is_modified=is_modified,
            created_time=created_time,
            updated_time=updated_time,
        )


@dataclass
class ChapterSet:
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
    created_time: datetime
    updated_time: datetime

    @classmethod
    def _from_json(cls: Type[ChapterSet], data: dict) -> ChapterSet:
        if data is None:
            return None

        id = cast(ChapterSetID, data.get("id"))
        deck_id = cast(DeckID, data.get("deck_id"))
        revision = cast(int, data.get("revision"))
        chapter_ids = cast(Sequence[ChapterID], data.get("chapter_ids"))
        is_modified = cast(bool, data.get("is_modified"))
        created_time = datetime.fromisoformat(cast(str, data.get("created_time")))
        updated_time = datetime.fromisoformat(cast(str, data.get("updated_time")))

        return cls(
            id=id,
            deck_id=deck_id,
            revision=revision,
            chapter_ids=chapter_ids,
            is_modified=is_modified,
            created_time=created_time,
            updated_time=updated_time,
        )

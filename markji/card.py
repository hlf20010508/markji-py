"""
:project: markji-py
:author: L-ING
:copyright: (C) 2025 L-ING <hlf01@icloud.com>
:license: MIT, see LICENSE for more details.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Type, TypeVar, cast
from markji.types import CardID, CardRootID, DeckID, DeckSource, File, Status, UserID

A = TypeVar("A", bound="Card")


@dataclass
class Card:
    """
    Card 卡片

    :param id: 卡片 ID
    :param content: 内容
    :param content_type: 内容类型
    :param status: 状态
    :param creator: 创建者 ID
    :param deck_id: 卡组 ID
    :param root_id: 根 ID
    :param files: 文件列表
    :param is_modified: 是否已修改
    :param revision: 修订版本
    :param grammar_version: 语法版本
    :param source: 来源
    :param created_time: 创建时间
    :param updated_time: 更新时间
    :param card_rids: 卡片根 ID 列表
    """

    id: CardID
    content: str
    content_type: int
    status: Status
    creator: UserID
    deck_id: DeckID
    root_id: CardRootID
    files: List[File]
    is_modified: bool
    revision: int
    grammar_version: int
    source: DeckSource
    created_time: datetime
    updated_time: datetime
    card_rids: List[CardRootID]

    @classmethod
    def _from_json(cls: Type[A], data: Dict) -> A:
        id = cast(CardID, data.get("id"))
        content = cast(str, data.get("content"))
        content_type = cast(int, data.get("content_type"))
        status = Status(data.get("status"))
        creator = cast(UserID, data.get("creator"))
        deck_id = cast(DeckID, data.get("deck_id"))
        root_id = cast(CardRootID, data.get("root_id"))
        files = [
            cast(File, File._from_json(file)) for file in cast(List, data.get("files"))
        ]
        is_modified = cast(bool, data.get("is_modified"))
        revision = cast(int, data.get("revision"))
        grammar_version = cast(int, data.get("grammar_version"))
        source = DeckSource(data.get("source"))
        created_time = datetime.fromisoformat(cast(str, data.get("created_time")))
        updated_time = datetime.fromisoformat(cast(str, data.get("updated_time")))
        card_rids = cast(List[CardRootID], data.get("card_rids"))

        return cls(
            id=id,
            content=content,
            content_type=content_type,
            status=status,
            creator=creator,
            deck_id=deck_id,
            root_id=root_id,
            files=files,
            is_modified=is_modified,
            revision=revision,
            grammar_version=grammar_version,
            source=source,
            created_time=created_time,
            updated_time=updated_time,
            card_rids=card_rids,
        )

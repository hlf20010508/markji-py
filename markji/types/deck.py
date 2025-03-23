"""
:project: markji-py
:author: L-ING
:copyright: (C) 2025 L-ING <hlf01@icloud.com>
:license: MIT, see LICENSE for more details.
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Sequence, Type, cast
from markji.types import (
    _Datetime,
    DeckAccessSetting,
    UserBrief,
    UserID,
    DeckID,
    Status,
    DeckSource,
)


@dataclass
class Deck:
    """
    Deck 卡组

    :param id: 卡组ID
    :param source: 卡组来源
    :param creator: 创建者ID
    :param status: 卡组状态
    :param name: 卡组名称
    :param authors: 卡组作者
    :param description: 卡组描述
    :param is_modified: 是否修改过
    :param is_private: 是否私有
    :param is_searchable: 是否可搜索
    :param is_semantic_learning: 是否语义学习
    :param like_count: 点赞数
    :param revision: 版本号
    :param card_count: 卡片数
    :param card_price: 卡片价格
    :param chapter_count: 章节数
    :param created_time: 创建时间
    :param updated_time: 更新时间
    :param tags: 标签
    :param is_anki: 是否从 Anki 导入
    :param root_creator: 根创建者
    :param access_setting: 访问设置
    """

    id: DeckID
    source: DeckSource
    creator: UserID
    status: Status
    name: str
    authors: Sequence[UserID]
    description: str
    is_modified: bool
    is_private: bool
    is_searchable: bool
    is_semantic_learning: bool
    like_count: int
    revision: int
    card_count: int
    card_price: int
    chapter_count: int
    created_time: _Datetime
    updated_time: _Datetime
    tags: Sequence
    is_anki: bool | None
    root_creator: UserBrief | None
    access_setting: DeckAccessSetting | None

    @classmethod
    def _from_json(cls: Type[Deck], data: dict) -> Deck:
        """
        从 JSON 数据创建 Deck 对象

        :param data: JSON 数据
        :return: Deck 对象
        """
        id = cast(DeckID, data.get("id"))
        source = DeckSource(data.get("source"))
        creator = cast(UserID, data.get("creator"))
        status = Status(data.get("status"))
        name = cast(str, data.get("name"))
        authors = [author for author in cast(Sequence[UserID], data.get("authors"))]
        description = cast(str, data.get("description"))
        is_modified = cast(bool, data.get("is_modified"))
        is_private = cast(bool, data.get("is_private"))
        is_searchable = cast(bool, data.get("is_searchable"))
        is_semantic_learning = cast(bool, data.get("is_semantic_learning"))
        like_count = cast(int, data.get("like_count"))
        revision = cast(int, data.get("revision"))
        card_count = cast(int, data.get("card_count"))
        card_price = cast(int, data.get("card_price"))
        chapter_count = cast(int, data.get("chapter_count"))
        created_time = _Datetime.fromisoformat(cast(str, data.get("created_time")))
        updated_time = _Datetime.fromisoformat(cast(str, data.get("updated_time")))
        tags = cast(Sequence, data.get("tags"))
        is_anki = cast(bool | None, data.get("is_anki"))
        root_creator = UserBrief._from_json(cast(dict, data.get("root_creator")))
        access_setting = DeckAccessSetting._from_json(
            cast(dict, data.get("access_setting"))
        )

        return cls(
            id=id,
            source=source,
            creator=creator,
            status=status,
            name=name,
            authors=authors,
            description=description,
            is_modified=is_modified,
            is_private=is_private,
            is_searchable=is_searchable,
            is_semantic_learning=is_semantic_learning,
            like_count=like_count,
            revision=revision,
            card_count=card_count,
            card_price=card_price,
            chapter_count=chapter_count,
            created_time=created_time,
            updated_time=updated_time,
            tags=tags,
            is_anki=is_anki,
            root_creator=root_creator,
            access_setting=access_setting,
        )

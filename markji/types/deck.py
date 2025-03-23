"""
:project: markji-py
:author: L-ING
:copyright: (C) 2025 L-ING <hlf01@icloud.com>
:license: MIT, see LICENSE for more details.
"""

from dataclasses import dataclass
from dataclasses_json import DataClassJsonMixin
from typing import Sequence
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
class Deck(DataClassJsonMixin):
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
    tags: Sequence
    created_time: _Datetime = _Datetime._field()
    updated_time: _Datetime = _Datetime._field()
    is_anki: bool | None = None
    root_creator: UserBrief | None = None
    access_setting: DeckAccessSetting | None = None

# :project: markji-py
# :author: L-ING
# :copyright: (C) 2025 L-ING <hlf01@icloud.com>
# :license: MIT, see LICENSE for more details.

from dataclasses import dataclass
from dataclasses_json import DataClassJsonMixin
from typing import Sequence
from markji.types import (
    Datetime,
    DeckAccessSetting,
    UserID,
    DeckID,
    Status,
    DeckSource,
)
from markji.types.user import UserBasic


@dataclass
class Deck(DataClassJsonMixin):
    """
    Deck 卡组

    :param DeckID id: 卡组ID
    :param DeckSource source: 卡组来源
    :param UserID creator: 创建者ID
    :param Status status: 状态
    :param str name: 名称
    :param Sequence[UserID] authors: 作者ID列表
    :param str description: 描述
    :param bool is_modified: 是否已修改
    :param bool is_private: 是否私有
    :param bool is_searchable: 是否可搜索
    :param bool is_semantic_learning: 是否语义学习
    :param int like_count: 点赞数
    :param int revision: 版本
    :param int card_count: 卡片数
    :param int card_price: 卡片价格
    :param int chapter_count: 章节数
    :param Sequence tags: 标签
    :param Datetime created_time: 创建时间
    :param Datetime updated_time: 更新时间
    :param bool is_anki: 是否从Anki导入
    :param UserBasic root_creator: 根创建者
    :param DeckAccessSetting access_setting: 访问设置
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
    created_time: Datetime = Datetime._field()
    updated_time: Datetime = Datetime._field()
    is_anki: bool | None = None
    root_creator: UserBasic | None = None
    access_setting: DeckAccessSetting | None = None

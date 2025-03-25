# :project: markji-py
# :author: L-ING
# :copyright: (C) 2025 L-ING <hlf01@icloud.com>
# :license: MIT, see LICENSE for more details.

from dataclasses import dataclass, field
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
class DeckBasic(DataClassJsonMixin):
    """
    卡组基本信息

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
    :param int like_count: 点赞数
    :param int revision: 版本
    :param int card_count: 卡片数
    :param int chapter_count: 章节数
    :param Datetime created_time: 创建时间
    :param Datetime updated_time: 更新时间
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
    like_count: int
    revision: int
    card_count: int
    chapter_count: int
    created_time: Datetime = field(metadata=Datetime._metadata())
    updated_time: Datetime = field(metadata=Datetime._metadata())


@dataclass
class DeckBrief(DeckBasic):
    """
    卡组简要信息

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
    :param int like_count: 点赞数
    :param int revision: 版本
    :param int card_count: 卡片数
    :param int chapter_count: 章节数
    :param Datetime created_time: 创建时间
    :param Datetime updated_time: 更新时间
    :param UserBasic root_creator: 根创建者
    """

    root_creator: UserBasic


@dataclass
class DeckInfo(DeckBasic):
    """
    卡组信息

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
    :param int like_count: 点赞数
    :param int revision: 版本
    :param int card_count: 卡片数
    :param int chapter_count: 章节数
    :param Datetime created_time: 创建时间
    :param Datetime updated_time: 更新时间
    :param bool is_semantic_learning: 是否语义学习
    :param int card_price: 卡片价格
    :param Sequence tags: 标签
    """

    is_semantic_learning: bool
    card_price: int
    tags: Sequence


@dataclass
class DeckForked(DeckBasic):
    """
    收藏卡组信息

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
    :param int like_count: 点赞数
    :param int revision: 版本
    :param int card_count: 卡片数
    :param int chapter_count: 章节数
    :param Datetime created_time: 创建时间
    :param Datetime updated_time: 更新时间
    :param int card_price: 卡片价格
    :param bool is_semantic_learning: 是否语义学习
    :param DeckID parent_id: 父卡组ID
    """

    card_price: int
    is_semantic_learning: bool
    parent_id: DeckID


@dataclass
class Deck(DeckBrief, DeckInfo):
    """
    卡组

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

    is_anki: bool
    access_setting: DeckAccessSetting

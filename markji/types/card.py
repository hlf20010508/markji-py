# :project: markji-py
# :author: L-ING
# :copyright: (C) 2025 L-ING <hlf01@icloud.com>
# :license: MIT, see LICENSE for more details.

from dataclasses import dataclass, field
from dataclasses_json import DataClassJsonMixin
from markji.types import (
    CardReference,
    Datetime,
    CardID,
    CardRootID,
    DeckID,
    DeckSource,
    File,
    Status,
    UserID,
)
from markji.types.deck import DeckBasic


@dataclass
class CardBase(DataClassJsonMixin):
    """
    基本卡片

    :param CardID id: 卡片 ID
    :param str content: 内容
    :param int content_type: 内容类型
    :param Status status: 状态
    :param UserID creator: 创建者
    :param DeckID deck_id: 所属卡组 ID
    :param CardRootID root_id: 卡片根 ID
    :param list[File] files: 文件列表
    :param bool is_modified: 是否修改
    :param int revision: 修订版本
    :param int grammar_version: 语法版本
    :param DeckSource source: 来源
    :param Datetime created_time: 创建时间
    :param Datetime updated_time: 更新时间
    """

    id: CardID
    content: str
    content_type: int
    status: Status
    creator: UserID
    deck_id: DeckID
    root_id: CardRootID
    files: list[File]
    is_modified: bool
    revision: int
    grammar_version: int
    source: DeckSource
    created_time: Datetime = field(metadata=Datetime._metadata())
    updated_time: Datetime = field(metadata=Datetime._metadata())


@dataclass
class Card(CardBase):
    """
    卡片

    :param CardID id: 卡片 ID
    :param str content: 内容
    :param int content_type: 内容类型
    :param Status status: 状态
    :param UserID creator: 创建者
    :param DeckID deck_id: 所属卡组 ID
    :param CardRootID root_id: 卡片根 ID
    :param list[File] files: 文件列表
    :param bool is_modified: 是否修改
    :param int revision: 修订版本
    :param int grammar_version: 语法版本
    :param DeckSource source: 来源
    :param list[CardRootID] card_rids: 卡片根 ID 列表
    :param Datetime created_time: 创建时间
    :param Datetime updated_time: 更新时间
    """

    card_rids: list[CardRootID]


@dataclass
class CardResult(CardBase):
    """
    卡片搜索结果

    :param CardID id: 卡片 ID
    :param str content: 内容
    :param int content_type: 内容类型
    :param Status status: 状态
    :param UserID creator: 创建者
    :param DeckID deck_id: 所属卡组 ID
    :param CardRootID root_id: 卡片根 ID
    :param list[File] files: 文件列表
    :param list[CardReference] references: 引用列表
    :param bool is_modified: 是否修改
    :param int revision: 修订版本
    :param int grammar_version: 语法版本
    :param DeckSource source: 来源
    :param Datetime created_time: 创建时间
    :param Datetime updated_time: 更新时间
    :param DeckBasic deck: 所属卡组基本信息
    """

    references: list[CardReference]
    deck: DeckBasic

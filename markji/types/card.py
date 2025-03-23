# :project: markji-py
# :author: L-ING
# :copyright: (C) 2025 L-ING <hlf01@icloud.com>
# :license: MIT, see LICENSE for more details.

from dataclasses import dataclass
from dataclasses_json import DataClassJsonMixin
from typing import Sequence
from markji.types import (
    Datetime,
    CardID,
    CardRootID,
    DeckID,
    DeckSource,
    File,
    Status,
    UserID,
)


@dataclass
class Card(DataClassJsonMixin):
    """
    Card 卡片

    :param CardID id: 卡片 ID
    :param str content: 内容
    :param int content_type: 内容类型
    :param Status status: 状态
    :param UserID creator: 创建者
    :param DeckID deck_id: 所属卡组 ID
    :param CardRootID root_id: 根卡片 ID
    :param Sequence[File] files: 文件列表
    :param bool is_modified: 是否修改
    :param int revision: 修订版本
    :param int grammar_version: 语法版本
    :param DeckSource source: 来源
    :param Sequence[CardRootID] card_rids: 卡片根 ID 列表
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
    files: Sequence[File]
    is_modified: bool
    revision: int
    grammar_version: int
    source: DeckSource
    card_rids: Sequence[CardRootID]
    created_time: Datetime = Datetime._field()
    updated_time: Datetime = Datetime._field()

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
    files: Sequence[File]
    is_modified: bool
    revision: int
    grammar_version: int
    source: DeckSource
    card_rids: Sequence[CardRootID]
    created_time: _Datetime = _Datetime._field()
    updated_time: _Datetime = _Datetime._field()

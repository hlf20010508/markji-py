"""
:project: markji-py
:author: L-ING
:copyright: (C) 2025 L-ING <hlf01@icloud.com>
:license: MIT, see LICENSE for more details.
"""

from dataclasses import dataclass
from dataclasses_json import DataClassJsonMixin
from typing import Sequence
from markji.types import _Datetime, UserID, FolderID, Status, FolderItem


@dataclass
class RootFolder(DataClassJsonMixin):
    """
    RootFolder 根文件夹

    :param id: 文件夹ID
    :param creator: 创建者ID
    :param status: 文件夹状态
    :param items: 文件夹项目
    :param name: 文件夹名称
    :param created_time: 创建时间
    """

    id: FolderID
    creator: UserID
    status: Status
    items: Sequence[FolderItem]
    name: str
    created_time: _Datetime = _Datetime._field()
    updated_time: _Datetime = _Datetime._field()


@dataclass
class Folder(DataClassJsonMixin):
    """
    Folder 文件夹

    :param id: 文件夹ID
    :param creator: 创建者ID
    :param status: 文件夹状态
    :param items: 文件夹项目
    :param parent_id: 父文件夹ID (root文件夹无此项)
    :param name: 文件夹名称
    :param created_time: 创建时间
    """

    id: FolderID
    creator: UserID
    status: Status
    items: Sequence[FolderItem]
    parent_id: FolderID
    name: str
    created_time: _Datetime = _Datetime._field()
    updated_time: _Datetime = _Datetime._field()

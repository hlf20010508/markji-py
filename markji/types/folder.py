# :project: markji-py
# :author: L-ING
# :copyright: (C) 2025 L-ING <hlf01@icloud.com>
# :license: MIT, see LICENSE for more details.

from dataclasses import dataclass
from dataclasses_json import DataClassJsonMixin
from typing import Sequence
from markji.types import Datetime, UserID, FolderID, Status, FolderItem


@dataclass
class RootFolder(DataClassJsonMixin):
    """
    RootFolder 根文件夹

    :param FolderID id: 文件夹ID
    :param UserID creator: 创建者ID
    :param Status status: 文件夹状态
    :param Sequence[FolderItem] items: 文件夹项目
    :param str name: 文件夹名称
    :param Datetime created_time: 创建时间
    """

    id: FolderID
    creator: UserID
    status: Status
    items: Sequence[FolderItem]
    name: str
    created_time: Datetime = Datetime._field()
    updated_time: Datetime = Datetime._field()


@dataclass
class Folder(DataClassJsonMixin):
    """
    Folder 文件夹

    :param FolderID id: 文件夹ID
    :param UserID creator: 创建者ID
    :param Status status: 文件夹状态
    :param Sequence[FolderItem] items: 文件夹项目
    :param FolderID parent_id: 父文件夹ID
    :param str name: 文件夹名称
    :param Datetime created_time: 创建时间
    :param Datetime updated_time: 更新
    """

    id: FolderID
    creator: UserID
    status: Status
    items: Sequence[FolderItem]
    parent_id: FolderID
    name: str
    created_time: Datetime = Datetime._field()
    updated_time: Datetime = Datetime._field()


@dataclass
class FolderDiff(DataClassJsonMixin):
    """
    FolderDiff 文件夹差异

    :param Folder new_folder: 新文件夹
    :param Folder old_folder: 旧文件夹
    """

    new_folder: Folder
    old_folder: Folder

# :project: markji-py
# :author: L-ING
# :copyright: (C) 2025 L-ING <hlf01@icloud.com>
# :license: MIT, see LICENSE for more details.

from dataclasses import dataclass, field

from dataclasses_json import DataClassJsonMixin

from markji.types import Datetime, FolderID, FolderItem, Status, UserID


@dataclass
class RootFolder(DataClassJsonMixin):
    """
    根文件夹

    :param FolderID id: 文件夹ID
    :param UserID creator: 创建者ID
    :param Status status: 文件夹状态
    :param list[FolderItem] items: 文件夹项目
    :param str name: 文件夹名称
    :param Datetime created_time: 创建时间
    """

    id: FolderID
    creator: UserID
    status: Status
    items: list[FolderItem]
    name: str
    created_time: Datetime = field(metadata=Datetime._metadata())
    updated_time: Datetime = field(metadata=Datetime._metadata())


@dataclass
class Folder(RootFolder):
    """
    文件夹

    :param FolderID id: 文件夹ID
    :param UserID creator: 创建者ID
    :param Status status: 文件夹状态
    :param list[FolderItem] items: 文件夹项目
    :param str name: 文件夹名称
    :param Datetime created_time: 创建时间
    :param Datetime updated_time: 更新
    :param FolderID parent_id: 父文件夹ID
    """

    parent_id: FolderID


@dataclass
class FolderDiff(DataClassJsonMixin):
    """
    文件夹差异

    :param Folder new_folder: 新文件夹
    :param Folder old_folder: 旧文件夹
    """

    new_folder: Folder
    old_folder: Folder

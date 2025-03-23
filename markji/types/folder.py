"""
:project: markji-py
:author: L-ING
:copyright: (C) 2025 L-ING <hlf01@icloud.com>
:license: MIT, see LICENSE for more details.
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Sequence, Type, cast
from markji.types import _Datetime, UserID, FolderID, Status, FolderItem


@dataclass
class RootFolder:
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
    created_time: _Datetime
    updated_time: _Datetime

    @classmethod
    def _from_json(cls: Type[RootFolder], data: dict) -> RootFolder:
        """
        从 JSON 数据创建 RootFolder 对象

        :param data: JSON 数据
        :return: RootFolder 对象
        """
        id = cast(FolderID, data.get("id"))
        creator = cast(UserID, data.get("creator"))
        status = Status(data.get("status"))
        items = [
            cast(FolderItem, FolderItem._from_json(item))
            for item in cast(Sequence, data.get("items"))
        ]
        name = cast(str, data.get("name"))
        created_time = _Datetime.fromisoformat(cast(str, data.get("created_time")))
        updated_time = _Datetime.fromisoformat(cast(str, data.get("updated_time")))

        return cls(
            id=id,
            creator=creator,
            status=status,
            items=items,
            name=name,
            created_time=created_time,
            updated_time=updated_time,
        )


@dataclass
class Folder:
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
    created_time: _Datetime
    updated_time: _Datetime

    @classmethod
    def _from_json(cls: Type[Folder], data: dict) -> Folder:
        """
        从 JSON 数据创建 Folder 对象

        :param data: JSON 数据
        :return: Folder 对象
        """
        id = cast(FolderID, data.get("id"))
        creator = cast(UserID, data.get("creator"))
        status = Status(data.get("status"))
        items = [
            cast(FolderItem, FolderItem._from_json(item))
            for item in cast(Sequence, data.get("items"))
        ]
        parent_id = cast(FolderID, data.get("parent_id"))
        name = cast(str, data.get("name"))
        created_time = _Datetime.fromisoformat(cast(str, data.get("created_time")))
        updated_time = _Datetime.fromisoformat(cast(str, data.get("updated_time")))

        return cls(
            id=id,
            creator=creator,
            status=status,
            items=items,
            parent_id=parent_id,
            name=name,
            created_time=created_time,
            updated_time=updated_time,
        )

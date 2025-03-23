"""
:project: markji-py
:author: L-ING
:copyright: (C) 2025 L-ING <hlf01@icloud.com>
:license: MIT, see LICENSE for more details.
"""

from dataclasses import dataclass, field
from dataclasses_json import DataClassJsonMixin, config
from typing import Sequence
from markji.types import (
    _Datetime,
    ChapterID,
    FolderID,
    FolderItem,
    FolderItemObjectClass,
)


@dataclass
class _LoginForm(DataClassJsonMixin):
    identity: str
    password: str
    nuencrypt_fields: Sequence[str] = field(
        default_factory=lambda: ["password"]
    )  # encrypt password


@dataclass
class _NewFolderForm(DataClassJsonMixin):
    name: str
    order: int


@dataclass
class _RenameFolderForm(DataClassJsonMixin):
    name: str


@dataclass
class _SortFoldersForm(DataClassJsonMixin):
    items: Sequence[FolderID | str] = field(
        metadata=config(
            encoder=lambda ids: [
                FolderItem(i, FolderItemObjectClass.FOLDER).to_dict() for i in ids
            ]
        ),
    )
    updated_time: _Datetime = _Datetime._field()


@dataclass
class _NewDeckForm(DataClassJsonMixin):
    name: str
    description: str
    is_private: bool
    folder_id: FolderID | str


@dataclass
class _UpdateDeckInfoForm(DataClassJsonMixin):
    name: str
    description: str
    is_private: bool


@dataclass
class _NewChapterForm(DataClassJsonMixin):
    name: str
    order: int


@dataclass
class _RenameChapterForm(DataClassJsonMixin):
    name: str


@dataclass
class _SortChaptersForm(DataClassJsonMixin):
    chapter_ids: Sequence[ChapterID | str]
    revision: int

# :project: markji-py
# :author: L-ING
# :copyright: (C) 2025 L-ING <hlf01@icloud.com>
# :license: MIT, see LICENSE for more details.

from dataclasses import dataclass, field
from typing import IO, Iterable

from dataclasses_json import DataClassJsonMixin, config

from markji.types import (
    CardID,
    ChapterID,
    Datetime,
    DeckID,
    FolderID,
    FolderItem,
    ItemObjectClass,
    TTSItem,
    UserID,
)


@dataclass
class _LoginForm(DataClassJsonMixin):
    identity: str
    password: str
    nuencrypt_fields: Iterable[str] = field(
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
    items: Iterable[FolderID | str] = field(
        metadata=config(
            encoder=lambda ids: [
                FolderItem(i, ItemObjectClass.FOLDER).to_dict() for i in ids
            ]
        ),
    )
    updated_time: Datetime = Datetime._field()


@dataclass
class _NewDeckForm(DataClassJsonMixin):
    name: str
    description: str
    is_private: bool
    folder_id: FolderID | str


@dataclass
class _UpdateDeckInfoForm(DataClassJsonMixin):
    name: str | None = field(default=None, metadata=config(exclude=lambda x: x is None))
    description: str | None = field(
        default=None, metadata=config(exclude=lambda x: x is None)
    )
    is_private: bool | None = field(
        default=None, metadata=config(exclude=lambda x: x is None)
    )
    card_price: int | None = field(
        default=None, metadata=config(exclude=lambda x: x is None)
    )


@dataclass
class _UpdateDeckAccessSettingForm(DataClassJsonMixin):
    is_private: bool
    is_searchable: bool | None = field(
        default=None, metadata=config(exclude=lambda x: x is None)
    )
    validation_request_access: bool | None = field(
        default=None, metadata=config(exclude=lambda x: x is None)
    )
    validation_password: str | None = field(
        default=None, metadata=config(exclude=lambda x: x is None)
    )


@dataclass
class _SortDecksForm(DataClassJsonMixin):
    items: Iterable[DeckID | str] = field(
        metadata=config(
            encoder=lambda ids: [
                FolderItem(i, ItemObjectClass.DECK).to_dict() for i in ids
            ]
        ),
    )
    updated_time: Datetime = Datetime._field()


@dataclass
class _MoveDecksForm(DataClassJsonMixin):
    items: Iterable[DeckID | str] = field(
        metadata=config(
            encoder=lambda ids: [
                FolderItem(i, ItemObjectClass.DECK).to_dict() for i in ids
            ]
        ),
    )
    to_folder_id: FolderID | str
    order: int


@dataclass
class _NewChapterForm(DataClassJsonMixin):
    name: str
    order: int


@dataclass
class _RenameChapterForm(DataClassJsonMixin):
    name: str


@dataclass
class _SortChaptersForm(DataClassJsonMixin):
    chapter_ids: Iterable[ChapterID | str]
    revision: int


@dataclass
class _ContentInfo(DataClassJsonMixin):
    content: str
    grammar_version: int


@dataclass
class _NewCardForm(DataClassJsonMixin):
    order: int
    card: _ContentInfo


@dataclass
class _ListCardsForm(DataClassJsonMixin):
    card_ids: Iterable[CardID]


@dataclass
class _EditCardForm(DataClassJsonMixin):
    card: _ContentInfo


@dataclass
class _SortCardsForm(DataClassJsonMixin):
    card_ids: Iterable[CardID | str]
    revision: int


@dataclass
class _MoveCardsForm(DataClassJsonMixin):
    to_chapter_id: ChapterID | str
    order: int
    card_ids: Iterable[CardID | str]


@dataclass
class _UploadFileForm(DataClassJsonMixin):
    file: IO[bytes] = field(
        metadata=config(encoder=lambda file: file),
    )


@dataclass
class _TTSGenForm(DataClassJsonMixin):
    info: TTSItem = field(
        metadata=config(
            encoder=lambda info: [info.to_dict()], field_name="content_slices"
        ),
    )


@dataclass
class _TTSGetFileForm(DataClassJsonMixin):
    url: str


@dataclass
class _QueryUsersForm(DataClassJsonMixin):
    ids: Iterable[UserID | int]

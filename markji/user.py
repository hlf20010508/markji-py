"""
:project: markji-py
:author: L-ING
:copyright: (C) 2025 L-ING <hlf01@icloud.com>
:license: MIT, see LICENSE for more details.
"""

from dataclasses import dataclass
from aiohttp import ClientSession
from markji.folder import Folder
from markji.deck import Deck
from markji._const import _API_URL, _FOLDER_URL

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from markji.auth import Auth


@dataclass
class User:
    _folders: dict[str, Folder]  # folder_id: Folder
    _auth: "Auth"

    @property
    def folder_count(self) -> int:
        return len(self._folders)

    @classmethod
    def _new(cls, auth: "Auth") -> "User":
        return cls({}, auth)

    def _session(self):
        return ClientSession(base_url=_API_URL, headers=self._auth._headers)

    async def new_folder(self, name: str) -> Folder:
        if len(name) == 0 or len(name) > 8:
            raise ValueError("Folder name must be between 1 and 8 characters")

        async with self._session() as session:
            response = await session.post(
                _FOLDER_URL,
                json={"name": name, "order": self.folder_count},
            )
            content: dict = await response.json()
            folder = Folder._from_json(content["data"]["folder"])
            folder.user = self
            self._folders[folder.id] = folder

        return folder

    def get_folder_by_id(self, folder_id: str) -> Folder | None:
        return self._folders.get(folder_id)

    def get_folders_by_name(self, folder_name: str) -> list[Folder]:
        folders = []
        for folder in self._folders.values():
            if folder.name == folder_name:
                folders.append(folder)

        return folders

    async def new_deck(
        self,
        folder: Folder | str,
        name: str,
        description: str = "",
        is_private: bool = False,
    ) -> Deck:
        if isinstance(folder, str):
            folder = self._folders[folder]

        return await folder.new_deck(name, description, is_private)

    def get_deck_by_id(self, deck_id: str) -> Deck | None:
        for folder in self._folders.values():
            deck = folder.get_deck_by_id(deck_id)
            if deck:
                return deck

        return None

    def get_decks_by_name(self, deck_name: str) -> list[Deck]:
        decks = []
        for folder in self._folders.values():
            sub_deck = folder.get_decks_by_name(deck_name)
            decks.extend(sub_deck)

        return decks

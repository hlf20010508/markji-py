"""
:project: markji-py
:author: L-ING
:copyright: (C) 2025 L-ING <hlf01@icloud.com>
:license: MIT, see LICENSE for more details.
"""

from dataclasses import dataclass
from markji.folder import Folder
from markji.deck import Deck
from markji.const import FOLDER_URL

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from markji.auth import Auth


@dataclass
class User:
    folders: dict[str, Folder]
    auth: "Auth"

    @classmethod
    def from_json(cls, json: dict) -> "User":
        folders = {}
        auth = None

        return cls(
            folders,
            auth,
        )

    async def new_folder(self, name: str) -> Folder:
        if len(name) == 0 or len(name) > 8:
            raise ValueError("Folder name must be between 1 and 8 characters")

        async with self.auth.session() as session:
            response = await session.post(
                FOLDER_URL,
                json={"name": name, "order": len(self.folders)},
            )
            content: dict = await response.json()
            folder = Folder.from_json(content["data"]["folder"])
            folder.user = self
            self.folders[folder.id] = folder

        return folder

    async def delete_folder(self, folder: Folder | str):
        if isinstance(folder, str):
            folder = self.folders[folder]

        await folder.delete()

    async def rename_folder(self, folder: Folder | str, name: str):
        if isinstance(folder, str):
            folder = self.folders[folder]

        await folder.rename(name)

    async def new_deck(
        self,
        folder: Folder | str,
        name: str,
        description: str = "",
        is_private: bool = False,
    ) -> Deck:
        if isinstance(folder, str):
            folder = self.folders[folder]

        return await folder.new_deck(name, description, is_private)

    async def delete_deck(self, folder: Folder | str, deck: str):
        if isinstance(folder, str):
            folder = self.folders[folder]

        await folder.decks[deck].delete()

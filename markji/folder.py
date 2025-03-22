"""
:project: markji-py
:author: L-ING
:copyright: (C) 2025 L-ING <hlf01@icloud.com>
:license: MIT, see LICENSE for more details.
"""

from dataclasses import dataclass
from markji.deck import Deck
from markji._const import _DECK_URL, _FOLDER_URL

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from markji.user import User


@dataclass
class Folder:
    id: str
    _decks: dict[str, Deck]  # deck_id: Deck
    name: str
    user: "User"

    @property
    def deck_count(self) -> int:
        return len(self._decks)

    @classmethod
    def _from_json(cls, json: dict) -> "Folder":
        id = json.get("id")
        decks = {}
        name = json.get("name")
        user = None

        return cls(id, decks, name, user)

    def _session(self):
        return self.user._session()

    async def delete(self):
        async with self._session() as session:
            await session.delete(f"{_FOLDER_URL}/{self.id}")
            del self.user._folders[self.id]

    async def rename(self, name: str):
        if len(name) == 0 or len(name) > 8:
            raise ValueError("Folder name must be between 1 and 8 characters")

        async with self._session() as session:
            response = await session.post(
                f"{_FOLDER_URL}/{self.id}",
                json={"name": name},
            )
            content: dict = await response.json()
            self.name = content["data"]["folder"]["name"]

    async def new_deck(
        self, name: str, description: str = "", is_private: bool = False
    ) -> Deck:
        if len(name) == 0 or len(name) > 48:
            raise ValueError("Deck name must be between 1 and 48 characters")

        async with self._session() as session:
            response = await session.post(
                f"{_DECK_URL}",
                json={
                    "name": name,
                    "description": description,
                    "is_private": is_private,
                    "folder_id": self.id,
                },
            )
            content: dict = await response.json()
            deck = Deck._from_json(content["data"]["deck"])
            deck.folder = self
            self._decks[deck.id] = deck

        return deck

    def get_deck_by_id(self, deck_id: str) -> Deck | None:
        return self._decks.get(deck_id)

    def get_decks_by_name(self, deck_name: str) -> list[Deck]:
        decks = []
        for deck in self._decks.values():
            if deck.name == deck_name:
                decks.append(deck)

        return decks

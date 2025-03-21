"""
:project: markji-py
:author: L-ING
:copyright: (C) 2025 L-ING <hlf01@icloud.com>
:license: MIT, see LICENSE for more details.
"""

from dataclasses import dataclass
from markji.deck import Deck
from markji.const import DECK_URL, FOLDER_URL

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from markji.user import User


@dataclass
class Folder:
    id: str
    decks: dict[str, Deck]
    name: str
    user: "User"

    @classmethod
    def from_json(cls, json: dict) -> "Folder":
        id = json.get("id")
        decks = {}
        name = json.get("name")
        user = None

        return cls(id, decks, name, user)

    async def delete(self):
        async with self.user.auth.session() as session:
            await session.delete(f"{FOLDER_URL}/{self.id}")
            del self.user.folders[self.id]

    async def rename(self, name: str):
        async with self.user.auth.session() as session:
            response = await session.post(
                f"{FOLDER_URL}/{self.id}",
                json={"name": name},
            )
            content: dict = await response.json()
            self.name = content["data"]["folder"]["name"]

    async def new_deck(
        self, name: str, description: str = "", is_private: bool = False
    ) -> Deck:
        async with self.user.auth.session() as session:
            response = await session.post(
                f"{DECK_URL}",
                json={
                    "name": name,
                    "description": description,
                    "is_private": is_private,
                    "folder_id": self.id,
                },
            )
            content: dict = await response.json()
            deck = Deck.from_json(content["data"]["deck"])
            deck.folder = self
            self.decks[deck.id] = deck

        return deck

    async def delete_deck(self, deck: Deck | str):
        if isinstance(deck, str):
            deck = self.decks[deck]

        await deck.delete()

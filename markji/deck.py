"""
:project: markji-py
:author: L-ING
:copyright: (C) 2025 L-ING <hlf01@icloud.com>
:license: MIT, see LICENSE for more details.
"""

from dataclasses import dataclass
from enum import Enum
from markji._const import _DECK_URL

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from markji.folder import Folder


class DeckSource(Enum):
    SELF = "SELF"
    FORK = "FORK"

    @classmethod
    def from_str(cls, source: str) -> "DeckSource":
        if source == "SELF":
            return cls.SELF
        elif source == "FORK":
            return cls.FORK
        else:
            raise ValueError("Invalid deck source")


@dataclass
class Deck:
    id: str
    source: DeckSource
    name: str
    description: str
    is_private: bool
    card_count: int
    card_price: int
    chapter_count: int
    folder: "Folder"

    @classmethod
    def _from_json(cls, json: dict) -> "Deck":
        id = json.get("id")
        source = DeckSource.from_str(json.get("source"))
        name = json.get("name")
        description = json.get("description")
        is_private = json.get("is_private")
        card_count = json.get("card_count")
        card_price = json.get("card_price")
        chapter_count = json.get("chapter_count")
        folder = None

        return cls(
            id,
            source,
            name,
            description,
            is_private,
            card_count,
            card_price,
            chapter_count,
            folder,
        )

    def _session(self):
        return self.folder._session()

    async def delete(self):
        async with self._session() as session:
            await session.delete(f"{_DECK_URL}/{self.id}")
            del self.folder._decks[self.id]

    async def update_info(self, name: str, description: str, is_private):
        async with self._session() as session:
            response = await session.post(
                f"{_DECK_URL}/{self.id}",
                json={
                    "name": name,
                    "description": description,
                    "is_private": is_private,
                },
            )
            content: dict = await response.json()
            deck: dict = content["data"]["deck"]

            self.name = deck["name"]
            self.description = deck["description"]
            self.is_private = deck["is_private"]

    async def rename(self, name: str):
        self.update_info(name, self.description, self.is_private)

    async def update_description(self, description: str):
        self.update_info(self.name, description, self.is_private)

    async def update_privacy(self, is_private: bool):
        self.update_info(self.name, self.description, is_private)

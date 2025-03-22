"""
:project: markji-py
:author: L-ING
:copyright: (C) 2025 L-ING <hlf01@icloud.com>
:license: MIT, see LICENSE for more details.
"""

from dataclasses import dataclass
from markji._const import _DECK_URL
from markji.chapter import Chapter

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from markji.folder import Folder


@dataclass
class Deck:
    id: str
    name: str
    description: str
    is_private: bool
    _chapters: dict[str, "Chapter"]
    _folder: "Folder"

    @property
    def chapter_count(self):
        return len(self._chapters)

    @property
    def card_count(self):
        count = 0
        for chapter_id in self._chapters:
            count += self._chapters[chapter_id].card_count

        return count

    @classmethod
    def _from_json(cls, json: dict) -> "Deck":
        id = json.get("id")
        name = json.get("name")
        description = json.get("description")
        is_private = json.get("is_private")
        card_count = json.get("card_count")
        chapter_count = json.get("chapter_count")
        folder = None

        return cls(
            id,
            name,
            description,
            is_private,
            card_count,
            chapter_count,
            folder,
        )

    def _session(self):
        return self._folder._session()

    async def delete(self):
        async with self._session() as session:
            await session.delete(f"{_DECK_URL}/{self.id}")
            del self._folder._decks[self.id]

    async def update_info(self, name: str, description: str, is_private):
        if len(name) == 0 or len(name) > 48:
            raise ValueError("Deck name must be between 1 and 48 characters")

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

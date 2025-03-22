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
    """
    Deck 卡组

    :param id: 卡组 ID
    :param name: 卡组名
    :param description: 卡组描述
    :param is_private: 是否私有
    """

    id: str
    name: str
    description: str
    is_private: bool
    _chapters: dict[str, "Chapter"]
    _folder: "Folder"

    @property
    def chapter_count(self):
        """
        章节数量

        :return: int
        """
        return len(self._chapters)

    @property
    def card_count(self):
        """
        卡片数量

        :return: int
        """
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
        """
        删除卡组
        """
        async with self._session() as session:
            await session.delete(f"{_DECK_URL}/{self.id}")
            del self._folder._decks[self.id]

    async def update_info(self, name: str, description: str, is_private):
        """
        更新卡组信息

        :param name: 卡组名
        :param description: 卡组描述
        :param is_private: 是否私有
        """
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
        """
        重命名卡组

        :param name: 新卡组名
        """
        self.update_info(name, self.description, self.is_private)

    async def update_description(self, description: str):
        """
        更新卡组描述

        :param description: 卡组描述
        """
        self.update_info(self.name, description, self.is_private)

    async def update_privacy(self, is_private: bool):
        """
        更新卡组隐私

        :param is_private: 是否私有
        """
        self.update_info(self.name, self.description, is_private)

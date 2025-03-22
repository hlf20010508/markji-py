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
    """
    Folder 文件夹

    :param id: 文件夹 ID
    :param name: 文件夹名
    :param user: 用户
    """

    id: str
    _decks: dict[str, Deck]  # deck id: Deck
    name: str
    user: "User"

    @property
    def deck_count(self) -> int:
        """
        卡组数量

        :return: int
        """
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
        """
        删除文件夹
        """
        async with self._session() as session:
            await session.delete(f"{_FOLDER_URL}/{self.id}")
            del self.user._folders[self.id]

    async def rename(self, name: str):
        """
        重命名文件夹

        :param name: 新文件夹名
        """
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
        """
        新建卡组

        :param name: 卡组名
        :param description: 卡组描述
        :param is_private: 是否私有
        :return: Deck
        """
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
            deck._folder = self
            self._decks[deck.id] = deck

        return deck

    def get_deck_by_id(self, deck_id: str) -> Deck | None:
        """
        通过卡组ID获取卡组
        若不存在则返回None

        :param deck_id: 卡组ID
        :return: Deck | None
        """
        return self._decks.get(deck_id)

    def get_decks_by_name(self, deck_name: str) -> list[Deck]:
        """
        通过卡组名获取卡组
        返回类型为列表，若有多个同名卡组则返回多个

        :param deck_name: 卡组名
        :return: list[Deck]
        """
        decks = []
        for deck in self._decks.values():
            if deck.name == deck_name:
                decks.append(deck)

        return decks

"""
:project: markji-py
:author: L-ING
:copyright: (C) 2025 L-ING <hlf01@icloud.com>
:license: MIT, see LICENSE for more details.
"""

from typing import Sequence
from aiohttp import ClientSession
from markji._const import (
    _API_URL,
    _CHAPTER_ROUTE,
    _DECK_ROUTE,
    _FOLDER_ROUTE,
    _PROFILE_ROUTE,
    _SORT_ROUTE,
)
from markji.types._form import (
    _NewChapterForm,
    _NewDeckForm,
    _NewFolderForm,
    _RenameChapterForm,
    _RenameFolderForm,
    _SortChaptersForm,
    _SortFoldersForm,
    _UpdateDeckInfoForm,
)
from markji.types import ChapterID, DeckID, FolderID
from markji.types.chapter import Chapter, ChapterSet
from markji.types.deck import Deck
from markji.types.folder import Folder, RootFolder
from markji.types.profile import Profile


class Markji:
    """
    Markji 客户端

    示例::
        from markji import Markji
        from markji.auth import Auth

        auth = Auth("username", "password")
        token = await auth.login()
        client = Markji(token)
    """

    def __init__(self, token: str):
        """
        初始化 Markji 客户端

        :param token: 用户令牌
        """
        self._token = token

    def _session(self):
        return ClientSession(base_url=_API_URL, headers={"token": self._token})

    async def get_profile(self) -> Profile:
        """
        获取用户信息
        """
        async with self._session() as session:
            response = await session.get(_PROFILE_ROUTE)
            if response.status != 200:
                raise Exception(f"获取用户信息失败: {response}{await response.text()}")
            data: dict = await response.json()

        return Profile.from_dict(data["data"]["user"])

    async def get_folder(self, folder_id: FolderID | str) -> Folder:
        """
        获取文件夹

        :param folder_id: 文件夹ID
        :return: Folder
        """
        async with self._session() as session:
            response = await session.get(f"{_FOLDER_ROUTE}/{folder_id}")
            if response.status != 200:
                raise FileNotFoundError(
                    f"获取文件夹失败: {response}{await response.text()}"
                )
            data: dict = await response.json()

        return Folder.from_dict(data["data"]["folder"])

    async def get_root_folder(self) -> RootFolder:
        """
        获取根文件夹

        :return: RootFolder
        """
        async with self._session() as session:
            response = await session.get(_FOLDER_ROUTE)
            if response.status != 200:
                raise Exception(f"获取根文件夹失败: {response}{await response.text()}")
            data: dict = await response.json()
            for folder in data["data"]["folders"]:
                if "parent_id" not in folder:
                    return RootFolder.from_dict(folder)

        raise FileNotFoundError("未找到根文件夹")

    async def list_folders(self) -> Sequence[Folder]:
        """
        获取用户的所有文件夹

        :return: Sequence[Folder]
        """
        async with self._session() as session:
            response = await session.get(_FOLDER_ROUTE)
            if response.status != 200:
                raise Exception(
                    f"获取文件夹列表失败: {response}{await response.text()}"
                )
            data: dict = await response.json()
            folders = []
            for folder in data["data"]["folders"]:
                # bypass root folder
                if "parent_id" not in folder:
                    continue
                folder = Folder.from_dict(folder)
                folders.append(folder)

        return folders

    async def new_folder(self, name: str) -> Folder:
        """
        创建文件夹
        文件名长度必须在 2 到 8 个字符之间

        :param name: 文件夹名
        :return: Folder
        """
        if len(name) < 2 or len(name) > 8:
            raise ValueError("文件夹名必须在 2 到 8 个字符之间")

        async with self._session() as session:
            response = await session.post(
                _FOLDER_ROUTE,
                json=_NewFolderForm(name, len(await self.list_folders())).to_dict(),
            )
            if response.status != 200:
                raise Exception(f"创建文件夹失败: {response}{await response.text()}")
            data: dict = await response.json()

        return Folder.from_dict(data["data"]["folder"])

    async def delete_folder(self, folder_id: FolderID | str):
        """
        删除文件夹

        :param folder_id: 文件夹ID
        """
        async with self._session() as session:
            response = await session.delete(f"{_FOLDER_ROUTE}/{folder_id}")
            if response.status != 200:
                raise Exception(f"删除文件夹失败: {response}{await response.text()}")

    async def rename_folder(self, folder_id: FolderID | str, name: str) -> Folder:
        """
        重命名文件夹
        文件名长度必须在 2 到 8 个字符之间

        :param folder_id: 文件夹ID
        :param name: 新文件夹名
        :return: Folder
        """
        if len(name) < 2 or len(name) > 8:
            raise ValueError("文件夹名必须在 2 到 8 个字符之间")

        async with self._session() as session:
            response = await session.post(
                f"{_FOLDER_ROUTE}/{folder_id}",
                json=_RenameFolderForm(name).to_dict(),
            )
            if response.status != 200:
                raise Exception(f"重命名文件夹失败: {response}{await response.text()}")
            data: dict = await response.json()

        return Folder.from_dict(data["data"]["folder"])

    async def sort_folders(self, folder_ids: Sequence[FolderID | str]) -> RootFolder:
        """
        排序文件夹

        :param folder_ids: 排序后的文件夹ID列表
        :return: RootFolder
        """
        root_folder = await self.get_root_folder()

        async with self._session() as session:
            response = await session.post(
                f"{_FOLDER_ROUTE}/{root_folder.id}/{_SORT_ROUTE}",
                json=_SortFoldersForm(folder_ids, root_folder.updated_time).to_dict(),
            )
            if response.status != 200:
                raise Exception(f"排序文件夹失败: {response}{await response.text()}")
            data: dict = await response.json()

        return RootFolder.from_dict(data["data"]["folder"])

    async def get_deck(self, deck_id: str) -> Deck:
        """
        获取卡组

        :param deck_id: 卡组ID
        :return: Deck
        """
        async with self._session() as session:
            response = await session.get(f"{_DECK_ROUTE}/{deck_id}")
            if response.status != 200:
                raise FileNotFoundError(
                    f"获取卡组失败: {response}{await response.text()}"
                )
            data: dict = await response.json()

        return Deck.from_dict(data["data"]["deck"])

    async def list_decks(self, folder_id: FolderID | str) -> Sequence[Deck]:
        """
        获取文件夹的所有卡组

        :param folder_id: 文件夹ID
        :return: Sequence[Deck]
        """
        async with self._session() as session:
            response = await session.get(_DECK_ROUTE, params={"folder_id": folder_id})
            if response.status != 200:
                raise Exception(f"获取卡组列表失败: {response}{await response.text()}")
            data: dict = await response.json()
            decks = []
            for deck in data["data"]["decks"]:
                deck = Deck.from_dict(deck)
                decks.append(deck)

        return decks

    async def new_deck(
        self,
        folder_id: FolderID | str,
        name: str,
        description: str = "",
        is_private: bool = False,
    ) -> Deck:
        """
        创建卡组
        卡组名长度必须在 2 到 48 个字符之间

        :param folder_id: 文件夹ID
        :param name: 卡组名
        :param description: 卡组描述
        :param is_private: 是否私有
        :return: Deck
        """
        if len(name) < 2 or len(name) > 48:
            raise ValueError("卡组名必须在 2 到 48 个字符之间")

        async with self._session() as session:
            response = await session.post(
                _DECK_ROUTE,
                json=_NewDeckForm(name, description, is_private, folder_id).to_dict(),
            )
            if response.status != 200:
                raise Exception(f"创建卡组失败: {response}{await response.text()}")
            data: dict = await response.json()

        return Deck.from_dict(data["data"]["deck"])

    async def delete_deck(self, deck_id: DeckID | str):
        """
        删除卡组

        :param deck_id: 卡组ID
        """
        async with self._session() as session:
            response = await session.delete(f"{_DECK_ROUTE}/{deck_id}")
            if response.status != 200:
                raise Exception(f"删除卡组失败: {response}{await response.text()}")

    async def update_deck_info(
        self, deck_id: DeckID | str, name: str, description: str, is_private: bool
    ) -> Deck:
        """
        更新卡组信息
        卡组名长度必须在 2 到 48 个字符之间

        :param deck_id: 卡组ID
        :param name: 卡组名
        :param description: 卡组描述
        :param is_private: 是否私有
        :return: Deck
        """
        if len(name) < 2 or len(name) > 48:
            raise ValueError("卡组名必须在 2 到 48 个字符之间")

        async with self._session() as session:
            response = await session.post(
                f"{_DECK_ROUTE}/{deck_id}",
                json=_UpdateDeckInfoForm(name, description, is_private).to_dict(),
            )
            if response.status != 200:
                raise Exception(f"更新卡组信息失败: {response}{await response.text()}")
            data: dict = await response.json()
            deck = Deck.from_dict(data["data"]["deck"])

        return deck

    async def update_deck_name(self, deck_id: DeckID | str, name: str) -> Deck:
        """
        重命名卡组
        卡组名长度必须在 2 到 48 个字符之间

        :param deck_id: 卡组ID
        :param name: 新卡组名
        :return: Deck
        """
        if len(name) < 2 or len(name) > 48:
            raise ValueError("卡组名必须在 2 到 48 个字符之间")

        old_deck = await self.get_deck(deck_id)
        deck = await self.update_deck_info(
            deck_id, name, old_deck.description, old_deck.is_private
        )

        return deck

    async def update_deck_description(
        self, deck_id: DeckID | str, description: str
    ) -> Deck:
        """
        更新卡组描述

        :param deck_id: 卡组ID
        :param description: 卡组描述
        :return: Deck
        """
        old_deck = await self.get_deck(deck_id)
        deck = await self.update_deck_info(
            deck_id, old_deck.name, description, old_deck.is_private
        )

        return deck

    async def update_deck_privacy(
        self, deck_id: DeckID | str, is_private: bool
    ) -> Deck:
        """
        更新卡组隐私状态

        :param deck_id: 卡组ID
        :param is_private: 是否私有
        :return: Deck
        """
        old_deck = await self.get_deck(deck_id)
        deck = await self.update_deck_info(
            deck_id, old_deck.name, old_deck.description, is_private
        )

        return deck

    async def get_chapter(
        self, deck_id: DeckID | str, chapter_id: ChapterID | str
    ) -> Chapter:
        """
        获取章节

        :param deck_id: 卡组ID
        :param chapter_id: 章节ID
        :return: Chapter
        """
        async with self._session() as session:
            response = await session.get(
                f"{_DECK_ROUTE}/{deck_id}/{_CHAPTER_ROUTE}/{chapter_id}"
            )
            if response.status != 200:
                raise FileNotFoundError(
                    f"获取章节失败: {response}{await response.text()}"
                )
            data: dict = await response.json()

        return Chapter.from_dict(data["data"]["chapter"])

    async def get_chapter_set(self, deck_id: DeckID | str) -> ChapterSet:
        """
        获取章节集合

        :param deck_id: 卡组ID
        :return: ChapterSet
        """
        async with self._session() as session:
            response = await session.get(f"{_DECK_ROUTE}/{deck_id}/{_CHAPTER_ROUTE}")
            if response.status != 200:
                raise FileNotFoundError(
                    f"获取章节集合失败: {response}{await response.text()}"
                )
            data: dict = await response.json()

        return ChapterSet.from_dict(data["data"]["chapterset"])

    async def list_chapters(self, deck_id: DeckID | str) -> Sequence[Chapter]:
        """
        获取卡组的所有章节

        :param deck_id: 卡组ID
        :return: Sequence[Chapter]
        """
        async with self._session() as session:
            response = await session.get(f"{_DECK_ROUTE}/{deck_id}/{_CHAPTER_ROUTE}")
            if response.status != 200:
                raise Exception(f"获取章节列表失败: {response}{await response.text()}")
            data: dict = await response.json()
            chapters = []
            for chapter in data["data"]["chapters"]:
                chapter = Chapter.from_dict(chapter)
                chapters.append(chapter)

        return chapters

    async def new_chapter(self, deck_id: DeckID | str, name: str) -> Chapter:
        """
        创建章节
        章节名长度必须在 1 到 48 个字符之间

        :param name: 章节名
        :return: Chapter
        """

        if len(name) < 1 or len(name) > 48:
            raise ValueError("章节名必须在 1 到 48 个字符之间")

        async with self._session() as session:
            response = await session.post(
                f"{_DECK_ROUTE}/{deck_id}/{_CHAPTER_ROUTE}",
                json=_NewChapterForm(
                    name, len(await self.list_chapters(deck_id))
                ).to_dict(),
            )
            if response.status != 200:
                raise Exception(f"创建章节失败: {response}{await response.text()}")
            data: dict = await response.json()

        return Chapter.from_dict(data["data"]["chapter"])

    async def delete_chapter(self, deck_id: DeckID | str, chapter_id: ChapterID | str):
        """
        删除章节

        :param deck_id: 卡组ID
        :param chapter_id: 章节ID
        """
        async with self._session() as session:
            response = await session.delete(
                f"{_DECK_ROUTE}/{deck_id}/{_CHAPTER_ROUTE}/{chapter_id}"
            )
            if response.status != 200:
                raise Exception(f"删除章节失败: {response}{await response.text()}")

    async def rename_chapter(
        self, deck_id: DeckID | str, chapter_id: ChapterID | str, name: str
    ) -> Chapter:
        """
        重命名章节
        章节名长度必须在 1 到 48 个字符之间

        :param deck_id: 卡组ID
        :param chapter_id: 章节ID
        :param name: 新章节名
        :return: Chapter
        """
        if len(name) < 1 or len(name) > 48:
            raise ValueError("章节名必须在 1 到 48 个字符之间")

        async with self._session() as session:
            response = await session.post(
                f"{_DECK_ROUTE}/{deck_id}/{_CHAPTER_ROUTE}/{chapter_id}",
                json=_RenameChapterForm(name).to_dict(),
            )
            if response.status != 200:
                raise Exception(f"重命名章节失败: {response}{await response.text()}")
            data: dict = await response.json()

        return Chapter.from_dict(data["data"]["chapter"])

    async def sort_chapters(
        self, deck_id: DeckID | str, chapter_ids: Sequence[ChapterID | str]
    ) -> ChapterSet:
        """
        排序章节

        :param deck_id: 卡组ID
        :param chapter_ids: 排序后的章节ID列表
        :return: Chapter
        """
        chapter_set = await self.get_chapter_set(deck_id)
        async with self._session() as session:
            response = await session.post(
                f"{_DECK_ROUTE}/{deck_id}/{_CHAPTER_ROUTE}/{_SORT_ROUTE}",
                json=_SortChaptersForm(chapter_ids, chapter_set.revision).to_dict(),
            )
            if response.status != 200:
                raise Exception(f"排序章节失败: {response}{await response.text()}")
            data: dict = await response.json()

        return ChapterSet.from_dict(data["data"]["chapterset"])

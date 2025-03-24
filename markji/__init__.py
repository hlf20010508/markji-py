# :project: markji-py
# :author: L-ING
# :copyright: (C) 2025 L-ING <hlf01@icloud.com>
# :license: MIT, see LICENSE for more details.

from datetime import datetime, UTC

__title__ = "markji-py"
__author__ = "L-ING"
__version__ = "0.1.0"
__license__ = "MIT"
__copyright__ = f"(C) 2025-{datetime.now(UTC).year} {__author__} <hlf01@icloud.com>"

from typing import IO, Sequence
from aiohttp import ClientSession
from markji._const import (
    _API_URL,
    _CARD_ROUTE,
    _CHAPTER_ROUTE,
    _DECK_ROUTE,
    _FILE_ROUTE,
    _FOLDER_ROUTE,
    _MOVE_ROUTE,
    _PROFILE_ROUTE,
    _QUERY_ROUTE,
    _SORT_ROUTE,
    _TTS_ROUTE,
    _URL_ROUTE,
)
from markji.types._form import (
    _ContentInfo,
    _EditCardForm,
    _ListCardsForm,
    _MoveCardsForm,
    _MoveDecksForm,
    _NewCardForm,
    _NewChapterForm,
    _NewDeckForm,
    _NewFolderForm,
    _RenameChapterForm,
    _RenameFolderForm,
    _SortCardsForm,
    _SortChaptersForm,
    _SortDecksForm,
    _SortFoldersForm,
    _TTSGenForm,
    _TTSGetFileForm,
    _UpdateDeckInfoForm,
    _UploadFileForm,
)
from markji.types import CardID, ChapterID, DeckID, FolderID, LanguageCode, TTSInfo
from markji.types.card import Card, File
from markji.types.chapter import Chapter, ChapterDiff, ChapterSet
from markji.types.deck import Deck
from markji.types.folder import Folder, FolderDiff, RootFolder
from markji.types.profile import Profile


class Markji:
    """
    Markji 客户端

    :param str token: 用户令牌

    .. code-block:: python

        from markji import Markji
        from markji.auth import Auth

        auth = Auth("username", "password")
        token = await auth.login()
        client = Markji(token)
    """

    def __init__(self, token: str):
        """
        Markji 客户端

        :param str token: 用户令牌
        """
        self._token = token

    def _session(self):
        return ClientSession(base_url=_API_URL, headers={"token": self._token})

    async def get_profile(self) -> Profile:
        """
        获取用户信息

        :return: 用户信息
        :rtype: Profile
        """
        async with self._session() as session:
            response = await session.get(_PROFILE_ROUTE)
            if response.status != 200:
                raise FileNotFoundError(
                    f"获取用户信息失败: {response}{await response.text()}"
                )
            data: dict = await response.json()

        return Profile.from_dict(data["data"]["user"])

    async def get_folder(self, folder_id: FolderID | str) -> Folder:
        """
        获取文件夹

        :param FolderID | str folder_id: 文件夹ID
        :return: 文件夹
        :rtype: Folder
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

        :return: 根文件夹
        :rtype: RootFolder
        """
        async with self._session() as session:
            response = await session.get(_FOLDER_ROUTE)
            if response.status != 200:
                raise FileNotFoundError(
                    f"获取根文件夹失败: {response}{await response.text()}"
                )
            data: dict = await response.json()
            for folder in data["data"]["folders"]:
                if "parent_id" not in folder:
                    return RootFolder.from_dict(folder)

        raise FileNotFoundError("未找到根文件夹")

    async def list_folders(self) -> Sequence[Folder]:
        """
        获取用户的所有文件夹

        :return: 文件夹列表
        :rtype: Sequence[Folder]
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

        :param str name: 文件夹名
        :return: 创建的文件夹
        :rtype: Folder
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

    async def delete_folder(self, folder_id: FolderID | str) -> RootFolder:
        """
        删除文件夹

        :param FolderID | str folder_id: 文件夹ID
        :return: 删除后的根文件
        :rtype: RootFolder
        """
        async with self._session() as session:
            response = await session.delete(f"{_FOLDER_ROUTE}/{folder_id}")
            if response.status != 200:
                raise FileNotFoundError(
                    f"删除文件夹失败: {response}{await response.text()}"
                )
            data: dict = await response.json()

        return RootFolder.from_dict(data["data"]["parent_folder"])

    async def rename_folder(self, folder_id: FolderID | str, name: str) -> Folder:
        """
        重命名文件夹

        文件名长度必须在 2 到 8 个字符之间

        :param FolderID | str folder_id: 文件夹ID
        :param str name: 新文件夹名
        :return: 重命名后的文件夹
        :rtype: Folder
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

        :param Sequence[FolderID | str] folder_ids: 排序后的文件夹ID列表
        :return: 排序后的根文件夹
        :rtype: RootFolder
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

        :param str deck_id: 卡组ID
        :return: 卡组
        :rtype: Deck
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

        :param FolderID | str folder_id: 文件夹ID
        :return: 卡组列表
        :rtype: Sequence[Deck]
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

        :param FolderID | str folder_id: 文件夹ID
        :param str name: 卡组名
        :param str description: 卡组描述
        :param bool is_private: 是否私有
        :return: 创建的卡组
        :rtype: Deck
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

        :param DeckID | str deck_id: 卡组ID
        """
        async with self._session() as session:
            response = await session.delete(f"{_DECK_ROUTE}/{deck_id}")
            if response.status != 200:
                raise FileNotFoundError(
                    f"删除卡组失败: {response}{await response.text()}"
                )

    async def update_deck_info(
        self, deck_id: DeckID | str, name: str, description: str, is_private: bool
    ) -> Deck:
        """
        更新卡组信息

        卡组名长度必须在 2 到 48 个字符之间

        :param DeckID | str deck_id: 卡组ID
        :param str name: 卡组名
        :param str description: 卡组描述
        :param bool is_private: 是否私有
        :return: 更新后的卡组
        :rtype: Deck
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

        :param DeckID | str deck_id: 卡组ID
        :param str name: 新卡组名
        :return: 更新后的卡组
        :rtype: Deck
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

        :param DeckID | str deck_id: 卡组ID
        :param str description: 卡组描述
        :return: 更新后的卡组
        :rtype: Deck
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

        :param DeckID | str deck_id: 卡组ID
        :param bool is_private: 是否私有
        :return: 更新后的卡组
        :rtype: Deck
        """
        old_deck = await self.get_deck(deck_id)
        deck = await self.update_deck_info(
            deck_id, old_deck.name, old_deck.description, is_private
        )

        return deck

    async def sort_decks(
        self, folder_id: FolderID | str, deck_ids: Sequence[DeckID | str]
    ) -> Folder:
        """
        排序卡组

        :param FolderID | str folder_id: 文件夹ID
        :param Sequence[DeckID | str] deck_ids: 排序后的卡组ID列表
        :return: 排序后的文件夹
        :rtype: Folder
        """
        folder = await self.get_folder(folder_id)

        async with self._session() as session:
            response = await session.post(
                f"{_FOLDER_ROUTE}/{folder_id}/{_SORT_ROUTE}",
                json=_SortDecksForm(deck_ids, folder.updated_time).to_dict(),
            )
            if response.status != 200:
                raise Exception(f"排序卡组失败: {response}{await response.text()}")
            data: dict = await response.json()

        return Folder.from_dict(data["data"]["folder"])

    async def move_decks(
        self,
        folder_id_from: FolderID | str,
        folder_id_to: FolderID | str,
        deck_ids: Sequence[DeckID | str],
        order: int | None = None,
    ) -> FolderDiff:
        """
        移动卡组

        :param FolderID | str folder_id_from: 旧文件夹ID
        :param FolderID | str folder_id_to: 新文件夹ID
        :param Sequence[DeckID | str] deck_ids: 卡组ID列表
        :param int order: 排序
        :return: 文件夹变化
        :rtype: FolderDiff
        """

        if order is None:
            order = len(await self.list_decks(folder_id_to))

        async with self._session() as session:
            response = await session.post(
                f"{_FOLDER_ROUTE}/{folder_id_from}/{_MOVE_ROUTE}",
                json=_MoveDecksForm(deck_ids, folder_id_to, order).to_dict(),
            )
            if response.status != 200:
                raise Exception(f"移动卡组失败: {response}{await response.text()}")
            data: dict = await response.json()

        return FolderDiff.from_dict(data["data"])

    async def get_chapter(
        self, deck_id: DeckID | str, chapter_id: ChapterID | str
    ) -> Chapter:
        """
        获取章节

        :param DeckID | str deck_id: 卡组ID
        :param ChapterID | str chapter_id: 章节ID
        :return: 章节
        :rtype: Chapter
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

        :param DeckID | str deck_id: 卡组ID
        :return: 章节集合
        :rtype: ChapterSet
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

        :param DeckID | str deck_id: 卡组ID
        :return: 章节列表
        :rtype: Sequence[Chapter]
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

        :param DeckID | str deck_id: 卡组ID
        :param str name: 章节名
        :return: 创建的章节
        :rtype: Chapter
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

    async def delete_chapter(
        self, deck_id: DeckID | str, chapter_id: ChapterID | str
    ) -> ChapterSet:
        """
        删除章节

        :param DeckID | str deck_id: 卡组ID
        :param ChapterID | str chapter_id: 章节ID
        :return: 删除后的章节集
        :rtype: ChapterSet
        """
        async with self._session() as session:
            response = await session.delete(
                f"{_DECK_ROUTE}/{deck_id}/{_CHAPTER_ROUTE}/{chapter_id}"
            )
            if response.status != 200:
                raise FileNotFoundError(
                    f"删除章节失败: {response}{await response.text()}"
                )
            data: dict = await response.json()

        return ChapterSet.from_dict(data["data"]["chapterset"])

    async def rename_chapter(
        self, deck_id: DeckID | str, chapter_id: ChapterID | str, name: str
    ) -> Chapter:
        """
        重命名章节

        章节名长度必须在 1 到 48 个字符之间

        :param DeckID | str deck_id: 卡组ID
        :param ChapterID | str chapter_id: 章节ID
        :param str name: 新章节名
        :return: 重命名后的章节
        :rtype: Chapter
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

        :param DeckID | str deck_id: 卡组ID
        :param Sequence[ChapterID | str] chapter_ids: 排序后的章节ID列表
        :return: 排序后的章节集合
        :rtype: ChapterSet
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

    async def get_card(self, deck_id: DeckID | str, card_id: str) -> Card:
        """
        获取卡片

        :param DeckID | str deck_id: 卡组ID
        :param str card_id: 卡片ID
        :return: 卡片
        :rtype: Card
        """
        async with self._session() as session:
            response = await session.get(
                f"{_DECK_ROUTE}/{deck_id}/{_CARD_ROUTE}/{card_id}"
            )
            if response.status != 200:
                raise FileNotFoundError(
                    f"获取卡片失败: {response}{await response.text()}"
                )
            data: dict = await response.json()

        return Card.from_dict(data["data"]["card"])

    async def list_cards(
        self, deck_id: DeckID | str, chapter_id: ChapterID | str
    ) -> Sequence[Card]:
        """
        获取章节的所有卡片

        :param DeckID | str deck_id: 卡组ID
        :param ChapterID | str chapter_id: 章节ID
        :return: 卡片列表
        :rtype: Sequence[Card]
        """
        chapter = await self.get_chapter(deck_id, chapter_id)
        if len(chapter.card_ids) == 0:
            return []

        async with self._session() as session:
            response = await session.post(
                f"{_DECK_ROUTE}/{deck_id}/{_QUERY_ROUTE}",
                json=_ListCardsForm(chapter.card_ids).to_dict(),
            )
            if response.status != 200:
                raise Exception(f"获取卡片列表失败: {response}{await response.text()}")
            data: dict = await response.json()
            cards = []
            for card in data["data"]["cards"]:
                card = Card.from_dict(card)
                cards.append(card)

        return cards

    async def new_card(
        self,
        deck_id: DeckID | str,
        chapter_id: ChapterID | str,
        content: str,
        grammar_version: int = 3,
    ) -> Card:
        """
        创建卡片

        卡片内容长度必须在 1 到 2500 个字符之间

        :param DeckID | str deck_id: 卡组ID
        :param ChapterID | str chapter_id: 章节ID
        :param str content: 卡片内容
        :param int grammar_version: 语法版本
        :return: 创建的卡片
        :rtype: Card
        """
        if len(content) < 1 or len(content) > 2500:
            raise ValueError("卡片内容必须在 1 到 2500 个字符之间")

        async with self._session() as session:
            response = await session.post(
                f"{_DECK_ROUTE}/{deck_id}/{_CHAPTER_ROUTE}/{chapter_id}/{_CARD_ROUTE}",
                json=_NewCardForm(
                    len(await self.list_cards(deck_id, chapter_id)),
                    _ContentInfo(content, grammar_version),
                ).to_dict(),
            )
            if response.status != 200:
                raise Exception(f"创建卡片失败: {response}{await response.text()}")
            data: dict = await response.json()

        return Card.from_dict(data["data"]["card"])

    async def delete_card(
        self, chapter_id: ChapterID | str, deck_id: DeckID | str, card_id: str
    ) -> Chapter:
        """
        删除卡片

        :param ChapterID | str chapter_id: 章节ID
        :param DeckID | str deck_id: 卡组ID
        :param str card_id: 卡片ID
        :return: 删除后的章节
        :rtype: Chapter
        """
        async with self._session() as session:
            response = await session.delete(
                f"{_DECK_ROUTE}/{deck_id}/{_CHAPTER_ROUTE}/{chapter_id}/{_CARD_ROUTE}/{card_id}"
            )
            if response.status != 200:
                raise FileNotFoundError(
                    f"删除卡片失败: {response}{await response.text()}"
                )
            data: dict = await response.json()

        return Chapter.from_dict(data["data"]["chapter"])

    async def edit_card(
        self,
        deck_id: DeckID | str,
        card_id: str,
        content: str,
        grammar_version: int = 3,
    ) -> Card:
        """
        编辑卡片

        卡片内容长度必须在 1 到 2500 个字符之间

        :param DeckID | str deck_id: 卡组ID
        :param str card_id: 卡片ID
        :param str content: 卡片内容
        :param int grammar_version: 语法版本
        :return: 编辑后的卡片
        :rtype: Card
        """
        if len(content) < 1 or len(content) > 2500:
            raise ValueError("卡片内容必须在 1 到 2500 个字符之间")

        async with self._session() as session:
            response = await session.post(
                f"{_DECK_ROUTE}/{deck_id}/{_CARD_ROUTE}/{card_id}",
                json=_EditCardForm(_ContentInfo(content, grammar_version)).to_dict(),
            )
            if response.status != 200:
                raise Exception(f"编辑卡片失败: {response}{await response.text()}")
            data: dict = await response.json()

        return Card.from_dict(data["data"]["card"])

    async def sort_cards(
        self,
        deck_id: DeckID | str,
        chapter_id: ChapterID | str,
        card_ids: Sequence[CardID | str],
    ) -> Chapter:
        """
        排序卡片

        :param DeckID | str deck_id: 卡组ID
        :param ChapterID | str chapter_id: 章节ID
        :param Sequence[str] card_ids: 排序后的卡片ID列表
        :return: 排序后的章节
        :rtype: Chapter
        """
        chapter = await self.get_chapter(deck_id, chapter_id)

        async with self._session() as session:
            response = await session.post(
                f"{_DECK_ROUTE}/{deck_id}/{_CHAPTER_ROUTE}/{chapter_id}/{_CARD_ROUTE}/{_SORT_ROUTE}",
                json=_SortCardsForm(card_ids, chapter.revision).to_dict(),
            )
            if response.status != 200:
                raise Exception(f"排序卡片失败: {response}{await response.text()}")
            data: dict = await response.json()

        return Chapter.from_dict(data["data"]["chapter"])

    async def move_cards(
        self,
        deck_id: DeckID | str,
        chapter_id_from: ChapterID | str,
        chapter_id_to: ChapterID | str,
        card_ids: Sequence[CardID | str],
        order: int | None = None,
    ) -> ChapterDiff:
        """
        移动卡片

        :param DeckID | str deck_id: 卡组ID
        :param ChapterID | str chapter_id: 章节ID
        :param CardID | str card_id: 卡片ID
        :param ChapterID | str new_chapter_id: 新章节ID
        :return: 章节变化
        :rtype: ChapterDiff
        """
        if order is None:
            order = len(await self.list_cards(deck_id, chapter_id_to))

        async with self._session() as session:
            response = await session.post(
                f"{_DECK_ROUTE}/{deck_id}/{_CHAPTER_ROUTE}/{chapter_id_from}/{_CARD_ROUTE}/{_MOVE_ROUTE}",
                json=_MoveCardsForm(chapter_id_to, order, card_ids).to_dict(),
            )
            if response.status != 200:
                raise Exception(f"移动卡片失败: {response}{await response.text()}")
            data: dict = await response.json()

        return ChapterDiff.from_dict(data["data"])

    async def upload_file(self, path: str | IO[bytes]) -> File:
        """
        上传文件（图片和音频）

        :param str | IO[bytes] path: 文件路径或字节流
        :return: 上传后的文件
        :rtype: File
        """
        async with self._session() as session:
            if isinstance(path, str):
                with open(path, "rb") as file:
                    response = await session.post(
                        _FILE_ROUTE, data=_UploadFileForm(file).to_dict()
                    )
            else:
                response = await session.post(
                    _FILE_ROUTE, data=_UploadFileForm(path).to_dict()
                )

            if response.status != 200:
                raise Exception(f"上传文件失败: {response}{await response.text()}")
            data: dict = await response.json()

        return File.from_dict(data["data"]["file"])

    async def tts(self, text: str, lang: LanguageCode | str) -> File:
        """
        语音合成

        :param str text: 文本
        :param LanguageCode | str lang: 语言代码
        :return: 语音文件
        :rtype: File
        """
        lang = LanguageCode(lang) if isinstance(lang, str) else lang

        async with self._session() as session:
            response = await session.post(
                _TTS_ROUTE,
                json=_TTSGenForm(TTSInfo(text, lang)).to_dict(),
            )
            if response.status != 200:
                raise Exception(f"语音合成失败: {response}{await response.text()}")
            data: dict = await response.json()
            url = data["data"]["url"]

            response = await session.post(
                _URL_ROUTE, json=_TTSGetFileForm(url).to_dict()
            )
            if response.status != 200:
                raise Exception(f"获取语音文件失败: {response}{await response.text()}")
            data: dict = await response.json()

        return File.from_dict(data["data"]["file"])

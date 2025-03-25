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

from io import BufferedReader
from typing import IO, Sequence
from aiohttp import ClientSession
from markji._response import _ResponseWrapper
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
    _SEARCH_ROUTE,
    _SORT_ROUTE,
    _TTS_ROUTE,
    _URL_ROUTE,
    _USER_ROUTE,
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
    _QueryUsersForm,
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
from markji.types import (
    CardID,
    ChapterID,
    DeckID,
    FolderID,
    LanguageCode,
    _SearchScope,
    TTSItem,
)
from markji.types.card import Card, CardResult, File, UserID
from markji.types.chapter import Chapter, ChapterDiff, ChapterSet
from markji.types.deck import Deck, DeckBasic, DeckBrief, DeckInfo
from markji.types.folder import Folder, FolderDiff, RootFolder
from markji.types.user import Collaborator, Profile, User, UserBrief


class Markji:
    """
    客户端
    """

    def __init__(self, token: str):
        """
        客户端

        :param str token: 用户令牌

        .. code-block:: python

            from markji import Markji
            from markji.auth import Auth

            auth = Auth("username", "password")
            token = await auth.login()
            client = Markji(token)
        """
        self._token = token

    def _session(self):
        return ClientSession(base_url=_API_URL, headers={"token": self._token})

    async def get_profile(self) -> Profile:
        """
        获取用户信息

        :return: 用户信息
        :rtype: Profile
        :raises aiohttp.ClientResponseError: 获取用户信息失败
        """
        async with self._session() as session:
            async with session.get(_PROFILE_ROUTE) as response:
                response = _ResponseWrapper(response)
                await response.raise_for_status()
                data: dict = await response.json()

        return Profile.from_dict(data["data"]["user"])

    async def query_users(
        self, user_ids: Sequence[UserID | int]
    ) -> Sequence[UserBrief]:
        """
        查询用户信息

        :param Sequence[UserID | int] user_ids: 用户ID列表
        :return: 用户简要信息列表
        :rtype: Sequence[UserBrief]
        :raises aiohttp.ClientResponseError: 查询用户失败
        """
        async with self._session() as session:
            async with session.post(
                f"{_USER_ROUTE}/{_QUERY_ROUTE}",
                json=_QueryUsersForm(user_ids).to_dict(),
            ) as response:
                response = _ResponseWrapper(response)
                await response.raise_for_status()
                data: dict = await response.json()
                users = []
                for user in data["data"]["users"]:
                    user = UserBrief.from_dict(user)
                    users.append(user)

        return users

    async def search_users(
        self, nickname: str, offset: int = 0, limit: int = 10
    ) -> tuple[Sequence[User], int]:
        """
        搜索用户

        昵称长度必须在 1 到 8000 个字符之间

        offset 和 limit 必须大于等于 0

        offset + limit 必须小于等于 10000

        :param str nickname: 用户昵称
        :return: 用户列表, 总数
        :rtype: tuple[Sequence[User], int]
        :raises ValueError: 昵称长度错误
        :raises ValueError: offset 或 limit 错误
        :raises ValueError: offset + limit 错误
        :raises aiohttp.ClientResponseError: 搜索用户失败
        """
        if len(nickname) < 1 or len(nickname) > 8000:
            raise ValueError("昵称长度必须在 1 到 8000 个字符之间")
        if offset < 0 or limit < 0:
            raise ValueError("offset 和 limit 必须大于等于 0")
        if offset + limit > 10000:
            raise ValueError("offset + limit 必须小于等于 10000")

        async with self._session() as session:
            async with session.get(
                f"{_USER_ROUTE}/{_SEARCH_ROUTE}",
                params={"keyword": nickname, "offset": offset, "limit": limit},
            ) as response:
                response = _ResponseWrapper(response)
                await response.raise_for_status()
                data: dict = await response.json()
                users = []
                for user in data["data"]["users"]:
                    user = User.from_dict(user)
                    users.append(user)

        return users, data["data"]["total"]

    async def search_collaborators(
        self, deck_id: DeckID | str, keyword: str | UserID | int
    ) -> Sequence[Collaborator]:
        """
        搜索协作者

        关键词长度必须在 1 到 8000 个字符之间

        :param DeckID | str deck_id: 卡组ID
        :param str | UserID | int keyword: 关键词（UserID，手机，邮箱，昵称）
        :return: 协作者列表
        :rtype: Sequence[Collaborator]
        :raises ValueError: 关键词长度错误
        :raises aiohttp.ClientResponseError: 搜索协作者失败
        """
        if isinstance(keyword, str):
            if len(keyword) < 1 or len(keyword) > 8000:
                raise ValueError("关键词长度必须在 1 到 8000 个字符之间")

        async with self._session() as session:
            async with session.get(
                f"{_USER_ROUTE}/{_SEARCH_ROUTE}",
                params={"collaborated_deck_id": deck_id, "keyword": keyword},
            ) as response:
                response = _ResponseWrapper(response)
                await response.raise_for_status()
                data: dict = await response.json()
                collaborators = []
                for collaborator in data["data"]["users"]:
                    collaborator = Collaborator.from_dict(collaborator)
                    collaborators.append(collaborator)

        return collaborators

    async def get_folder(self, folder_id: FolderID | str) -> Folder:
        """
        获取文件夹

        :param FolderID | str folder_id: 文件夹ID
        :return: 文件夹
        :rtype: Folder
        :raises aiohttp.ClientResponseError: 获取文件夹失败
        """
        async with self._session() as session:
            async with session.get(f"{_FOLDER_ROUTE}/{folder_id}") as response:
                response = _ResponseWrapper(response)
                await response.raise_for_status()
                data: dict = await response.json()

        return Folder.from_dict(data["data"]["folder"])

    async def get_root_folder(self) -> RootFolder:
        """
        获取根文件夹

        :return: 根文件夹
        :rtype: RootFolder
        :raises aiohttp.ClientResponseError: 获取根文件夹失败
        :raises FileNotFoundError: 未找到根文件夹
        """
        async with self._session() as session:
            async with session.get(_FOLDER_ROUTE) as response:
                response = _ResponseWrapper(response)
                await response.raise_for_status()
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
        :raises aiohttp.ClientResponseError: 获取文件夹列表失败
        """
        async with self._session() as session:
            async with session.get(_FOLDER_ROUTE) as response:
                response = _ResponseWrapper(response)
                await response.raise_for_status()
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
        :raises ValueError: 文件夹名长度错误
        :raises aiohttp.ClientResponseError: 创建文件夹失败
        """
        if len(name) < 2 or len(name) > 8:
            raise ValueError("文件夹名必须在 2 到 8 个字符之间")

        async with self._session() as session:
            async with session.post(
                _FOLDER_ROUTE,
                json=_NewFolderForm(name, len(await self.list_folders())).to_dict(),
            ) as response:
                response = _ResponseWrapper(response)
                await response.raise_for_status()
                data: dict = await response.json()

        return Folder.from_dict(data["data"]["folder"])

    async def delete_folder(self, folder_id: FolderID | str) -> RootFolder:
        """
        删除文件夹

        :param FolderID | str folder_id: 文件夹ID
        :return: 删除后的根文件
        :rtype: RootFolder
        :raises aiohttp.ClientResponseError: 删除文件夹失败
        """
        async with self._session() as session:
            async with session.delete(f"{_FOLDER_ROUTE}/{folder_id}") as response:
                response = _ResponseWrapper(response)
                await response.raise_for_status()
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
        :raises ValueError: 文件夹名长度错误
        :raises aiohttp.ClientResponseError: 重命名文件夹失败
        """
        if len(name) < 2 or len(name) > 8:
            raise ValueError("文件夹名必须在 2 到 8 个字符之间")

        async with self._session() as session:
            async with session.post(
                f"{_FOLDER_ROUTE}/{folder_id}",
                json=_RenameFolderForm(name).to_dict(),
            ) as response:
                response = _ResponseWrapper(response)
                await response.raise_for_status()
                data: dict = await response.json()

        return Folder.from_dict(data["data"]["folder"])

    async def sort_folders(self, folder_ids: Sequence[FolderID | str]) -> RootFolder:
        """
        排序文件夹

        :param Sequence[FolderID | str] folder_ids: 排序后的文件夹ID列表
        :return: 排序后的根文件夹
        :rtype: RootFolder
        :raises aiohttp.ClientResponseError: 排序文件夹失败
        """
        root_folder = await self.get_root_folder()

        async with self._session() as session:
            async with session.post(
                f"{_FOLDER_ROUTE}/{root_folder.id}/{_SORT_ROUTE}",
                json=_SortFoldersForm(folder_ids, root_folder.updated_time).to_dict(),
            ) as response:
                response = _ResponseWrapper(response)
                await response.raise_for_status()
                data: dict = await response.json()

        return RootFolder.from_dict(data["data"]["folder"])

    async def get_deck(self, deck_id: str) -> Deck:
        """
        获取卡组

        :param str deck_id: 卡组ID
        :return: 卡组
        :rtype: Deck
        :raises aiohttp.ClientResponseError: 获取卡组失败
        """
        async with self._session() as session:
            async with session.get(f"{_DECK_ROUTE}/{deck_id}") as response:
                response = _ResponseWrapper(response)
                await response.raise_for_status()
                data: dict = await response.json()

        return Deck.from_dict(data["data"]["deck"])

    async def list_decks(self, folder_id: FolderID | str) -> Sequence[DeckBrief]:
        """
        获取文件夹的所有卡组

        :param FolderID | str folder_id: 文件夹ID
        :return: 卡组列表
        :rtype: Sequence[DeckBrief]
        :raises aiohttp.ClientResponseError: 获取卡组列表失败
        """
        async with self._session() as session:
            async with session.get(
                _DECK_ROUTE, params={"folder_id": folder_id}
            ) as response:
                response = _ResponseWrapper(response)
                await response.raise_for_status()
                data: dict = await response.json()
                decks = []
                for deck in data["data"]["decks"]:
                    deck = DeckBrief.from_dict(deck)
                    decks.append(deck)

        return decks

    async def new_deck(
        self,
        folder_id: FolderID | str,
        name: str,
        description: str = "",
        is_private: bool = False,
    ) -> DeckInfo:
        """
        创建卡组

        卡组名长度必须在 2 到 48 个字符之间

        :param FolderID | str folder_id: 文件夹ID
        :param str name: 卡组名
        :param str description: 卡组描述
        :param bool is_private: 是否私有
        :return: 创建的卡组
        :rtype: DeckInfo
        :raises ValueError: 卡组名长度错误
        :raises aiohttp.ClientResponseError: 创建卡组失败
        """
        if len(name) < 2 or len(name) > 48:
            raise ValueError("卡组名必须在 2 到 48 个字符之间")

        async with self._session() as session:
            async with session.post(
                _DECK_ROUTE,
                json=_NewDeckForm(name, description, is_private, folder_id).to_dict(),
            ) as response:
                response = _ResponseWrapper(response)
                await response.raise_for_status()
                data: dict = await response.json()

        return DeckInfo.from_dict(data["data"]["deck"])

    async def delete_deck(self, deck_id: DeckID | str):
        """
        删除卡组

        :param DeckID | str deck_id: 卡组ID
        :raises aiohttp.ClientResponseError: 删除卡组失败
        """
        async with self._session() as session:
            async with session.delete(f"{_DECK_ROUTE}/{deck_id}") as response:
                response = _ResponseWrapper(response)
                await response.raise_for_status()

    async def update_deck_info(
        self, deck_id: DeckID | str, name: str, description: str, is_private: bool
    ) -> DeckBasic:
        """
        更新卡组信息

        卡组名长度必须在 2 到 48 个字符之间

        :param DeckID | str deck_id: 卡组ID
        :param str name: 卡组名
        :param str description: 卡组描述
        :param bool is_private: 是否私有
        :return: 更新后的卡组
        :rtype: DeckBasic
        :raises ValueError: 卡组名长度错误
        :raises aiohttp.ClientResponseError: 更新卡组信息失败
        """
        if len(name) < 2 or len(name) > 48:
            raise ValueError("卡组名必须在 2 到 48 个字符之间")

        async with self._session() as session:
            async with session.post(
                f"{_DECK_ROUTE}/{deck_id}",
                json=_UpdateDeckInfoForm(name, description, is_private).to_dict(),
            ) as response:
                response = _ResponseWrapper(response)
                await response.raise_for_status()
                data: dict = await response.json()
                deck = DeckBasic.from_dict(data["data"]["deck"])

        return deck

    async def update_deck_name(self, deck_id: DeckID | str, name: str) -> DeckBasic:
        """
        重命名卡组

        卡组名长度必须在 2 到 48 个字符之间

        :param DeckID | str deck_id: 卡组ID
        :param str name: 新卡组名
        :return: 更新后的卡组
        :rtype: DeckBasic
        :raises ValueError: 卡组名长度错误
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
    ) -> DeckBasic:
        """
        更新卡组描述

        :param DeckID | str deck_id: 卡组ID
        :param str description: 卡组描述
        :return: 更新后的卡组
        :rtype: DeckBasic
        """
        old_deck = await self.get_deck(deck_id)
        deck = await self.update_deck_info(
            deck_id, old_deck.name, description, old_deck.is_private
        )

        return deck

    async def update_deck_privacy(
        self, deck_id: DeckID | str, is_private: bool
    ) -> DeckBasic:
        """
        更新卡组隐私状态

        :param DeckID | str deck_id: 卡组ID
        :param bool is_private: 是否私有
        :return: 更新后的卡组
        :rtype: DeckBasic
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
        :raises aiohttp.ClientResponseError: 排序卡组失败
        """
        folder = await self.get_folder(folder_id)

        async with self._session() as session:
            async with session.post(
                f"{_FOLDER_ROUTE}/{folder_id}/{_SORT_ROUTE}",
                json=_SortDecksForm(deck_ids, folder.updated_time).to_dict(),
            ) as response:
                response = _ResponseWrapper(response)
                await response.raise_for_status()
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
        :raises aiohttp.ClientResponseError: 移动卡组失败
        """

        if order is None:
            order = len(await self.list_decks(folder_id_to))

        async with self._session() as session:
            async with session.post(
                f"{_FOLDER_ROUTE}/{folder_id_from}/{_MOVE_ROUTE}",
                json=_MoveDecksForm(deck_ids, folder_id_to, order).to_dict(),
            ) as response:
                response = _ResponseWrapper(response)
                await response.raise_for_status()
                data: dict = await response.json()

        return FolderDiff.from_dict(data["data"])

    async def search_decks(
        self, keyword: str, offset: int = 0, limit: int = 10, self_only: bool = False
    ) -> tuple[Sequence[DeckBasic], int]:
        """
        搜索卡组

        关键词长度必须在 1 到 8000 个字符之间

        offset 必须在 0 到 1000 之间

        limit 必须在 1 到 100 之间

        :param str keyword: 关键词
        :param int offset: 偏移
        :param int limit: 限制
        :param bool self_only: 仅自己
        :return: 卡组基本信息列表, 总数
        :rtype: tuple[Sequence[DeckBasic], int]
        :raises ValueError: 关键词长度错误
        :raises ValueError: offset 错误
        :raises ValueError: limit 错误
        :raises aiohttp.ClientResponseError: 搜索卡组失败
        """
        if len(keyword) < 1 or len(keyword) > 8000:
            raise ValueError("关键词长度必须在 1 到 8000 个字符之间")
        if offset < 0 or offset > 1000:
            raise ValueError("offset 必须在 0 到 1000 之间")
        if limit < 1 or limit > 100:
            raise ValueError("limit 必须在 1 到 100 之间")

        async with self._session() as session:
            params = {
                "keyword": keyword,
                "offset": offset,
                "limit": limit,
                "debug": "true",
                "source": "SEARCH",
            }

            if self_only:
                params["scope"] = _SearchScope.MINE
            else:
                params["scope"] = _SearchScope.ALL

            async with session.get(
                f"{_DECK_ROUTE}/{_SEARCH_ROUTE}",
                params=params,
            ) as response:
                response = _ResponseWrapper(response)
                await response.raise_for_status()
                data: dict = await response.json()
                decks = []
                for deck in data["data"]["decks"]:
                    deck = DeckBasic.from_dict(deck)
                    decks.append(deck)

        return decks, data["data"]["total"]

    async def get_chapter(
        self, deck_id: DeckID | str, chapter_id: ChapterID | str
    ) -> Chapter:
        """
        获取章节

        :param DeckID | str deck_id: 卡组ID
        :param ChapterID | str chapter_id: 章节ID
        :return: 章节
        :rtype: Chapter
        :raises aiohttp.ClientResponseError: 获取章节失败
        """
        async with self._session() as session:
            async with session.get(
                f"{_DECK_ROUTE}/{deck_id}/{_CHAPTER_ROUTE}/{chapter_id}"
            ) as response:
                response = _ResponseWrapper(response)
                await response.raise_for_status()
                data: dict = await response.json()

        return Chapter.from_dict(data["data"]["chapter"])

    async def get_chapter_set(self, deck_id: DeckID | str) -> ChapterSet:
        """
        获取章节集合

        :param DeckID | str deck_id: 卡组ID
        :return: 章节集合
        :rtype: ChapterSet
        :raises aiohttp.ClientResponseError: 获取章节集合失败
        """
        async with self._session() as session:
            async with session.get(
                f"{_DECK_ROUTE}/{deck_id}/{_CHAPTER_ROUTE}"
            ) as response:
                response = _ResponseWrapper(response)
                await response.raise_for_status()
                data: dict = await response.json()

        return ChapterSet.from_dict(data["data"]["chapterset"])

    async def list_chapters(self, deck_id: DeckID | str) -> Sequence[Chapter]:
        """
        获取卡组的所有章节

        :param DeckID | str deck_id: 卡组ID
        :return: 章节列表
        :rtype: Sequence[Chapter]
        :raises aiohttp.ClientResponseError: 获取章节列表失败
        """
        async with self._session() as session:
            async with session.get(
                f"{_DECK_ROUTE}/{deck_id}/{_CHAPTER_ROUTE}"
            ) as response:
                response = _ResponseWrapper(response)
                await response.raise_for_status()
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
        :raises ValueError: 章节名长度错误
        :raises aiohttp.ClientResponseError: 创建章节失败
        """

        if len(name) < 1 or len(name) > 48:
            raise ValueError("章节名必须在 1 到 48 个字符之间")

        async with self._session() as session:
            async with session.post(
                f"{_DECK_ROUTE}/{deck_id}/{_CHAPTER_ROUTE}",
                json=_NewChapterForm(
                    name, len(await self.list_chapters(deck_id))
                ).to_dict(),
            ) as response:
                response = _ResponseWrapper(response)
                await response.raise_for_status()
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
        :raises aiohttp.ClientResponseError: 删除章节失败
        """
        async with self._session() as session:
            async with session.delete(
                f"{_DECK_ROUTE}/{deck_id}/{_CHAPTER_ROUTE}/{chapter_id}"
            ) as response:
                response = _ResponseWrapper(response)
                await response.raise_for_status()
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
        :raises ValueError: 章节名长度错误
        :raises aiohttp.ClientResponseError: 重命名章节失败
        """
        if len(name) < 1 or len(name) > 48:
            raise ValueError("章节名必须在 1 到 48 个字符之间")

        async with self._session() as session:
            async with session.post(
                f"{_DECK_ROUTE}/{deck_id}/{_CHAPTER_ROUTE}/{chapter_id}",
                json=_RenameChapterForm(name).to_dict(),
            ) as response:
                response = _ResponseWrapper(response)
                await response.raise_for_status()
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
        :raises aiohttp.ClientResponseError: 排序章节失败
        """
        chapter_set = await self.get_chapter_set(deck_id)
        async with self._session() as session:
            async with session.post(
                f"{_DECK_ROUTE}/{deck_id}/{_CHAPTER_ROUTE}/{_SORT_ROUTE}",
                json=_SortChaptersForm(chapter_ids, chapter_set.revision).to_dict(),
            ) as response:
                response = _ResponseWrapper(response)
                await response.raise_for_status()
                data: dict = await response.json()

        return ChapterSet.from_dict(data["data"]["chapterset"])

    async def get_card(self, deck_id: DeckID | str, card_id: str) -> Card:
        """
        获取卡片

        :param DeckID | str deck_id: 卡组ID
        :param str card_id: 卡片ID
        :return: 卡片
        :rtype: Card
        :raises aiohttp.ClientResponseError: 获取卡片失败
        """
        async with self._session() as session:
            async with session.get(
                f"{_DECK_ROUTE}/{deck_id}/{_CARD_ROUTE}/{card_id}"
            ) as response:
                response = _ResponseWrapper(response)
                await response.raise_for_status()
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
        :raises aiohttp.ClientResponseError: 获取卡片列表失败
        """
        chapter = await self.get_chapter(deck_id, chapter_id)
        if len(chapter.card_ids) == 0:
            return []

        async with self._session() as session:
            async with session.post(
                f"{_DECK_ROUTE}/{deck_id}/{_CARD_ROUTE}/{_QUERY_ROUTE}",
                json=_ListCardsForm(chapter.card_ids).to_dict(),
            ) as response:
                response = _ResponseWrapper(response)
                await response.raise_for_status()
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
        :raises ValueError: 卡片内容长度错误
        :raises aiohttp.ClientResponseError: 创建卡片失败
        """
        if len(content) < 1 or len(content) > 2500:
            raise ValueError("卡片内容必须在 1 到 2500 个字符之间")

        async with self._session() as session:
            async with session.post(
                f"{_DECK_ROUTE}/{deck_id}/{_CHAPTER_ROUTE}/{chapter_id}/{_CARD_ROUTE}",
                json=_NewCardForm(
                    len(await self.list_cards(deck_id, chapter_id)),
                    _ContentInfo(content, grammar_version),
                ).to_dict(),
            ) as response:
                response = _ResponseWrapper(response)
                await response.raise_for_status()
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
        :raises aiohttp.ClientResponseError: 删除卡片失败
        """
        async with self._session() as session:
            async with session.delete(
                f"{_DECK_ROUTE}/{deck_id}/{_CHAPTER_ROUTE}/{chapter_id}/{_CARD_ROUTE}/{card_id}"
            ) as response:
                response = _ResponseWrapper(response)
                await response.raise_for_status()
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
        :raises ValueError: 卡片内容长度错误
        :raises aiohttp.ClientResponseError: 编辑卡片失败
        """
        if len(content) < 1 or len(content) > 2500:
            raise ValueError("卡片内容必须在 1 到 2500 个字符之间")

        async with self._session() as session:
            async with session.post(
                f"{_DECK_ROUTE}/{deck_id}/{_CARD_ROUTE}/{card_id}",
                json=_EditCardForm(_ContentInfo(content, grammar_version)).to_dict(),
            ) as response:
                response = _ResponseWrapper(response)
                await response.raise_for_status()
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
        :raises aiohttp.ClientResponseError: 排序卡片失败
        """
        chapter = await self.get_chapter(deck_id, chapter_id)

        async with self._session() as session:
            async with session.post(
                f"{_DECK_ROUTE}/{deck_id}/{_CHAPTER_ROUTE}/{chapter_id}/{_CARD_ROUTE}/{_SORT_ROUTE}",
                json=_SortCardsForm(card_ids, chapter.revision).to_dict(),
            ) as response:
                response = _ResponseWrapper(response)
                await response.raise_for_status()
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
        :raises aiohttp.ClientResponseError: 移动卡片失败
        """
        if order is None:
            order = len(await self.list_cards(deck_id, chapter_id_to))

        async with self._session() as session:
            async with session.post(
                f"{_DECK_ROUTE}/{deck_id}/{_CHAPTER_ROUTE}/{chapter_id_from}/{_CARD_ROUTE}/{_MOVE_ROUTE}",
                json=_MoveCardsForm(chapter_id_to, order, card_ids).to_dict(),
            ) as response:
                response = _ResponseWrapper(response)
                await response.raise_for_status()
                data: dict = await response.json()

        return ChapterDiff.from_dict(data["data"])

    async def search_cards(
        self,
        keyword: str,
        offset: int = 0,
        limit: int = 10,
        self_only: bool = False,
    ) -> tuple[Sequence[CardResult], int]:
        """
        搜索卡片

        关键词长度必须在 1 到 8000 个字符之间

        offset 必须在 0 到 1000 之间

        limit 必须在 10 到 100 之间

        :param str keyword: 关键词
        :param int offset: 偏移
        :param int limit: 限制
        :param bool self_only: 仅自己的
        :return: 卡片列表, 总数
        :rtype: tuple[Sequence[Card], int]
        :raises ValueError: 关键词长度错误
        :raises ValueError: offset 错误
        :raises ValueError: limit 错误
        :raises aiohttp.ClientResponseError: 搜索卡片失败
        """
        if len(keyword) < 1 or len(keyword) > 8000:
            raise ValueError("关键词长度必须在 1 到 8000 个字符之间")
        if offset < 0 or offset > 1000:
            raise ValueError("offset 必须在 0 到 1000 之间")
        if limit < 10 or limit > 100:
            raise ValueError("limit 必须在 10 到 100 之间")

        async with self._session() as session:
            params = {
                "keyword": keyword,
                "offset": offset,
                "limit": limit,
                "source": "SEARCH",
            }

            if self_only:
                params["scope"] = _SearchScope.MINE

            async with session.get(
                f"{_CARD_ROUTE}/{_SEARCH_ROUTE}",
                params=params,
            ) as response:
                response = _ResponseWrapper(response)
                await response.raise_for_status()
                data: dict = await response.json()
                cards = []
                for card in data["data"]["cards"]:
                    card = CardResult.from_dict(card)
                    cards.append(card)

        return cards, data["data"]["total"]

    async def upload_file(self, path: str | IO[bytes]) -> File:
        """
        上传文件（图片和音频）

        :param str | IO[bytes] path: 文件路径或字节流
        :return: 上传后的文件
        :rtype: File
        :raises aiohttp.ClientResponseError: 上传文件失败
        """
        async with self._session() as session:
            if isinstance(path, str):
                io = open(path, "rb")
            else:
                io = path

            async with session.post(
                _FILE_ROUTE, data=_UploadFileForm(io).to_dict()
            ) as response:
                if isinstance(io, BufferedReader):
                    io.close()
                response = _ResponseWrapper(response)
                await response.raise_for_status()
                data: dict = await response.json()

        return File.from_dict(data["data"]["file"])

    async def tts(self, text: str, lang: LanguageCode | str) -> File:
        """
        语音合成

        :param str text: 文本
        :param LanguageCode | str lang: 语言代码
        :return: 语音文件
        :rtype: File
        :raises aiohttp.ClientResponseError: 语音合成失败
        :raises aiohttp.ClientResponseError: 获取语音文件失败
        """
        lang = LanguageCode(lang) if isinstance(lang, str) else lang

        async with self._session() as session:
            async with session.post(
                _TTS_ROUTE,
                json=_TTSGenForm(TTSItem(text, lang)).to_dict(),
            ) as response:
                response = _ResponseWrapper(response)
                await response.raise_for_status()
                data: dict = await response.json()
                url = data["data"]["url"]

            async with session.post(
                _URL_ROUTE, json=_TTSGetFileForm(url).to_dict()
            ) as response:
                response = _ResponseWrapper(response)
                await response.raise_for_status()
                data: dict = await response.json()

        return File.from_dict(data["data"]["file"])

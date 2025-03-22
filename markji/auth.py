"""
:project: markji-py
:author: L-ING
:copyright: (C) 2025 L-ING <hlf01@icloud.com>
:license: MIT, see LICENSE for more details.
"""

from aiohttp import ClientSession
from markji.user import User
from markji.folder import Folder
from markji.deck import Deck
from markji._const import _API_URL, _LOGIN_URL, _FOLDER_URL, _DECK_URL


class Auth:
    def __init__(self, username: str, password: str):
        self._username = username
        self._password = password

    async def login(self) -> User:
        async with ClientSession(base_url=_API_URL) as session:
            response = await session.post(
                _LOGIN_URL,
                json={
                    "identity": self._username,
                    "password": self._password,
                    "nuencrypt_fields": ["password"],
                },
            )
            content: dict = await response.json()
            user = User._new(self)

            self.token: str = content["data"]["token"]

            response = await session.get(_FOLDER_URL, headers=self._headers)
            content: dict = await response.json()
            folders = content["data"]["folders"]
            for folder in folders:
                # useless root folder
                if "parent_id" not in folder:
                    continue
                folder = Folder._from_json(folder)

                response = await session.get(
                    _DECK_URL,
                    headers=self._headers,
                    params={"folder_id": folder.id},
                )
                content: dict = await response.json()
                decks = content["data"]["decks"]
                for deck in decks:
                    # bypass the forked deck
                    if deck.get("source") == "FORK":
                        continue
                    deck = Deck._from_json(deck)
                    deck._folder = folder
                    folder._decks[deck.id] = deck

                folder.user = user
                user._folders[folder.id] = folder

        return user

    @property
    def _headers(self):
        return {"token": self.token}

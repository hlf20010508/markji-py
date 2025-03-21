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
from markji.const import API_URL, LOGIN_URL, FOLDER_URL, DECK_URL


class Auth:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    async def login(self) -> User:
        async with ClientSession(base_url=API_URL) as session:
            response = await session.post(
                LOGIN_URL,
                json={
                    "identity": self.username,
                    "password": self.password,
                    "nuencrypt_fields": ["password"],
                },
            )
            content: dict = await response.json()
            user = User.from_json(content["data"])

            self.token: str = content["data"]["token"]

            response = await session.get(FOLDER_URL, headers={"token": self.token})
            content: dict = await response.json()
            folders = content["data"]["folders"]
            for folder in folders:
                # useless root folder
                if "parent_id" not in folder:
                    continue
                folder = Folder.from_json(folder)

                response = await session.get(
                    DECK_URL,
                    headers={"token": self.token},
                    params={"folder_id": folder.id},
                )
                content: dict = await response.json()
                decks = content["data"]["decks"]
                for deck in decks:
                    deck = Deck.from_json(deck)
                    deck.folder = folder
                    folder.decks[deck.id] = deck

                folder.user = user
                user.folders[folder.id] = folder

            user.auth = self

        return user

    def session(self):
        return ClientSession(base_url=API_URL, headers={"token": self.token})

# :project: markji-py
# :author: L-ING
# :copyright: (C) 2025 L-ING <hlf01@icloud.com>
# :license: MIT, see LICENSE for more details.

import unittest
from tests import AsyncTestCase, ENV
from markji import Markji
from markji.auth import Auth


class TestUser(AsyncTestCase):
    async def test_get_profile(self):
        auth = Auth(ENV.username, ENV.password)
        token = await auth.login()
        client = Markji(token)

        await client.get_profile()

    async def test_query(self):
        auth = Auth(ENV.username, ENV.password)
        token = await auth.login()
        client = Markji(token)

        profile = await client.get_profile()

        users = await client.query_users([profile.id])

        self.assertEqual(len(users), 1)
        self.assertEqual(users[0].id, profile.id)

    async def test_search(self):
        auth = Auth(ENV.username, ENV.password)
        token = await auth.login()
        client = Markji(token)

        profile = await client.get_profile()

        users = await client.search_users(profile.nickname)

        self.assertEqual(len(users), 1)
        self.assertEqual(users[0].id, profile.id)

        users = await client.search_users(profile.phone)

        self.assertEqual(len(users), 0)

        users = await client.search_users(profile.email)

        self.assertEqual(len(users), 0)

        users = await client.search_users(str(profile.id))

        self.assertEqual(len(users), 0)

    async def test_search_collaborators(self):
        auth = Auth(ENV.username, ENV.password)
        token = await auth.login()
        client = Markji(token)

        folder_name = "t_folder"
        folder = await client.new_folder(folder_name)
        deck_name = "t_deck"
        deck = await client.new_deck(folder.id, deck_name)

        profile = await client.get_profile()

        users = await client.search_collaborators(deck.id, profile.id)

        self.assertEqual(len(users), 1)
        self.assertEqual(users[0].id, profile.id)

        users = await client.search_collaborators(deck.id, profile.nickname)

        self.assertEqual(len(users), 1)
        self.assertEqual(users[0].id, profile.id)

        users = await client.search_collaborators(deck.id, profile.phone)

        self.assertEqual(len(users), 1)
        self.assertEqual(users[0].id, profile.id)

        users = await client.search_collaborators(deck.id, profile.email)

        self.assertEqual(len(users), 1)
        self.assertEqual(users[0].id, profile.id)

        await client.delete_deck(deck.id)
        await client.delete_folder(folder.id)


if __name__ == "__main__":
    unittest.main()

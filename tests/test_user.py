# :project: markji-py
# :author: L-ING
# :copyright: (C) 2025 L-ING <hlf01@icloud.com>
# :license: MIT, see LICENSE for more details.

import unittest
from tests import AsyncTestCase


class TestUser(AsyncTestCase):
    async def test_get_profile(self):
        await self.client.get_profile()

    async def test_query(self):
        profile = await self.client.get_profile()

        users = await self.client.query_users([profile.id])

        self.assertEqual(len(users), 1)
        self.assertEqual(users[0].id, profile.id)

    async def test_search(self):
        profile = await self.client.get_profile()

        users, num = await self.client.search_users(profile.nickname)

        self.assertEqual(len(users), 1)
        self.assertEqual(users[0].id, profile.id)
        self.assertTrue(num >= len(users))

        users, num = await self.client.search_users(profile.phone)

        self.assertEqual(len(users), 0)

        users, num = await self.client.search_users(profile.email)

        self.assertEqual(len(users), 0)

        users, num = await self.client.search_users(str(profile.id))

        self.assertEqual(len(users), 0)

        with self.assertRaises(ValueError):
            await self.client.search_users("")
        with self.assertRaises(ValueError):
            await self.client.search_users("_" * 8001)
        with self.assertRaises(ValueError):
            await self.client.search_users(profile.nickname, offset=-1)
        with self.assertRaises(ValueError):
            await self.client.search_users(profile.nickname, limit=-1)
        with self.assertRaises(ValueError):
            await self.client.search_users(profile.nickname, offset=9990, limit=11)

    async def test_search_collaborators(self):
        folder_name = "t_folder"
        folder = await self.client.new_folder(folder_name)
        self.addCleanup(self.client.delete_folder, folder.id)
        deck_name = "t_deck"
        deck = await self.client.new_deck(folder.id, deck_name)
        self.addCleanup(self.client.delete_deck, deck.id)

        profile = await self.client.get_profile()

        users = await self.client.search_collaborators(deck.id, profile.id)

        self.assertEqual(len(users), 1)
        self.assertEqual(users[0].id, profile.id)

        users = await self.client.search_collaborators(deck.id, profile.nickname)

        self.assertEqual(len(users), 1)
        self.assertEqual(users[0].id, profile.id)

        users = await self.client.search_collaborators(deck.id, profile.phone)

        self.assertEqual(len(users), 1)
        self.assertEqual(users[0].id, profile.id)

        users = await self.client.search_collaborators(deck.id, profile.email)

        self.assertEqual(len(users), 1)
        self.assertEqual(users[0].id, profile.id)

        with self.assertRaises(ValueError):
            await self.client.search_collaborators(deck.id, "")
        with self.assertRaises(ValueError):
            await self.client.search_collaborators(deck.id, "_" * 8001)


if __name__ == "__main__":
    unittest.main()

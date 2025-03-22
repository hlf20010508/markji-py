"""
:project: markji-py
:author: L-ING
:copyright: (C) 2025 L-ING <hlf01@icloud.com>
:license: MIT, see LICENSE for more details.
"""

import unittest
from tests import AsyncTestCase, ENV
from markji.auth import Auth


class TestUser(AsyncTestCase):
    async def test_folder_new_and_delete(self):
        auth = Auth(ENV.username, ENV.password)
        user = await auth.login()

        folder_name = "t_folder"
        folder_number = user.folder_count
        folder = await user.new_folder(folder_name)
        new_folder_number = user.folder_count

        self.assertEqual(folder.name, folder_name)
        self.assertEqual(new_folder_number, folder_number + 1)

        await folder.delete()
        new_folder_number = user.folder_count

        self.assertEqual(new_folder_number, folder_number)

    async def test_deck_new_and_delete(self):
        auth = Auth(ENV.username, ENV.password)
        user = await auth.login()

        folder_name = "t_folder"
        folder = await user.new_folder(folder_name)
        new_deck_name = "t_deck"
        deck = await user.new_deck(folder, new_deck_name)

        self.assertEqual(deck.name, new_deck_name)
        self.assertEqual(folder.deck_count, 1)

        await deck.delete()

        self.assertEqual(folder.deck_count, 0)

        await folder.delete()


if __name__ == "__main__":
    unittest.main()

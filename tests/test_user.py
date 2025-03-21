"""
:project: markji-py
:author: L-ING
:copyright: (C) 2025 L-ING <hlf01@icloud.com>
:license: MIT, see LICENSE for more details.
"""

import unittest
import warnings
from tests.utils import ENV
from markji.auth import Auth


class TestFolder(unittest.IsolatedAsyncioTestCase):
    async def test_folder_new_and_delete(self):
        auth = Auth(ENV.username, ENV.password)
        user = await auth.login()

        folder_name = "t_folder"
        folder_number = len(user.folders)
        folder = await user.new_folder(folder_name)
        new_folder_number = len(user.folders)

        self.assertEqual(folder.name, folder_name)
        self.assertEqual(new_folder_number, folder_number + 1)

        await user.delete_folder(folder)
        new_folder_number = len(user.folders)

        self.assertEqual(new_folder_number, folder_number)

    async def test_folder_rename(self):
        auth = Auth(ENV.username, ENV.password)
        user = await auth.login()

        folder_name = "t_folder"
        folder = await user.new_folder(folder_name)

        new_folder_name = "r_folder"
        await user.rename_folder(folder, new_folder_name)

        self.assertEqual(folder.name, new_folder_name)

        await user.delete_folder(folder)

    def setUp(self):
        warnings.simplefilter("ignore", ResourceWarning)


class TestDeck(unittest.IsolatedAsyncioTestCase):
    async def test_deck_and_delete(self):
        auth = Auth(ENV.username, ENV.password)
        user = await auth.login()

        folder_name = "t_folder"
        folder = await user.new_folder(folder_name)
        new_deck_name = "t_deck"
        deck = await user.new_deck(folder, new_deck_name)

        self.assertEqual(deck.name, new_deck_name)
        self.assertEqual(len(folder.decks), 1)

        await user.delete_deck(folder, deck.id)

        self.assertEqual(len(folder.decks), 0)

        await folder.delete()


if __name__ == "__main__":
    unittest.main()

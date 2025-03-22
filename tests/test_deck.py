"""
:project: markji-py
:author: L-ING
:copyright: (C) 2025 L-ING <hlf01@icloud.com>
:license: MIT, see LICENSE for more details.
"""

import unittest
from tests import AsyncTestCase, ENV
from markji.auth import Auth


class TestDeck(AsyncTestCase):
    async def test_update_info(self):
        auth = Auth(ENV.username, ENV.password)
        user = await auth.login()

        folder_name = "t_folder"
        folder = await user.new_folder(folder_name)
        deck_name = "t_deck"
        deck = await user.new_deck(folder, deck_name)

        new_deck_name = "r_deck"
        new_description = "new_description"
        new_privacy = True

        await deck.update_info(new_deck_name, new_description, new_privacy)

        self.assertEqual(deck.name, new_deck_name)
        self.assertEqual(deck.description, new_description)
        self.assertEqual(deck.is_private, new_privacy)

        await deck.delete()
        await folder.delete()


if __name__ == "__main__":
    unittest.main()

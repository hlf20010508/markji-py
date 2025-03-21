"""
:project: markji-py
:author: L-ING
:copyright: (C) 2025 L-ING <hlf01@icloud.com>
:license: MIT, see LICENSE for more details.
"""

import unittest
from tests import AsyncTestCase, ENV
from markji import Markji
from markji.auth import Auth


class TestDeck(AsyncTestCase):
    async def test_get(self):
        auth = Auth(ENV.username, ENV.password)
        token = await auth.login()
        client = Markji(token)

        folder_name = "t_folder"
        folder = await client.new_folder(folder_name)
        deck_name = "t_deck"
        deck = await client.new_deck(folder.id, deck_name)

        deck = await client.get_deck(deck.id)
        self.assertEqual(deck.name, deck_name)

        await client.delete_deck(deck.id)
        await client.delete_folder(folder.id)

    async def test_list(self):
        auth = Auth(ENV.username, ENV.password)
        token = await auth.login()
        client = Markji(token)

        folder_name = "t_folder"
        folder = await client.new_folder(folder_name)
        deck_name = "t_deck"
        deck = await client.new_deck(folder.id, deck_name)

        decks = await client.list_decks(folder.id)
        self.assertEqual(len(decks), 1)

        await client.delete_deck(deck.id)
        await client.delete_folder(folder.id)

    async def test_new(self):
        auth = Auth(ENV.username, ENV.password)
        token = await auth.login()
        client = Markji(token)

        folder_name = "t_folder"
        folder = await client.new_folder(folder_name)
        deck_name = "t_deck"
        deck = await client.new_deck(folder.id, deck_name)

        self.assertEqual(deck.name, deck_name)

        await client.delete_deck(deck.id)

        deck_name = "t"
        with self.assertRaises(ValueError):
            await client.new_deck(folder.id, deck_name)

        deck_name = "t" + "_" * 48
        with self.assertRaises(ValueError):
            await client.new_deck(folder.id, deck_name)

        await client.delete_folder(folder.id)

    async def test_delete(self):
        auth = Auth(ENV.username, ENV.password)
        token = await auth.login()
        client = Markji(token)

        folder_name = "t_folder"
        folder = await client.new_folder(folder_name)
        deck_name = "t_deck"
        deck = await client.new_deck(folder.id, deck_name)

        await client.delete_deck(deck.id)

        with self.assertRaises(FileNotFoundError):
            await client.get_deck(deck.id)

        await client.delete_folder(folder.id)

    async def test_update_info(self):
        auth = Auth(ENV.username, ENV.password)
        token = await auth.login()
        client = Markji(token)

        folder_name = "t_folder"
        folder = await client.new_folder(folder_name)
        deck_name = "t_deck"
        deck = await client.new_deck(folder.id, deck_name)

        new_deck_name = "r_deck"
        new_description = "new_description"
        new_privacy = True
        deck = await client.update_deck_info(
            deck.id, new_deck_name, new_description, new_privacy
        )

        self.assertEqual(deck.name, new_deck_name)
        self.assertEqual(deck.description, new_description)
        self.assertEqual(deck.is_private, new_privacy)

        new_deck_name = "t"
        with self.assertRaises(ValueError):
            await client.update_deck_info(
                deck.id, new_deck_name, new_description, new_privacy
            )

        new_deck_name = "t" + "_" * 48
        with self.assertRaises(ValueError):
            await client.update_deck_info(
                deck.id, new_deck_name, new_description, new_privacy
            )

        await client.delete_deck(deck.id)
        await client.delete_folder(folder.id)

    async def test_update_name(self):
        auth = Auth(ENV.username, ENV.password)
        token = await auth.login()
        client = Markji(token)

        folder_name = "t_folder"
        folder = await client.new_folder(folder_name)
        deck_name = "t_deck"
        deck = await client.new_deck(folder.id, deck_name)

        new_deck_name = "r_deck"
        deck = await client.update_deck_name(deck.id, new_deck_name)

        self.assertEqual(deck.name, new_deck_name)

        new_deck_name = "t"
        with self.assertRaises(ValueError):
            await client.update_deck_name(deck.id, new_deck_name)

        new_deck_name = "t" + "_" * 48
        with self.assertRaises(ValueError):
            await client.update_deck_name(deck.id, new_deck_name)

        await client.delete_deck(deck.id)
        await client.delete_folder(folder.id)

    async def test_update_description(self):
        auth = Auth(ENV.username, ENV.password)
        token = await auth.login()
        client = Markji(token)

        folder_name = "t_folder"
        folder = await client.new_folder(folder_name)
        deck_name = "t_deck"
        deck = await client.new_deck(folder.id, deck_name)

        new_description = "new_description"
        deck = await client.update_deck_description(deck.id, new_description)

        self.assertEqual(deck.description, new_description)

        await client.delete_deck(deck.id)
        await client.delete_folder(folder.id)

    async def test_update_privacy(self):
        auth = Auth(ENV.username, ENV.password)
        token = await auth.login()
        client = Markji(token)

        folder_name = "t_folder"
        folder = await client.new_folder(folder_name)
        deck_name = "t_deck"
        deck = await client.new_deck(folder.id, deck_name)

        new_privacy = True
        deck = await client.update_deck_privacy(deck.id, new_privacy)

        self.assertEqual(deck.is_private, new_privacy)

        await client.delete_deck(deck.id)
        await client.delete_folder(folder.id)


if __name__ == "__main__":
    unittest.main()

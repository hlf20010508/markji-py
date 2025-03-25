# :project: markji-py
# :author: L-ING
# :copyright: (C) 2025 L-ING <hlf01@icloud.com>
# :license: MIT, see LICENSE for more details.

import unittest
from aiohttp import ClientResponseError
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
        self.addCleanup(client.delete_folder, folder.id)
        deck_name = "t_deck"
        deck = await client.new_deck(folder.id, deck_name)
        self.addCleanup(client.delete_deck, deck.id)

        deck = await client.get_deck(deck.id)
        self.assertEqual(deck.name, deck_name)

    async def test_list(self):
        auth = Auth(ENV.username, ENV.password)
        token = await auth.login()
        client = Markji(token)

        folder_name = "t_folder"
        folder = await client.new_folder(folder_name)
        self.addCleanup(client.delete_folder, folder.id)
        deck_name = "t_deck"
        deck = await client.new_deck(folder.id, deck_name)
        self.addCleanup(client.delete_deck, deck.id)

        decks = await client.list_decks(folder.id)
        self.assertEqual(len(decks), 1)

    async def test_new(self):
        auth = Auth(ENV.username, ENV.password)
        token = await auth.login()
        client = Markji(token)

        folder_name = "t_folder"
        folder = await client.new_folder(folder_name)
        self.addCleanup(client.delete_folder, folder.id)
        deck_name = "t_deck"
        deck = await client.new_deck(folder.id, deck_name)
        self.addCleanup(client.delete_deck, deck.id)

        self.assertEqual(deck.name, deck_name)

        deck_name = "t"
        with self.assertRaises(ValueError):
            await client.new_deck(folder.id, deck_name)

        deck_name = "t" + "_" * 48
        with self.assertRaises(ValueError):
            await client.new_deck(folder.id, deck_name)

    async def test_delete(self):
        auth = Auth(ENV.username, ENV.password)
        token = await auth.login()
        client = Markji(token)

        folder_name = "t_folder"
        folder = await client.new_folder(folder_name)
        deck_name = "t_deck"
        deck = await client.new_deck(folder.id, deck_name)

        await client.delete_deck(deck.id)

        with self.assertRaises(ClientResponseError):
            await client.get_deck(deck.id)

        await client.delete_folder(folder.id)

    async def test_update_info(self):
        auth = Auth(ENV.username, ENV.password)
        token = await auth.login()
        client = Markji(token)

        folder_name = "t_folder"
        folder = await client.new_folder(folder_name)
        self.addCleanup(client.delete_folder, folder.id)
        deck_name = "t_deck"
        deck = await client.new_deck(folder.id, deck_name)
        self.addCleanup(client.delete_deck, deck.id)

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

    async def test_update_name(self):
        auth = Auth(ENV.username, ENV.password)
        token = await auth.login()
        client = Markji(token)

        folder_name = "t_folder"
        folder = await client.new_folder(folder_name)
        self.addCleanup(client.delete_folder, folder.id)
        deck_name = "t_deck"
        deck = await client.new_deck(folder.id, deck_name)
        self.addCleanup(client.delete_deck, deck.id)

        new_deck_name = "r_deck"
        deck = await client.update_deck_name(deck.id, new_deck_name)

        self.assertEqual(deck.name, new_deck_name)

        new_deck_name = "t"
        with self.assertRaises(ValueError):
            await client.update_deck_name(deck.id, new_deck_name)

        new_deck_name = "t" + "_" * 48
        with self.assertRaises(ValueError):
            await client.update_deck_name(deck.id, new_deck_name)

    async def test_update_description(self):
        auth = Auth(ENV.username, ENV.password)
        token = await auth.login()
        client = Markji(token)

        folder_name = "t_folder"
        folder = await client.new_folder(folder_name)
        self.addCleanup(client.delete_folder, folder.id)
        deck_name = "t_deck"
        deck = await client.new_deck(folder.id, deck_name)
        self.addCleanup(client.delete_deck, deck.id)

        new_description = "new_description"
        deck = await client.update_deck_description(deck.id, new_description)

        self.assertEqual(deck.description, new_description)

    async def test_update_privacy(self):
        auth = Auth(ENV.username, ENV.password)
        token = await auth.login()
        client = Markji(token)

        folder_name = "t_folder"
        folder = await client.new_folder(folder_name)
        self.addCleanup(client.delete_folder, folder.id)
        deck_name = "t_deck"
        deck = await client.new_deck(folder.id, deck_name)
        self.addCleanup(client.delete_deck, deck.id)

        new_privacy = True
        deck = await client.update_deck_privacy(deck.id, new_privacy)

        self.assertEqual(deck.is_private, new_privacy)

    async def test_sort(self):
        auth = Auth(ENV.username, ENV.password)
        token = await auth.login()
        client = Markji(token)

        folder_name = "t_folder"
        folder = await client.new_folder(folder_name)
        self.addCleanup(client.delete_folder, folder.id)

        deck_name1 = "t_deck1"
        deck1 = await client.new_deck(folder.id, deck_name1)
        self.addCleanup(client.delete_deck, deck1.id)
        deck_name2 = "t_deck2"
        deck2 = await client.new_deck(folder.id, deck_name2)
        self.addCleanup(client.delete_deck, deck2.id)

        deck_ids = [deck2.id, deck1.id]
        folder = await client.sort_decks(folder.id, deck_ids)

        self.assertEqual([i.object_id for i in folder.items], deck_ids)

    async def test_move(self):
        auth = Auth(ENV.username, ENV.password)
        token = await auth.login()
        client = Markji(token)

        folder_name1 = "t_f1"
        folder1 = await client.new_folder(folder_name1)
        self.addCleanup(client.delete_folder, folder1.id)
        deck_name1 = "t_deck1"
        deck1 = await client.new_deck(folder1.id, deck_name1)
        self.addCleanup(client.delete_deck, deck1.id)

        folder_name2 = "t_f2"
        folder2 = await client.new_folder(folder_name2)
        self.addCleanup(client.delete_folder, folder2.id)
        deck_name2 = "t_deck2"
        deck2 = await client.new_deck(folder2.id, deck_name2)
        self.addCleanup(client.delete_deck, deck2.id)
        deck_name3 = "t_deck3"
        deck3 = await client.new_deck(folder2.id, deck_name3)
        self.addCleanup(client.delete_deck, deck3.id)

        folder_diff = await client.move_decks(folder2.id, folder1.id, [deck3.id], 0)

        deck_ids1 = [deck3.id, deck1.id]
        deck_ids2 = [deck2.id]

        self.assertEqual([i.object_id for i in folder_diff.new_folder.items], deck_ids1)
        self.assertEqual([i.object_id for i in folder_diff.old_folder.items], deck_ids2)

    async def test_search(self):
        auth = Auth(ENV.username, ENV.password)
        token = await auth.login()
        client = Markji(token)

        decks1, num1 = await client.search_decks("english")
        decks2, num2 = await client.search_decks("english", self_only=True)

        self.assertTrue(num1 > len(decks1))
        self.assertEqual(len(decks1), 10)
        self.assertTrue(num2 >= len(decks2))
        self.assertTrue(num1 > num2)

        with self.assertRaises(ValueError):
            await client.search_decks("")
        with self.assertRaises(ValueError):
            await client.search_decks("_" * 8001)
        with self.assertRaises(ValueError):
            await client.search_decks("english", offset=-1)
        with self.assertRaises(ValueError):
            await client.search_decks("english", offset=1001)
        with self.assertRaises(ValueError):
            await client.search_decks("english", limit=0)
        with self.assertRaises(ValueError):
            await client.search_decks("english", limit=101)

    async def test_fork(self):
        auth = Auth(ENV.username, ENV.password)
        token = await auth.login()
        client = Markji(token)

        decks, num1 = await client.search_decks("english")
        deck = decks[0]

        deck_forked = await client.fork_deck(deck.id)
        self.addCleanup(client.delete_deck, deck_forked.id)

        self.assertEqual(deck.name, deck_forked.name)
        self.assertNotEqual(deck.id, deck_forked.id)

        folder_name = "t_folder"
        folder = await client.new_folder(folder_name)
        self.addCleanup(client.delete_folder, folder.id)
        deck_name = "t_deck"
        deck = await client.new_deck(folder.id, deck_name)
        self.addCleanup(client.delete_deck, deck.id)

        with self.assertRaises(ClientResponseError):
            await client.fork_deck(deck.id)


if __name__ == "__main__":
    unittest.main()

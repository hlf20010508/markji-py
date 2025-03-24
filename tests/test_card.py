# :project: markji-py
# :author: L-ING
# :copyright: (C) 2025 L-ING <hlf01@icloud.com>
# :license: MIT, see LICENSE for more details.

import unittest
from tests import AsyncTestCase, ENV
from markji import Markji
from markji.auth import Auth


class TestCard(AsyncTestCase):
    async def test_get(self):
        auth = Auth(ENV.username, ENV.password)
        token = await auth.login()
        client = Markji(token)

        folder_name = "t_folder"
        folder = await client.new_folder(folder_name)
        deck_name = "t_deck"
        deck = await client.new_deck(folder.id, deck_name)
        chapter_name = "t_chapter"
        chapter = await client.new_chapter(deck.id, chapter_name)
        card_content = "t_card"
        card = await client.new_card(deck.id, chapter.id, card_content)

        card = await client.get_card(deck.id, card.id)
        self.assertEqual(card.content, card_content)

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
        chapter_name = "t_chapter"
        chapter = await client.new_chapter(deck.id, chapter_name)
        card_content = "t_card"
        card = await client.new_card(deck.id, chapter.id, card_content)

        cards = await client.list_cards(deck.id, chapter.id)
        self.assertEqual(len(cards), 1)

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
        chapter_name = "t_chapter"
        chapter = await client.new_chapter(deck.id, chapter_name)
        card_content = "t_card"
        card = await client.new_card(deck.id, chapter.id, card_content)

        self.assertEqual(card.content, card_content)

        card_content = ""
        with self.assertRaises(ValueError):
            await client.new_card(deck.id, chapter.id, card_content)

        card_content = "t" + "_" * 2500
        with self.assertRaises(ValueError):
            await client.new_card(deck.id, chapter.id, card_content)

        await client.delete_deck(deck.id)
        await client.delete_folder(folder.id)

    async def test_delete(self):
        auth = Auth(ENV.username, ENV.password)
        token = await auth.login()
        client = Markji(token)

        folder_name = "t_folder"
        folder = await client.new_folder(folder_name)
        deck_name = "t_deck"
        deck = await client.new_deck(folder.id, deck_name)
        chapter_name = "t_chapter"
        chapter = await client.new_chapter(deck.id, chapter_name)
        card_content = "t_card"
        card = await client.new_card(deck.id, chapter.id, card_content)

        await client.delete_card(chapter.id, deck.id, card.id)

        with self.assertRaises(FileNotFoundError):
            await client.get_card(deck.id, card.id)

        await client.delete_deck(deck.id)
        await client.delete_folder(folder.id)

    async def test_edit(self):
        auth = Auth(ENV.username, ENV.password)
        token = await auth.login()
        client = Markji(token)

        folder_name = "t_folder"
        folder = await client.new_folder(folder_name)
        deck_name = "t_deck"
        deck = await client.new_deck(folder.id, deck_name)
        chapter_name = "t_chapter"
        chapter = await client.new_chapter(deck.id, chapter_name)
        card_content = "t_card"
        card = await client.new_card(deck.id, chapter.id, card_content)

        new_content = "new_content"
        card = await client.edit_card(deck.id, card.id, new_content)

        self.assertEqual(card.content, new_content)

        new_content = ""
        with self.assertRaises(ValueError):
            await client.edit_card(deck.id, card.id, new_content)

        new_content = "t" + "_" * 2500
        with self.assertRaises(ValueError):
            await client.edit_card(deck.id, card.id, new_content)

        await client.delete_deck(deck.id)
        await client.delete_folder(folder.id)

    async def test_sort(self):
        auth = Auth(ENV.username, ENV.password)
        token = await auth.login()
        client = Markji(token)

        folder_name = "t_folder"
        folder = await client.new_folder(folder_name)
        deck_name = "t_deck"
        deck = await client.new_deck(folder.id, deck_name)
        chapter_name = "t_chapter"
        chapter = await client.new_chapter(deck.id, chapter_name)

        card_content1 = "t_card1"
        card1 = await client.new_card(deck.id, chapter.id, card_content1)
        card_content2 = "t_card2"
        card2 = await client.new_card(deck.id, chapter.id, card_content2)

        card_ids = [card2.id, card1.id]
        chapter = await client.sort_cards(deck.id, chapter.id, card_ids)

        self.assertEqual(list(chapter.card_ids), card_ids)

        await client.delete_deck(deck.id)
        await client.delete_folder(folder.id)

    async def test_move(self):
        auth = Auth(ENV.username, ENV.password)
        token = await auth.login()
        client = Markji(token)

        folder_name = "t_folder"
        folder = await client.new_folder(folder_name)
        deck_name = "t_deck"
        deck = await client.new_deck(folder.id, deck_name)

        chapter_name1 = "t_chapter1"
        chapter1 = await client.new_chapter(deck.id, chapter_name1)
        card_content1 = "t_card1"
        card1 = await client.new_card(deck.id, chapter1.id, card_content1)

        chapter_name2 = "t_chapter2"
        chapter2 = await client.new_chapter(deck.id, chapter_name2)
        card_content2 = "t_card2"
        card2 = await client.new_card(deck.id, chapter2.id, card_content2)
        card_content3 = "t_card3"
        card3 = await client.new_card(deck.id, chapter2.id, card_content3)

        chapter_diff = await client.move_cards(
            deck.id, chapter2.id, chapter1.id, [card3.id], 0
        )

        card_ids1 = [card3.id, card1.id]
        card_ids2 = [card2.id]

        self.assertEqual(list(chapter_diff.new_chapter.card_ids), card_ids1)
        self.assertEqual(list(chapter_diff.old_chapter.card_ids), card_ids2)

        await client.delete_deck(deck.id)
        await client.delete_folder(folder.id)

    async def test_search(self):
        auth = Auth(ENV.username, ENV.password)
        token = await auth.login()
        client = Markji(token)

        cards, num = await client.search_cards("english")

        self.assertTrue(num > len(cards))
        self.assertEqual(len(cards), 10)

        with self.assertRaises(ValueError):
            await client.search_cards("")
        with self.assertRaises(ValueError):
            await client.search_cards("_" * 8001)
        with self.assertRaises(ValueError):
            await client.search_cards("english", offset=-1)
        with self.assertRaises(ValueError):
            await client.search_cards("english", offset=1001)
        with self.assertRaises(ValueError):
            await client.search_cards("english", limit=9)
        with self.assertRaises(ValueError):
            await client.search_cards("english", limit=101)


if __name__ == "__main__":
    unittest.main()

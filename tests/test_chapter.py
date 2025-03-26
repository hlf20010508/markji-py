# :project: markji-py
# :author: L-ING
# :copyright: (C) 2025 L-ING <hlf01@icloud.com>
# :license: MIT, see LICENSE for more details.

import unittest
from aiohttp import ClientResponseError
from tests import AsyncTestCase


class TestChapter(AsyncTestCase):
    async def test_get(self):
        folder_name = "t_folder"
        folder = await self.client.new_folder(folder_name)
        self.addCleanup(self.client.delete_folder, folder.id)
        deck_name = "t_deck"
        deck = await self.client.new_deck(folder.id, deck_name)
        self.addCleanup(self.client.delete_deck, deck.id)

        chapter_name = "t_chapter"
        chapter = await self.client.new_chapter(deck.id, chapter_name)

        chapter = await self.client.get_chapter(deck.id, chapter.id)
        self.assertEqual(chapter.name, chapter_name)

    async def test_get_chapter_set(self):
        folder_name = "t_folder"
        folder = await self.client.new_folder(folder_name)
        self.addCleanup(self.client.delete_folder, folder.id)
        deck_name = "t_deck"
        deck = await self.client.new_deck(folder.id, deck_name)
        self.addCleanup(self.client.delete_deck, deck.id)

        chapter_name = "t_chapter"
        chapter = await self.client.new_chapter(deck.id, chapter_name)

        chapter_set = await self.client.get_chapter_set(deck.id)
        self.assertTrue(chapter.id in chapter_set.chapter_ids)

    async def test_list(self):
        folder_name = "t_folder"
        folder = await self.client.new_folder(folder_name)
        self.addCleanup(self.client.delete_folder, folder.id)
        deck_name = "t_deck"
        deck = await self.client.new_deck(folder.id, deck_name)
        self.addCleanup(self.client.delete_deck, deck.id)

        chapter_name = "t_chapter"
        await self.client.new_chapter(deck.id, chapter_name)

        chapters = await self.client.list_chapters(deck.id)
        self.assertEqual(len(chapters), 2)

    async def test_new(self):
        folder_name = "t_folder"
        folder = await self.client.new_folder(folder_name)
        self.addCleanup(self.client.delete_folder, folder.id)
        deck_name = "t_deck"
        deck = await self.client.new_deck(folder.id, deck_name)
        self.addCleanup(self.client.delete_deck, deck.id)

        chapter_name = "t_chapter"
        chapter = await self.client.new_chapter(deck.id, chapter_name)

        self.assertEqual(chapter.name, chapter_name)

        chapter_name = ""
        with self.assertRaises(ValueError):
            await self.client.new_chapter(deck.id, chapter_name)

        chapter_name = "t" + "_" * 48
        with self.assertRaises(ValueError):
            await self.client.new_chapter(deck.id, chapter_name)

    async def test_delete(self):
        folder_name = "t_folder"
        folder = await self.client.new_folder(folder_name)
        self.addCleanup(self.client.delete_folder, folder.id)
        deck_name = "t_deck"
        deck = await self.client.new_deck(folder.id, deck_name)
        self.addCleanup(self.client.delete_deck, deck.id)

        chapter_name = "t_chapter"
        chapter = await self.client.new_chapter(deck.id, chapter_name)

        await self.client.delete_chapter(deck.id, chapter.id)

        with self.assertRaises(ClientResponseError):
            await self.client.get_chapter(deck.id, chapter.id)

    async def test_rename(self):
        folder_name = "t_folder"
        folder = await self.client.new_folder(folder_name)
        self.addCleanup(self.client.delete_folder, folder.id)
        deck_name = "t_deck"
        deck = await self.client.new_deck(folder.id, deck_name)
        self.addCleanup(self.client.delete_deck, deck.id)

        chapter_name = "t_chapter"
        chapter = await self.client.new_chapter(deck.id, chapter_name)

        new_chapter_name = "t_chapter_new"
        chapter = await self.client.rename_chapter(
            deck.id, chapter.id, new_chapter_name
        )

        self.assertEqual(chapter.name, new_chapter_name)

        new_chapter_name = ""
        with self.assertRaises(ValueError):
            await self.client.rename_chapter(deck.id, chapter.id, new_chapter_name)

        new_chapter_name = "t" + "_" * 48
        with self.assertRaises(ValueError):
            await self.client.rename_chapter(deck.id, chapter.id, new_chapter_name)

    async def test_sort(self):
        folder_name = "t_folder"
        folder = await self.client.new_folder(folder_name)
        self.addCleanup(self.client.delete_folder, folder.id)
        deck_name = "t_deck"
        deck = await self.client.new_deck(folder.id, deck_name)
        self.addCleanup(self.client.delete_deck, deck.id)

        chapter_set = await self.client.get_chapter_set(deck.id)
        default_chapter_ids = chapter_set.chapter_ids

        chapter_name1 = "t_chapter1"
        chapter1 = await self.client.new_chapter(deck.id, chapter_name1)
        chapter_name2 = "t_chapter2"
        chapter2 = await self.client.new_chapter(deck.id, chapter_name2)

        chapter_ids = [chapter2.id, chapter1.id]
        chapter_ids.extend(default_chapter_ids)
        chapter_set = await self.client.sort_chapters(deck.id, chapter_ids)

        self.assertListEqual(chapter_set.chapter_ids, chapter_ids)


if __name__ == "__main__":
    unittest.main()

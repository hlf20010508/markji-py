# :project: markji-py
# :author: L-ING
# :copyright: (C) 2025 L-ING <hlf01@icloud.com>
# :license: MIT, see LICENSE for more details.

from typing import cast
from markji.editor import AnswerLine, AudioBuilder, ParagraphBuilder
from markji.types import LanguageCode
from markji.types.deck import DeckInfo
from markji.types.folder import Folder
from tests import AsyncTestCase, ENV
from markji import Markji
from markji.auth import Auth


class TestExample(AsyncTestCase):
    async def test(self):
        auth = Auth(ENV.username, ENV.password)
        token = await auth.login()
        client = Markji(token)

        folder_name = "t_folder"
        _folder = await client.new_folder(folder_name)
        self.addCleanup(client.delete_folder, _folder.id)

        folder = None
        folders = await client.list_folders()
        for _folder in folders:
            if _folder.name == folder_name:
                folder = _folder
                break

        self.assertIsNotNone(folder)

        folder = cast(Folder, folder)

        self.assertEqual(folder.name, folder_name)
        self.assertEqual(type(folder), Folder)

        deck_name = "t_deck"
        _deck = await client.new_deck(folder.id, deck_name)
        self.addCleanup(client.delete_deck, _deck.id)

        deck = None
        decks = await client.list_decks(folder.id)

        for _deck in decks:
            if _deck.name == deck_name:
                deck = _deck
                break

        self.assertIsNotNone(deck)

        deck = cast(DeckInfo, deck)

        self.assertEqual(deck.name, deck_name)

        chapters = await client.list_chapters(deck.id)

        self.assertTrue(len(chapters) == 1)

        chapter = chapters[0]

        content = []

        word = "English"
        tts = await client.tts(word, LanguageCode.EN_US)
        word = ParagraphBuilder(AudioBuilder(tts.id, word)).heading().build()
        content.append(word)
        content.append(AnswerLine)
        content.append("英语")
        content = "\n".join(content)

        card = await client.new_card(deck.id, chapter.id, content)

        self.assertEqual(card.content, content)

# :project: markji-py
# :author: L-ING
# :copyright: (C) 2025 L-ING <hlf01@icloud.com>
# :license: MIT, see LICENSE for more details.

import unittest
import itertools
from markji import Markji
from markji.auth import Auth
from markji.types import LanguageCode
from markji.editor import (
    AnswerLine,
    AudioBuilder,
    ClozeBuilder,
    FontBackgroundColor,
    FontBuilder,
    FontColor,
    FontScript,
    ParagraphBuilder,
    ReferenceBuilder,
)
from tests import ENV, AsyncTestCase


class TestAnswerLine(unittest.TestCase):
    def test(self):
        self.assertEqual(AnswerLine, "---")


class TestFont(unittest.TestCase):
    def test(self):
        result = FontBuilder("test").build()

        self.assertEqual(result, "[T##test]")

    def test_bold(self):
        result = FontBuilder("test").bold().build()

        self.assertEqual(result, "[T#B#test]")

    def test_color(self):
        result = FontBuilder("test").color(FontColor.RED).build()

        self.assertEqual(result, "[T#!d16056#test]")

    def test_background(self):
        result = FontBuilder("test").background(FontBackgroundColor.RED).build()

        self.assertEqual(result, "[T#!!fbc0bc#test]")

    def test_italics(self):
        result = FontBuilder("test").italics().build()

        self.assertEqual(result, "[T#I#test]")

    def test_underline(self):
        result = FontBuilder("test").underline().build()

        self.assertEqual(result, "[T#U#test]")

    def test_script(self):
        result = FontBuilder("test").script(FontScript.UP).build()

        self.assertEqual(result, "[T#up#test]")

        result = FontBuilder("test").script(FontScript.DOWN).build()

        self.assertEqual(result, "[T#down#test]")

    def test_combination(self):
        result = (
            FontBuilder("test")
            .bold()
            .color(FontColor.YELLOW)
            .background(FontBackgroundColor.GREEN)
            .italics()
            .underline()
            .script(FontScript.UP)
            .build()
        )

        all_correct = [
            f"[T#{",".join(e)}#test]"
            for e in itertools.permutations(
                ["B", "!eb9e27", "!!c5f1c0", "I", "U", "up"], 6
            )
        ]

        self.assertIn(result, all_correct)


class TestParagraph(AsyncTestCase):
    def test(self):
        result = ParagraphBuilder("test").build()

        self.assertEqual(result, "[P##test]")

    def test_heading(self):
        result = ParagraphBuilder("test").heading().build()

        self.assertEqual(result, "[P#H1#test]")

    def test_center(self):
        result = ParagraphBuilder("test").center().build()

        self.assertEqual(result, "[P#center#test]")

    def test_list(self):
        result = ParagraphBuilder("test").list().build()

        self.assertEqual(result, "[P#L#test]")

    def test_combination(self):
        result = ParagraphBuilder("test").heading().center().list().build()

        all_correct = [
            f"[P#{",".join(e)}#test]"
            for e in itertools.permutations(["H1", "center", "L"], 3)
        ]

        self.assertIn(result, all_correct)

    def test_font(self):
        result = ParagraphBuilder(FontBuilder("test").bold()).heading().build()

        self.assertEqual(result, "[P#H1#[T#B#test]]")

    def test_cloze(self):
        result = ParagraphBuilder(ClozeBuilder("test", 1)).heading().build()

        self.assertEqual(result, "[P#H1#[F#1#test]]")

    async def test_audio(self):
        auth = Auth(ENV.username, ENV.password)
        token = await auth.login()
        client = Markji(token)

        word = "test"
        audio = await client.tts(word, LanguageCode.EN_US)

        result = ParagraphBuilder(AudioBuilder(audio.id, word)).heading().build()

        self.assertEqual(result, f"[P#H1#[Audio#A,ID/{audio.id}#test]]")

    async def test_reference(self):
        auth = Auth(ENV.username, ENV.password)
        token = await auth.login()
        client = Markji(token)

        word = "test"
        cards, _ = await client.search_cards(word, self_only=False)

        result = ParagraphBuilder(ReferenceBuilder(word, cards[0])).heading().build()

        self.assertEqual(result, f"[P#H1#[Card#ID/{cards[0].root_id}#test]]")


class TestCloze(unittest.TestCase):
    def test(self):
        result = ClozeBuilder("test").build()

        self.assertEqual(result, "[F#1#test]")

        with self.assertRaises(ValueError):
            ClozeBuilder("test", 0)


if __name__ == "__main__":
    unittest.main()

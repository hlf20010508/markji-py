# :project: markji-py
# :author: L-ING
# :copyright: (C) 2025 L-ING <hlf01@icloud.com>
# :license: MIT, see LICENSE for more details.

import unittest
import itertools
from markji.editor import (
    AnswerLine,
    FontBackgroundColor,
    FontBuilder,
    FontColor,
    FontScript,
)


class TestAnswerLine(unittest.TestCase):
    def test(self):
        self.assertEqual(AnswerLine, "---")


class TestFont(unittest.TestCase):
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


if __name__ == "__main__":
    unittest.main()

# :project: markji-py
# :author: L-ING
# :copyright: (C) 2025 L-ING <hlf01@icloud.com>
# :license: MIT, see LICENSE for more details.

from markji.editor.choice import ChoiceBuilder, ChoiceItem
from markji.editor.cloze import ClozeBuilder
from markji.editor.font import FontBackgroundColor, FontBuilder, FontColor, FontScript
from markji.editor.formula import FormulaBuilder
from markji.editor.media import AudioBuilder, ImageBuilder
from markji.editor.paragraph import ParagraphBuilder
from markji.editor.reference import ReferenceBuilder

AnswerLine = "---"
"""答案分割线"""

__all__ = [
    "FontBuilder",
    "FontColor",
    "FontBackgroundColor",
    "FontScript",
    "ParagraphBuilder",
    "ClozeBuilder",
    "ChoiceBuilder",
    "ChoiceItem",
    "FormulaBuilder",
    "ReferenceBuilder",
    "ImageBuilder",
    "AudioBuilder",
    "AnswerLine",
]

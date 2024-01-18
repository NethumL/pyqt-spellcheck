from __future__ import annotations

import re
from typing import TYPE_CHECKING

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QSyntaxHighlighter, QTextCharFormat

if TYPE_CHECKING:
    from pyqt_spellcheck.spellcheckwrapper import SpellCheckWrapper


class SpellCheckHighlighter(QSyntaxHighlighter):
    """Highlighter for spell checking in Qt."""

    wordRegEx = re.compile(r"\b([A-Za-z]{2,})\b")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.speller: SpellCheckWrapper | None = None

        self.misspelledFormat = QTextCharFormat()
        self.misspelledFormat.setUnderlineStyle(QTextCharFormat.SpellCheckUnderline)
        self.misspelledFormat.setUnderlineColor(Qt.GlobalColor.red)

    def highlightBlock(self, text: str | None) -> None:
        if self.speller is None:
            return
        if text is None:
            return

        for word_object in self.wordRegEx.finditer(text):
            if not self.speller.check(word_object.group()):
                self.setFormat(
                    word_object.start(),
                    word_object.end() - word_object.start(),
                    self.misspelledFormat,
                )

    def setSpeller(self, speller: SpellCheckWrapper):
        self.speller = speller

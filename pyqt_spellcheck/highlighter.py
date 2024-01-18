import re

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QSyntaxHighlighter, QTextCharFormat

from pyqt_spellcheck.spellcheckwrapper import SpellCheckWrapper


class SpellCheckHighlighter(QSyntaxHighlighter):
    wordRegEx = re.compile(r"\b([A-Za-z]{2,})\b")

    def highlightBlock(self, text: str | None) -> None:
        if not hasattr(self, "speller"):
            return
        if text is None:
            return

        self.misspelledFormat = QTextCharFormat()
        self.misspelledFormat.setUnderlineStyle(QTextCharFormat.SpellCheckUnderline)
        self.misspelledFormat.setUnderlineColor(Qt.GlobalColor.red)

        for word_object in self.wordRegEx.finditer(text):
            if not self.speller.check(word_object.group()):
                self.setFormat(
                    word_object.start(),
                    word_object.end() - word_object.start(),
                    self.misspelledFormat,
                )

    def setSpeller(self, speller: SpellCheckWrapper):
        self.speller = speller

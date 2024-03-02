from __future__ import annotations

from PyQt5.QtCore import QEvent, Qt, pyqtSlot
from PyQt5.QtGui import QContextMenuEvent, QMouseEvent
from PyQt5.QtWidgets import QLineEdit, QMenu

from pyqt_spellcheck import util
from pyqt_spellcheck.correction_action import CorrectionAction
from pyqt_spellcheck.spellcheckwrapper import SpellCheckWrapper


class SpellLineEdit(QLineEdit):
    """QLineEdit widget with spell checking."""

    def __init__(self, *args):
        if args and isinstance(args[0], SpellCheckWrapper):
            super().__init__(*args[1:])
            self.speller = args[0]
        else:
            super().__init__(*args)

    def setSpeller(self, speller: SpellCheckWrapper):
        self.speller = speller

    def mousePressEvent(self, event: QMouseEvent | None) -> None:
        if event is None:
            return

        if event.button() == Qt.MouseButton.RightButton:
            event = QMouseEvent(
                QEvent.Type.MouseButtonPress,
                event.pos(),
                Qt.MouseButton.LeftButton,
                Qt.MouseButton.LeftButton,
                Qt.KeyboardModifier.NoModifier,
            )
        super().mousePressEvent(event)

    def contextMenuEvent(self, event: QContextMenuEvent | None) -> None:
        if event is None:
            return

        self.contextMenu = self.createStandardContextMenu()
        if self.contextMenu is None:
            return

        # Select word under cursor
        currentPosition = self.cursorPosition()
        currentText = self.text()
        bounds = util.find_word_bounds(currentText, currentPosition)
        wordToCheck = currentText[bounds[0] : bounds[1]]
        self.setSelection(bounds[0], len(wordToCheck))

        if wordToCheck != "":
            suggestions = self.speller.suggestions(wordToCheck)

            if len(suggestions) > 0:
                self.contextMenu.addSeparator()
                self.contextMenu.addMenu(self.createSuggestionsMenu(suggestions))

            if not self.speller.check(wordToCheck):
                addToDictionary_action = CorrectionAction(
                    "Add to dictionary",
                    self.contextMenu,
                )
                addToDictionary_action.triggered.connect(self.addToDictionary)
                self.contextMenu.addAction(addToDictionary_action)

        self.contextMenu.exec_(event.globalPos())

    def createSuggestionsMenu(self, suggestions: list[str]) -> QMenu:
        suggestionsMenu = QMenu("Change to", self)
        for word in suggestions:
            action = CorrectionAction(word, self.contextMenu)
            action.actionTriggered.connect(self.correctWord)
            suggestionsMenu.addAction(action)

        return suggestionsMenu

    @pyqtSlot(str)
    def correctWord(self, word: str) -> None:
        """Replace the currently selected word with the given word."""
        bounds = (self.selectionStart(), self.selectionEnd())
        self.setSelection(bounds[0], bounds[1] - bounds[0])
        self.insert(word)
        self.setSelection(bounds[0], len(word))

    @pyqtSlot()
    def addToDictionary(self):
        currentPosition = self.cursorPosition()
        currentText = self.text()
        bounds = util.find_word_bounds(currentText, currentPosition)
        newWord = currentText[bounds[0] : bounds[1]]
        self.speller.add(newWord)

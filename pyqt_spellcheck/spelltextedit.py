from PyQt5.QtCore import QEvent, Qt, pyqtSlot
from PyQt5.QtGui import QContextMenuEvent, QMouseEvent, QTextCursor
from PyQt5.QtWidgets import QMenu, QTextEdit

from pyqt_spellcheck.correction_action import SpecialAction
from pyqt_spellcheck.highlighter import SpellCheckHighlighter
from pyqt_spellcheck.spellcheckwrapper import SpellCheckWrapper


class SpellTextEdit(QTextEdit):
    def __init__(self, *args):
        if args and type(args[0]) == SpellCheckWrapper:
            super().__init__(*args[1:])
            self.speller = args[0]
        else:
            super().__init__(*args)

        self.highlighter = SpellCheckHighlighter(self.document())
        if hasattr(self, "speller"):
            self.highlighter.setSpeller(self.speller)

    def setSpeller(self, speller):
        self.speller = speller
        self.highlighter.setSpeller(self.speller)

    def mousePressEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.RightButton:
            event = QMouseEvent(
                QEvent.MouseButtonPress,
                event.pos(),
                Qt.LeftButton,
                Qt.LeftButton,
                Qt.NoModifier,
            )
        super().mousePressEvent(event)

    def contextMenuEvent(self, event: QContextMenuEvent) -> None:
        self.contextMenu = self.createStandardContextMenu(event.pos())

        textCursor = self.textCursor()
        textCursor.select(QTextCursor.WordUnderCursor)
        self.setTextCursor(textCursor)
        wordToCheck = textCursor.selectedText()
        if wordToCheck != "":
            suggestions = self.speller.suggestions(wordToCheck)

            if len(suggestions) > 0:
                self.contextMenu.addSeparator()
                self.contextMenu.addMenu(self.createSuggestionsMenu(suggestions))
            if not self.speller.check(wordToCheck):
                addToDictionary_action = SpecialAction(
                    "Add to dictionary", self.contextMenu
                )
                addToDictionary_action.triggered.connect(self.addToDictionary)
                self.contextMenu.addAction(addToDictionary_action)

        self.contextMenu.exec_(event.globalPos())

    def createSuggestionsMenu(self, suggestions: list[str]):
        suggestionsMenu = QMenu("Change to", self)
        for word in suggestions:
            action = SpecialAction(word, self.contextMenu)
            action.actionTriggered.connect(self.correctWord)
            suggestionsMenu.addAction(action)

        return suggestionsMenu

    @pyqtSlot(str)
    def correctWord(self, word: str):
        textCursor = self.textCursor()
        textCursor.beginEditBlock()
        textCursor.removeSelectedText()
        textCursor.insertText(word)
        textCursor.endEditBlock()

    @pyqtSlot()
    def addToDictionary(self):
        textCursor = self.textCursor()
        new_word = textCursor.selectedText()
        self.speller.add(new_word)
        self.highlighter.rehighlight()

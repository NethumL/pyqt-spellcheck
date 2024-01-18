from collections.abc import Callable

from enchant import DictWithPWL
from PyQt5.QtCore import QTemporaryFile


class SpellCheckWrapper:
    """Wrapper for enchant spell checking library."""

    def __init__(
        self,
        personal_word_list: list[str],
        addToDictionary: Callable[[str], None],
    ):
        # Creating temporary file
        self.file = QTemporaryFile()
        self.file.open()
        self.dictionary = DictWithPWL(
            "en_US",
            self.file.fileName(),
        )

        self.addToDictionary = addToDictionary

        self.word_list = set(personal_word_list)
        self.load_words()

    def load_words(self):
        for word in self.word_list:
            self.dictionary.add(word)

    def suggestions(self, word: str) -> list[str]:
        return self.dictionary.suggest(word)

    def correction(self, word: str) -> str:
        return self.dictionary.suggest(word)[0]

    def add(self, new_word: str) -> bool:
        if self.check(new_word):
            return False
        self.word_list.add(new_word)
        self.addToDictionary(new_word)
        self.dictionary.add(new_word)
        return True

    def check(self, word: str) -> bool:
        return self.dictionary.check(word)

    def getNewWords(self) -> set[str]:
        return self.word_list

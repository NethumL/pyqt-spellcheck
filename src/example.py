import sys
from typing import List

from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget

from spellcheckwrapper import SpellCheckWrapper
from spelltextedit import SpellTextEdit


class Ui_MainWindow(QMainWindow):
    def __init__(self, word_list_path: str):
        super().__init__()
        self.word_list_path = word_list_path
        self.speller = SpellCheckWrapper(self.getWords(), self.addToDictionary)
        self.setupUi()

    def setupUi(self):
        self.resize(500, 500)
        self.setWindowTitle("Example app")

        self.centralWidget = QWidget(self)
        self.setCentralWidget(self.centralWidget)

        self.layout = QVBoxLayout(self.centralWidget)
        self.centralWidget.setLayout(self.layout)

        self.textEdit1 = SpellTextEdit(self.speller, self.centralWidget)
        self.layout.addWidget(self.textEdit1)

        self.textEdit2 = SpellTextEdit(self.speller, self.centralWidget)
        self.layout.addWidget(self.textEdit2)

    def getWords(self) -> List[str]:
        with open(self.word_list_path, "r") as f:
            word_list = [line.strip() for line in f]
        return word_list

    def addToDictionary(self, new_word: str):
        with open(self.word_list_path, "a") as f:
            f.write("\n" + new_word)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Ui_MainWindow("example_word_list.txt")
    window.show()
    sys.exit(app.exec_())

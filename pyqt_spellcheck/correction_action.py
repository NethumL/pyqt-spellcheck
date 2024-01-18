from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QAction


class CorrectionAction(QAction):
    """Custom QAction for correcting spelling."""

    actionTriggered = pyqtSignal(str)

    def __init__(self, *args):
        super().__init__(*args)

        self.triggered.connect(self.emitTriggered)

    def emitTriggered(self):
        self.actionTriggered.emit(self.text())

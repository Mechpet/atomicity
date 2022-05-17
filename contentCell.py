import sys

from PyQt6.QtWidgets import QWidget, QTextEdit

class contentCell(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()


    def initUI(self):
        self.setMinimumSize(30, 30)
        self.text = "Wake up"
        te = QTextEdit()
    
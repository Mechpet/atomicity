import sys

from PyQt6.QtWidgets import QWidget, QTextEdit, QPushButton
from PyQt6.QtGui import QPainter, QColor

class contentCell(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()


    def initUI(self):
        self.setMinimumSize(30, 30)
        self.text = "Wake up"
        color = QColor(0, 0, 0)
        qp = QPainter()
        qp.begin(self)
        
        button = QPushButton(self.text, self)
        self.show()
    
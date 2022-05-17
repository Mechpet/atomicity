import sys

from PyQt6.QtWidgets import QHBoxLayout, QWidget, QPushButton, QApplication
from contentCell import contentCell

class contentRow(QWidget):
    def __init__(self):
        super().__init__()

        layout = QHBoxLayout()
        layout.addWidget(contentCell())
        layout.addWidget(contentCell())
        layout.addWidget(contentCell())

        self.setLayout(layout)
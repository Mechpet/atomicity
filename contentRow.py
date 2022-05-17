import sys

from PyQt6.QtWidgets import QHBoxLayout, QWidget, QPushButton, QApplication
from contentHead import contentHead

class contentRow(QWidget):
    def __init__(self):
        super().__init__()

        layout = QHBoxLayout()
        layout.addWidget(contentHead())
        layout.addWidget(contentHead())
        layout.addWidget(contentHead())
        layout.addWidget(contentHead())

        self.setLayout(layout)
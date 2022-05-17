import sys

from PyQt6.QtWidgets import QHBoxLayout, QWidget, QPushButton, QApplication

class contentRow(QWidget):
    def __init__(self):
        super().__init__()

        layout = QHBoxLayout()
        layout.addWidget(QPushButton("Left-most"))
        layout.addWidget(QPushButton("Center"))
        layout.addWidget(QPushButton("Right-most"))

        self.setLayout(layout)
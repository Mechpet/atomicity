# The main window of the application 
import sys

from PyQt6.QtWidgets import QApplication, QWidget, QTextEdit, QPushButton, QHBoxLayout, QVBoxLayout
from contentRow import *

class mainWrapper(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        hbox = QHBoxLayout()
        hbox.addWidget(contentRow())
        vbox = QVBoxLayout()
        vbox.addLayout(hbox)

        self.setLayout(vbox)

        self.setGeometry(300, 300, 650, 550)
        self.setWindowTitle('Atomicity')
        self.show()

def main():
    app = QApplication(sys.argv)

    window = mainWrapper()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
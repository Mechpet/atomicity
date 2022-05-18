# The main window of the application 
import sys
import ctypes

from PyQt6.QtWidgets import QApplication, QWidget, QTextEdit, QPushButton, QHBoxLayout, QVBoxLayout
from PyQt6.QtGui import QIcon
from contentRow import *
from window import *

class mainWrapper(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        """Initialize the interface"""
        # Set the window icon and taskbar icon
        self.setWindowIcon(QIcon(r"images\icon3_trans.png"))
        self.setWindowTitle('Atomicity')
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(APP_ID)

        hbox = QHBoxLayout()
        hbox.addWidget(contentRow())
        vbox = QVBoxLayout()
        vbox.addLayout(hbox)

        self.setLayout(vbox)

        self.setGeometry(300, 300, 650, 550)
        self.show()

def main():
    app = QApplication(sys.argv)

    window = mainWrapper()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
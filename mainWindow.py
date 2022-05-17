# The main window of the application 
import sys
import ctypes

from PyQt6.QtWidgets import QApplication, QWidget, QTextEdit, QPushButton, QHBoxLayout, QVBoxLayout
from contentRow import *
from PyQt6.QtGui import QIcon

class mainWrapper(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        # Set the window icon and taskbar icon
        self.setWindowIcon(QIcon(r"images\icon3_trans.png"))
        self.setWindowTitle('Atomicity')
        appid = "Atomicity-prgm"
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(appid)

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
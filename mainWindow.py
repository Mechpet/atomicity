# The main window of the application 
import sys
import ctypes

from PyQt6.QtWidgets import QApplication, QWidget, QTextEdit, QPushButton, QHBoxLayout, QVBoxLayout
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt
from contentRow import contentRow
from window import Window, APP_ID
from dateColumn import dateColumn
from contentAdder import contentAdder
from contentCell import contentCell

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

        hboxTop = QHBoxLayout()
        hboxTop.addWidget(contentAdder(), 0, Qt.AlignmentFlag.AlignCenter)
        hboxTop.addWidget(contentRow(3), 1, Qt.AlignmentFlag.AlignLeft)
        vbox = QVBoxLayout()
        vbox.addLayout(hboxTop)
        hboxBot = QHBoxLayout()
        hboxBot.addWidget(dateColumn(), 0, Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        hboxBot.addWidget(contentCell(), 1, Qt.AlignmentFlag.AlignLeft)
        vbox.addLayout(hboxBot)

        self.setLayout(vbox)

        self.setGeometry(300, 300, 650, 550)
        self.show()

def main():
    app = QApplication(sys.argv)

    window = mainWrapper()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
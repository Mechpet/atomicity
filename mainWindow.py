# The main window of the application 
import sys
import ctypes

from PyQt6.QtWidgets import QApplication, QWidget, QScrollArea, QGridLayout
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt, QSettings
from contentColumn import contentColumn
from contentRow import contentRow
from window import Window, APP_ID
from dateColumn import dateColumn
from contentAdder import contentAdder
from contentCell import cellType
from contentGrid import contentGrid

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

        self.adder = contentAdder()
        self.adder.added.connect(self.addHeader)

        self.contentRow = contentRow()

        self.dateColumn = dateColumn()

        self.contentGrid = contentGrid(cellType.binary)

        self.layout = QGridLayout()
        self.layout.addWidget(self.adder, 0, 0, 1, 1, Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        self.layout.addWidget(self.contentRow, 0, 1, 1, 3)#, Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        #self.layout.addWidget(self.dateColumn, 1, 0, 3, 1, Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        #self.layout.addWidget(self.contentGrid, 1, 1, 3, 1, Qt.AlignmentFlag.AlignLeft)

        self.setLayout(self.layout)

        # Useful scroll methods:
        #scroll = QScrollArea()
        #scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        #scroll.verticalScrollBar().setDisabled(True)
        #scroll.setStyleSheet("""
        #    QScrollBar:horizontal {
        #        background: blue;
        #    }
        #""")

        self.setGeometry(300, 300, 650, 550)
        self.show()

    def addHeader(self):
        self.contentRow.addHeader()
        

def main():
    app = QApplication(sys.argv)

    window = mainWrapper()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
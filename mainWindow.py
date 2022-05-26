# The main window of the application 
import sys
import ctypes

from PyQt6.QtWidgets import QApplication, QWidget, QScrollArea, QGridLayout, QSizePolicy, QPushButton
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt, QSettings, QDate
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

        self.testExpand()
        #self.initUI()

    def testExpand(self):
        self.dateColumn = dateColumn()
        self.scroll1 = QScrollArea()
        self.scroll1.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll1.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll1.horizontalScrollBar().setDisabled(True)
        self.scroll1.setWidget(self.dateColumn)
        self.scroll1.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        self.layout = QGridLayout()
        self.layout.addWidget(self.scroll1, 0, 0, -1, 1)
        self.layout.setRowStretch(0, 10)
        self.setLayout(self.layout)
        self.show()

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
        self.layout.addWidget(self.contentRow, 0, 1, 1, 3)
        scroll1 = QScrollArea()
        scroll1.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll1.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll1.horizontalScrollBar().setDisabled(True)
        scroll1.setWidget(self.dateColumn)
        self.layout.addWidget(scroll1, 1, 0, -1, 1, Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        scroll1.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        dateColumn2 = dateColumn(QDate(2020, 3, 20))
        scroll2 = QScrollArea()
        scroll2.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll2.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll2.horizontalScrollBar().setDisabled(True)
        scroll2.setWidget(dateColumn2)
        scroll2.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.layout.addWidget(scroll2, 1, 1, -1, 1, Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)

        self.layout.addWidget(QPushButton("Back to Top"), 2, 0, 1, 1)

        scroll1.verticalScrollBar().valueChanged.connect(scroll2.verticalScrollBar().setValue)
        scroll2.verticalScrollBar().valueChanged.connect(scroll1.verticalScrollBar().setValue)

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

    
    settings = QSettings("Mechpet", "Atomicity")
    settings.beginGroup("contentRow")

    settings.setValue("num", 0)

    window = mainWrapper()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
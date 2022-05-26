# The main window of the application 
import sys
import ctypes

from PyQt6.QtWidgets import QApplication, QWidget, QScrollArea, QGridLayout, QSizePolicy, QPushButton, QFrame, QLabel, QVBoxLayout
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

        #self.testExpand()

        self.initUI()

    def testExpand(self):
        self.dateColumn = dateColumn()
        self.self.dateScroll = QScrollArea()
        self.self.dateScroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.self.dateScroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.self.dateScroll.horizontalScrollBar().setDisabled(True)
        self.self.dateScroll.setWidget(self.dateColumn)
        self.self.dateScroll.setMaximumSize(self.dateColumn.width(), self.dateColumn.height())
        #self.self.dateScroll.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        self.layout = QGridLayout()
        self.layout.addWidget(self.self.dateScroll, 0, 0, -1, 1)
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

        vbox = QVBoxLayout()

        self.dateColumn = dateColumn()
        self.dateScroll = QScrollArea()
        self.dateScroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.dateScroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.dateScroll.horizontalScrollBar().setDisabled(True)
        self.dateScroll.setWidget(self.dateColumn)
        self.dateScroll.setMaximumSize(self.dateColumn.width(), self.dateColumn.height())
        self.dateScroll.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.dateScroll.setFrameShape(QFrame.Shape.NoFrame)

        self.dateEdit = QPushButton("Jump to date", self)
        self.dateEdit.clicked.connect(self.dateColumn.setDate)

        self.contentGrid = contentGrid(cellType.binary)

        vbox.addWidget(self.dateEdit)
        vbox.addWidget(self.dateScroll)

        self.layout = QGridLayout()
        
        self.layout.addWidget(self.adder, 0, 0, 1, 1, Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        self.layout.addWidget(self.contentRow, 0, 1, 1, 3)
        self.layout.addLayout(vbox, 1, 0, -1, 1)
        self.layout.addWidget(QLabel("Copyright", self), 6, 7, 1, 1)

        # Filler:
        dateColumn2 = dateColumn(QDate(2020, 3, 20))
        scroll2 = QScrollArea()
        scroll2.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll2.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll2.horizontalScrollBar().setDisabled(True)
        scroll2.setWidget(dateColumn2)
        scroll2.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.layout.addWidget(scroll2, 1, 1, -1, 1, Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)

        self.dateScroll.verticalScrollBar().valueChanged.connect(scroll2.verticalScrollBar().setValue)
        scroll2.verticalScrollBar().valueChanged.connect(self.dateScroll.verticalScrollBar().setValue)

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
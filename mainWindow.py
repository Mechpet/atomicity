# The main window of the application 
from cgitb import reset
import sys
import ctypes

from PyQt6.QtWidgets import QApplication, QWidget, QScrollArea, QGridLayout, QSizePolicy, QPushButton, QFrame, QLabel, QVBoxLayout
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt, QSettings, QDate
from contentRow import contentRow
from window import APP_ID
from dateColumn import dateColumn
from contentAdder import contentAdder
from contentCell import cellType
from binaryCell import binaryCell
from contentColumn import contentColumn
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

        # Initialize widgets
        self.adder = contentAdder()

        self.contentRow = contentRow()
        self.contentRowScroll = QScrollArea()
        self.contentRowScroll.setWidgetResizable(True)
        self.contentRowScroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.contentRowScroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.contentRowScroll.verticalScrollBar().setDisabled(True)
        self.contentRowScroll.setWidget(self.contentRow)
        self.contentRowScroll.setMaximumSize(self.contentRow.width(), self.contentRow.height())
        self.contentRowScroll.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.contentRowScroll.setFrameShape(QFrame.Shape.NoFrame)

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
        print(f"Height of dateEdit = {self.dateEdit.height()}")

        self.contentCol = contentColumn(cellType.binary)

        self.contentGridScroll = QScrollArea()
        self.contentGridScroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.contentGridScroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.contentGridScroll.horizontalScrollBar().setDisabled(True)
        self.contentGridScroll.setWidget(self.contentCol)
        self.contentGridScroll.setMaximumSize(self.contentCol.width(), self.contentCol.height())
        self.contentGridScroll.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.contentGridScroll.setFrameShape(QFrame.Shape.NoFrame)

        emptyBtn = QPushButton("", self)
        emptyBtn.setStyleSheet("""
            QPushButton {
                border: 0px;
                background: transparent;
            }
        """)

        # Connect widgets
        self.adder.added.connect(self.contentRow.addHeader)
        self.dateEdit.clicked.connect(self.dateColumn.setDate)

        # Layout the widgets
        dateVbox = QVBoxLayout()
        dateVbox.addWidget(self.dateEdit)
        dateVbox.addWidget(self.dateScroll)

        colVbox = QVBoxLayout()
        colVbox.addWidget(emptyBtn)
        colVbox.addWidget(self.contentGridScroll)

        self.layout = QGridLayout()
        
        self.layout.addWidget(self.adder, 0, 0, 1, 1, Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        self.layout.addWidget(self.contentRowScroll, 0, 1, 1, 10)
        self.layout.addLayout(dateVbox, 1, 0, -1, 1)
        self.layout.addLayout(colVbox, 1, 1, -1, 1)
        self.layout.addWidget(QLabel("COPYRIGHT", self), 8, 9, 1, 1)

        self.dateScroll.verticalScrollBar().valueChanged.connect(self.contentGridScroll.verticalScrollBar().setValue)
        self.contentGridScroll.verticalScrollBar().valueChanged.connect(self.dateScroll.verticalScrollBar().setValue)

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

def main():
    app = QApplication(sys.argv)

    window = mainWrapper()
    #resetContentHeads()

    sys.exit(app.exec())

def resetContentHeads():
    settings = QSettings("Mechpet", "Atomicity")
    settings.beginGroup("contentRow")

    settings.setValue("num", 0)
    quit()

if __name__ == "__main__":
    main()
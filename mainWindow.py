# The main window of the application 
from cgitb import reset
import sys
import ctypes

from PyQt6.QtWidgets import QApplication, QWidget, QScrollArea, QGridLayout, QSizePolicy, QPushButton, QFrame, QVBoxLayout
from PyQt6.QtGui import QIcon, QCursor
from PyQt6.QtCore import Qt, QSettings
from headList import headList, headListScroll
from window import APP_ID
from dateList import dateList
from headAdder import headAdder
from cellGrid import cellGrid

app = QApplication(sys.argv)

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

        self.layout = QGridLayout()

        # Initialize widgets
        self.adder = headAdder()

        self.headList = headList()
        self.headListScroll = headListScroll()
        self.headListScroll.installWidget(self.headList)
        print("Head list scroll height = ", self.headListScroll.height())

        self.dateList = dateList()
        self.dateScroll = QScrollArea()
        #self.dateScroll.setWidgetResizable(True)
        self.dateScroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        #self.dateScroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.dateScroll.verticalScrollBar().setDisabled(True)
        self.dateScroll.setWidget(self.dateList)
        #self.dateScroll.setMaximumSize(self.dateList.width(), self.dateList.height())
        self.dateScroll.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.dateScroll.setFrameShape(QFrame.Shape.NoFrame)

        self.dateEdit = QPushButton("Jump to date", self)

        self.cellGrid = cellGrid(self.dateList.topDate)

        self.cellGridScroll = QScrollArea()
        self.cellGridScroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.cellGridScroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.cellGridScroll.setWidget(self.cellGrid)
        self.cellGridScroll.setMaximumSize(self.cellGrid.width(), self.cellGrid.height())
        self.cellGridScroll.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.cellGridScroll.setFrameShape(QFrame.Shape.NoFrame)

        emptyBtn = QPushButton("", self)
        emptyBtn.setStyleSheet("""
            QPushButton {
                border: 0px;
                background: transparent;
            }
        """)

        # Connect widgets
        self.adder.added.connect(self.headList.addHeader)
        self.dateEdit.clicked.connect(self.dateList.setDate)
        self.dateList.topDateChanged.connect(self.cellGrid.updateGrid)
        self.headList.append.connect(self.cellGrid.showCellsAt)

        # Layout the widgets
        dateVbox = QVBoxLayout()
        dateVbox.addWidget(self.dateEdit)
        dateVbox.addWidget(self.dateScroll)
        
        self.layout.addWidget(self.adder, 0, 0, 1, 1)
        self.layout.addLayout(dateVbox, 0, 1, 1, 20, Qt.AlignmentFlag.AlignLeft)
        #self.layout.setColumnStretch(1, 1)
        self.layout.addWidget(self.headListScroll, 1, 0, -1, 1)
        self.layout.addWidget(self.cellGridScroll, 1, 1, -1, 20, Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)

        # Connect related scroll areas
        self.dateScroll.horizontalScrollBar().valueChanged.connect(self.cellGridScroll.horizontalScrollBar().setValue)
        self.cellGridScroll.horizontalScrollBar().valueChanged.connect(self.dateScroll.horizontalScrollBar().setValue)
        self.headListScroll.verticalScrollBar().valueChanged.connect(self.cellGridScroll.verticalScrollBar().setValue)
        self.cellGridScroll.verticalScrollBar().valueChanged.connect(self.headListScroll.verticalScrollBar().setValue)

        self.setLayout(self.layout)

        self.setGeometry(300, 300, 650, 550)
        self.show()

def main():
    #resetContentHeads()
    window = mainWrapper()

    sys.exit(app.exec())

def resetContentHeads():
    settings = QSettings("Mechpet", "Atomicity")
    settings.beginGroup("headList")

    settings.setValue("num", 0)
    quit()

def setHorScroll():
    app.setOverrideCursor(QCursor(Qt.CursorShape.SizeHorCursor))

if __name__ == "__main__":
    main()
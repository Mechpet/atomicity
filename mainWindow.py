# The main window of the application
import sys
import ctypes
from types import CellType

from PyQt6.QtWidgets import QApplication, QWidget, QTabWidget, QGridLayout, QSizePolicy, QPushButton, QFrame, QVBoxLayout, QLabel, QMenu
from PyQt6.QtGui import QColor, QCursor
from PyQt6.QtCore import Qt, QSettings

from headList import headList, headListScroll
from window import APP_ID
from dateList import dateList
from headAdder import headAdder
from contentHead import contentHead
from contentCell import cellType
from cellList import cellList
from cellGrid import cellGrid
from statistics import statisticsWidget
from window import Window
from scroll import scroll
from preferences import preferences

app = QApplication(sys.argv)

class mainWrapper(Window):
    def __init__(self):
        super().__init__('Atomicity', 300, 300, 650, 550)

        self.initWidgets()

    def initWidgets(self):
        """Initialize the interface"""
        self.layout = QGridLayout()

        # Initialize child widgets
        self.adder = headAdder()

        self.headList = headList()
        self.headListScroll = headListScroll()
        self.headListScroll.installWidget(self.headList)
        self.headListScroll.installMouseEvents()

        self.dateList = dateList()
        self.dateScroll = scroll()
        self.dateScroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.dateScroll.verticalScrollBar().setDisabled(True)
        self.dateScroll.setWidget(self.dateList)
        self.dateScroll.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.dateScroll.setFrameShape(QFrame.Shape.NoFrame)

        self.dateEdit = QPushButton("Jump to date", self)

        self.cellGrid = cellGrid(self.dateList.topDate)

        self.cellGridScroll = scroll()
        self.cellGridScroll.setWidgetResizable(False)
        self.cellGridScroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.cellGridScroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.cellGridScroll.setWidget(self.cellGrid)
        self.cellGridScroll.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.MinimumExpanding)
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
        self.headList.deleteRow.connect(self.cellGrid.deleteRowAt)
        self.headList.rearrangeRow.connect(self.cellGrid.rearrangeRows)

        # Layout the widgets
        dateVbox = QVBoxLayout()
        dateVbox.addWidget(self.dateEdit)
        dateVbox.addWidget(self.dateScroll)

        self.dailyLabel = QLabel("DAILY")
        self.dailyLabel.setFixedSize(200, 200)

        self.daily = cellList(cellType.benchmark)
        self.dailyScroll = scroll()
        self.dailyScroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.dailyScroll.verticalScrollBar().setDisabled(True)
        self.dailyScroll.setWidget(self.daily)
        self.dailyScroll.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.dailyScroll.setFrameShape(QFrame.Shape.NoFrame)
        
        self.layout.addWidget(self.adder, 0, 0, 1, 1)
        self.layout.addLayout(dateVbox, 0, 1, 1, -1, Qt.AlignmentFlag.AlignLeft)
        self.layout.addWidget(self.headListScroll, 1, 0, -1, 1)
        self.layout.addWidget(self.cellGridScroll, 1, 1, -1, -1)

        # Connect related scroll areas
        self.dateScroll.horizontalScrollBar().valueChanged.connect(self.cellGridScroll.horizontalScrollBar().setValue)
        self.cellGridScroll.horizontalScrollBar().valueChanged.connect(self.dateScroll.horizontalScrollBar().setValue)
        self.headListScroll.verticalScrollBar().valueChanged.connect(self.cellGridScroll.verticalScrollBar().setValue)
        self.cellGridScroll.verticalScrollBar().valueChanged.connect(self.headListScroll.verticalScrollBar().setValue)

        # Initialize the tab widgets 
        self.tabs = QTabWidget()
        self.tracker = QWidget()
        self.tracker.setLayout(self.layout)
        self.stats = statisticsWidget()

        # Set the tabs 
        self.tabs.addTab(self.tracker, "Tracker")
        self.tabs.addTab(self.stats, "Stats")
        self.tabs.currentChanged.connect(self.updateTabViewport)
        self.setCentralWidget(self.tabs)

        # Set the menubar
        menubar = self.menuBar()
        preferences = menubar.addAction("Preferences")
        preferences.triggered.connect(self.openPreferences)

        self.show()

    def updateTabViewport(self, index):
        if index == 1:
            self.stats.initUI(self.headListScroll)
            self.stats.listWidget.uninstallMouseEvents()
        elif index == 0:
            self.layout.addWidget(self.headListScroll, 1, 0, -1, 1)

    def openPreferences(self):
        self.pref = preferences()
        self.pref.show()


def main():
    #resetContentHeads()
    initPreferences()
    window = mainWrapper()

    sys.exit(app.exec())

def resetContentHeads():
    settings = QSettings("Mechpet", "Atomicity")
    settings.beginGroup("headList")

    settings.setValue("num", 0)
    settings.endGroup()
    quit()

def initPreferences():
    settings = QSettings("Mechpet", "Atomicity")
    settings.beginGroup("global")

    if settings.value("cellColor") is None:
        settings.setValue("cellColor", QColor(55, 55, 55))
        settings.setValue("textColor", QColor(0, 0, 0))

def setHorScroll():
    app.setOverrideCursor(QCursor(Qt.CursorShape.SizeHorCursor))

if __name__ == "__main__":
    main()
    
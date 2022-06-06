from PyQt6.QtWidgets import QHBoxLayout, QVBoxLayout, QWidget
from PyQt6.QtCore import QSettings, QDate
import sqliteHelper as sql
from contentCell import cellType
from cellList import cellList

DEFAULT_NUM_COLUMNS = 14
# Layout of contentCells in a vertical column
class cellGrid(QWidget):
    """A grid of contentColumns."""
    def __init__(self, topDate):
        super().__init__()

        self.topDate = topDate
        self.layout = QVBoxLayout()

        self.showAllCells()

        self.setLayout(self.layout)

    def showAllCells(self):
        """Display all cells"""
        settings = QSettings("Mechpet", "Atomicity")
        settings.beginGroup("headList")
        for i in range(settings.value("num")):
            self.showCellsAt(i)

    def showCellsAt(self, i):
        """Display cells matching the one at the given index"""
        settingName = f"contentHead{i}.ini"
        settings = QSettings(settingName, QSettings.Format.IniFormat)

        tableName = settings.value("table")
        newList = cellList(cellType.binary, tableName, self.topDate)
        self.layout.addWidget(newList)

    def updateGrid(self, newDate):
        self.topDate = newDate

        return
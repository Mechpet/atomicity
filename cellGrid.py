from re import L
from PyQt6.QtWidgets import QHBoxLayout, QVBoxLayout, QWidget, QLayout
from PyQt6.QtCore import QSettings, QDate
import sqliteHelper as sql
from contentCell import cellType
from cellList import cellList

from timeit import default_timer as timer

DEFAULT_NUM_COLUMNS = 14
# Layout of contentCells in a vertical column
class cellGrid(QWidget):
    """A grid of contentColumns."""
    def __init__(self, topDate):
        super().__init__()

        self.topDate = topDate
        self.setMinimumHeight(100)
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSizeConstraint(QLayout.SizeConstraint.SetMinAndMaxSize)

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
        newList = cellList(settings.value("type"), tableName, self.topDate, settings)
        self.layout.addWidget(newList)

    def deleteRowAt(self, index):
        self.layout.itemAt(index).widget().close()
        self.layout.removeWidget(self.layout.itemAt(index).widget())

    def rearrangeRows(self, selectedIndex, targetIndex):
        deletedRow = self.layout.itemAt(selectedIndex).widget()
        self.layout.removeWidget(deletedRow)
        self.layout.insertWidget(targetIndex, deletedRow)

    def updateGrid(self, newDate):
        self.topDate = newDate

        # Update all lists:
        for i in range(self.layout.count()):
            print("UPDATE")
            self.layout.itemAt(i).widget().updateUI(newDate)

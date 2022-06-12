from re import L
from PyQt6.QtWidgets import QHBoxLayout, QVBoxLayout, QWidget
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
        self.layout = QVBoxLayout()

        self.showAllCells()

        self.setLayout(self.layout)

    def showAllCells(self):
        """Display all cells"""
        settings = QSettings("Mechpet", "Atomicity")
        settings.beginGroup("headList")
        for i in range(settings.value("num")):
            self.showCellsAt(i)

    def showCellsAt(self, i, cellType = cellType.binary):
        """Display cells matching the one at the given index"""
        settingName = f"contentHead{i}.ini"
        settings = QSettings(settingName, QSettings.Format.IniFormat)

        tableName = settings.value("table")
        newList = cellList(cellType, tableName, self.topDate)
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

        start = timer()

        # Remove all lists and then create new lists:
        #for i in range(self.layout.count() - 1, -1, -1):
        #    self.layout.removeWidget(self.layout.itemAt(i).widget())
        #self.showAllCells()

        # Update all lists:
        for i in range(self.layout.count()):
            self.layout.itemAt(i).widget().updateUI(newDate)

        end = timer()
        with open("updateGrid.txt", "a+") as file:
            file.write(f"Took {end - start} seconds")
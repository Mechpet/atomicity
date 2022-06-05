from PyQt6.QtWidgets import QHBoxLayout, QWidget
from PyQt6.QtCore import QSettings, QDate
import sqliteHelper
from contentCell import cellType
from contentColumn import contentColumn

DEFAULT_NUM_COLUMNS = 14
# Layout of contentCells in a vertical column
class contentGrid(QWidget):
    """A grid of contentColumns."""
    def __init__(self, topDate):
        super().__init__()

        #self.settings = QSettings("Mechpet", "Atomicity")
        #self.settings.beginGroup("contentRow")

        self.topDate = topDate
        self.layout = QHBoxLayout()
        #for i in range(int(self.settings.value("num"))):
        #    layout.addWidget(contentColumn(cellType.binary))

        #self.setLayout(layout)

    def showColumns(self):
        """Display all columns"""
        settings = QSettings("Mechpet", "Atomicity")
        settings.beginGroup("contentRow")
        for i in range(settings.value("num")):
            self.showColumn(i)

    def showColumn(self, i):
        """Display a column of fulfillment matching the one at the given index"""
        settingName = f"contentHead{i}.ini"
        settings = QSettings(settingName, QSettings.Format.IniFormat)

        tableName = settings.value("table")
        newColumn = contentColumn(cellType.binary, tableName, self.topDate)

    def updateGrid(self, newDate):
        self.topDate = newDate

        return
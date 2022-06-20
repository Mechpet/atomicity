from PyQt6.QtWidgets import QWidget, QGridLayout, QPushButton
from PyQt6.QtCore import Qt, QDate, QSettings, pyqtSlot
import pyqtgraph as pg

from contentHead import contentHead
import sqliteHelper as sql

class statisticsWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QGridLayout()
        self.plot = pg.plot()
        self.layout.addWidget(self.plot, 0, 1, -1, -1)
        self.setLayout(self.layout)

    def initUI(self, listWidget):
        self.listWidget = listWidget
        self.listWidget.checkStats.connect(self.showPlot)
        self.layout.addWidget(self.listWidget, 0, 0, -1, 1)

    @pyqtSlot(contentHead) # from a contentHead
    def showPlot(self, clickedWidget):
        """Clear the current plot's points and then draw the new plot"""
        # Fetch settings from .ini and SQLite
        tableName = clickedWidget.settings.value("table")
        today = QDate.currentDate()
        startDate = clickedWidget.settings.value("startDate")
        info = sql.fetchConsecutive(sql.connection, tableName, today.toString(Qt.DateFormat.ISODate), -1)
        info.reverse()

        # Plot data:
        # x = # of days since the startDay
        # y = value
        x = [i for i in range(startDate.daysTo(today) + 1)]
        y = [row[1] for row in info]

        self.plot.clear()
        line = pg.PlotDataItem(x, y, connect = "finite", pen = 'g', symbol = 'o', symbolPen = 'g', symbolBrush = 1.0, name = 'normal')
        self.plot.addItem(line)

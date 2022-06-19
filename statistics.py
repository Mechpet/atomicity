from PyQt6.QtWidgets import QWidget, QLabel, QGridLayout
from PyQt6.QtCore import Qt, QDate, QSettings
import pyqtgraph as pg
import sqliteHelper as sql

class statisticsWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        layout = QGridLayout()

        # Fetch settings from .ini and SQLite
        testSettingsName = "contentHead1.ini"
        self.settings = QSettings(testSettingsName, QSettings.Format.IniFormat)
        tableName = self.settings.value("table")
        today = QDate.currentDate()
        startDate = self.settings.value("startDate")
        info = sql.fetchConsecutive(sql.connection, tableName, today.toString(Qt.DateFormat.ISODate), -1)
        info.reverse()

        # Plot:
        plot = pg.plot()
        x = [i for i in range(startDate.daysTo(today) + 1)]
        y = [row[1] for row in info]

        line = pg.PlotDataItem(x, y, connect = "finite", pen = 'g', symbol = 'o', symbolPen = 'g', symbolBrush = 1.0, name = 'normal')
        plot.addItem(line)

        layout.addWidget(plot)

        self.setLayout(layout)


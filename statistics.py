from PyQt6.QtWidgets import QWidget, QLabel
from PyQt6.QtCore import Qt, QDate, QSettings
import pyqtgraph as pg
import sqliteHelper as sql

class statisticsWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        testSettingsName = "contentHead1.ini"
        self.settings = QSettings(testSettingsName, QSettings.Format.IniFormat)
        tableName = self.settings.value("table")
        today = QDate.currentDate()
        startDate = self.settings.value("startDate")
        info = sql.fetchConsecutive(sql.connection, tableName, today.toString(Qt.DateFormat.ISODate), -1)
        info.reverse()

        x = [i for i in range(startDate.daysTo(today) + 1)]
        y = [row[1] for row in info]

        print(f"x = {x}")
        print(f"y = {y}")

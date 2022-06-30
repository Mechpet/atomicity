from PyQt6.QtWidgets import QWidget, QGridLayout, QComboBox, QLabel
from PyQt6.QtCore import Qt, QDate, QSettings, pyqtSlot
import pyqtgraph as pg
import pandas as pd
import numpy as np
from enum import IntEnum
from itertools import cycle

from contentHead import contentHead
from contentCell import cellType
import sqliteHelper as sql

class plotModes(IntEnum):
    """Indices for the plotModeSelect items"""
    Value = 0
    Consecutive = 1
    Average = 2
    OnePercent = 3

class statisticsWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QGridLayout()
        self.plot = pg.plot()
        self.plotModeSelect = QComboBox()
        self.selectedDisplay = QLabel("")
        self.selectedDisplay.setFixedSize(200, 200)

        self.initPlotMode()
        self.layout.addWidget(self.plotModeSelect, 0, 2, 1, 1)
        self.layout.addWidget(self.selectedDisplay, 0, 1, Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.plot, 1, 1, -1, -1)
        self.setLayout(self.layout)

    def initUI(self, listWidget):
        self.listWidget = listWidget
        self.listWidget.checkStats.connect(self.showPlot)
        self.layout.addWidget(self.listWidget, 0, 0, -1, 1)

    def initPlotMode(self):
        """Initialize the QComboBox that holds the modes selectable"""
        plotModeHints = {
            plotModes.Value : "Raw user-input.",
            plotModes.Consecutive : "Consecutive days where the user-input meets the benchmark value.",
            plotModes.Average : "Cumulative average (all days leading up to) of the raw user-inputs.",
            plotModes.OnePercent : "Abstract percent where meeting/missing the benchmark value is a 1%% increase/decrease."
        }
        for enumItem in plotModes:
            self.plotModeSelect.insertItem(enumItem.value, enumItem.name)
            self.plotModeSelect.setItemData(enumItem.value, plotModeHints[enumItem], Qt.ItemDataRole.ToolTipRole)
        self.plotModeSelect.currentIndexChanged.connect(self.updatePlot)

    @pyqtSlot(contentHead) # from a contentHead
    def showPlot(self, clickedWidget):
        """Clear the current plot's points and then draw the new plot"""
        # Fetch settings from .ini and SQLite
        self.selectedDisplay.setPixmap(clickedWidget.grab())
        tableName = clickedWidget.settings.value("table")
        today = QDate.currentDate()
        startDate = clickedWidget.settings.value("startDate")
        info = sql.fetchConsecutive(sql.connection, tableName, today.toString(Qt.DateFormat.ISODate), -1)
        info.reverse()

        self.plot.clear()
        # Plot data:
        # x = # of days since the startDay
        # y = value
        x = [i for i in range(startDate.daysTo(today) + 1)]
        print("Length of x = ", len(x))

        currentMode = self.plotModeSelect.currentIndex()
        match currentMode:
            case plotModes.Value.value:
                y = [row[1] for row in info]
                self.plot.setLabel("left", "Value")
            case plotModes.Consecutive.value:
                ySeries = [row[1] for row in info]
                y = self.getChain(clickedWidget, ySeries)
            case plotModes.Average.value:
                ySeries = pd.Series([row[1] for row in info])
                y = ySeries.expanding().mean().to_list()
                self.plot.setLabel("left", "Average value")
            case plotModes.OnePercent.value:
                ySeries = [row[1] for row in info]
                y = self.onePercent(clickedWidget, ySeries)
        
        print("Info = ", info)
        print("Length of y = ", y)
        self.plot.setLabel("bottom", f"Days since {startDate.toString(Qt.DateFormat.ISODate)}")

        line = pg.PlotDataItem(x, y, connect = "finite", pen = 'g', symbol = 'o', symbolPen = 'g', symbolBrush = 1.0, name = 'normal')
        self.plot.addItem(line)

        if clickedWidget.settings.value("type") == cellType.binary:
            match currentMode:
                case plotModes.Value.value | plotModes.Average.value:
                    self.plot.getViewBox().setRange(xRange = (0, startDate.daysTo(today) + 1), yRange = (0, 1.5))
                    yAxis = self.plot.getAxis("left")
                    yAxis.setTicks([[(0, "0"), (1, "1")]])
                    return
        
        yAxis = self.plot.getAxis("left")
        yAxis.setTicks(None)
        self.plot.getViewBox().autoRange()
                

    @pyqtSlot(int)
    def updatePlot(self, index):
        pass

    def getChain(self, clickedWidget, data):
        """Get a list that contains data about habit chaining"""
        referenceDf = pd.DataFrame(data, columns = ["value"])
        referenceDf.replace([np.inf, -np.inf], np.nan, inplace=True)

        if clickedWidget.settings.value("type") == cellType.binary:
            referenceDf = pd.concat([pd.DataFrame([np.nan]), referenceDf]).reset_index(drop = True)
            truthDf = referenceDf["value"].ge(1)
            chainDf = truthDf * (truthDf.groupby((truthDf != truthDf.shift()).cumsum()).cumcount() + 1)
            negativeChainDf = -1 * truthDf.groupby(truthDf.cumsum()).cumcount()
            chainDf.loc[chainDf == 0] = negativeChainDf
            chainDf = chainDf.iloc[1:]
        elif clickedWidget.settings.value("type") == cellType.benchmark:
            startingDayIndex = clickedWidget.settings.value("startDate").dayOfWeek()
            numDays = referenceDf.shape[0]
            rulesList = [float(ruleNum) for ruleNum in clickedWidget.settings.value("rules")]
            rulesListShifted = cycle(rulesList[startingDayIndex:] + rulesList[:startingDayIndex])
            rulesDf = [next(rulesListShifted) for count in range(numDays + 1)]
            print(f"referenceDf = {referenceDf}, Shape of referenceDf = {numDays}")
            print(f"RulesDf = {rulesDf}, len = {len(rulesDf)}")

            referenceDf = pd.concat([pd.DataFrame([np.nan]), referenceDf]).reset_index(drop = True)
            truthDf = referenceDf["value"].ge(rulesDf)
            chainDf = truthDf * (truthDf.groupby((truthDf != truthDf.shift()).cumsum()).cumcount() + 1)
            negativeChainDf = -1 * truthDf.groupby(truthDf.cumsum()).cumcount()
            chainDf.loc[chainDf == 0] = negativeChainDf
            chainDf = chainDf.iloc[1:]
            print("Ret list of length = ", chainDf.shape[0])

        return chainDf.to_list()

    def onePercent(self, clickedWidget, data):
        referenceDf = pd.DataFrame(data, columns = ["value"])
        referenceDf.replace([np.inf, -np.inf], np.nan, inplace=True)

        if clickedWidget.settings.value("type") == cellType.binary:
            referenceDf["true"] = referenceDf["value"].ge(1)
            referenceDf["false"] = ~referenceDf["true"]
            referenceDf["trueCnt"] = referenceDf["true"].cumsum()
            referenceDf["falseCnt"] = referenceDf["false"].cumsum()
            ones = np.full(referenceDf.shape[0], 1.01)
            nines = np.full(referenceDf.shape[0], 0.99)
            progress = np.power(ones, referenceDf["trueCnt"]) * np.power(nines, referenceDf["falseCnt"])
        elif clickedWidget.settings.value("type") == cellType.benchmark:
            startingDayIndex = clickedWidget.settings.value("startDate").dayOfWeek()
            numDays = referenceDf.shape[0]
            rulesList = [float(ruleNum) for ruleNum in clickedWidget.settings.value("rules")]
            rulesListShifted = cycle(rulesList[startingDayIndex:] + rulesList[:startingDayIndex])
            rulesDf = [next(rulesListShifted) for count in range(numDays)]

            referenceDf["true"] = referenceDf["value"].ge(rulesDf)
            referenceDf["false"] = ~referenceDf["true"]
            referenceDf["trueCnt"] = referenceDf["true"].cumsum()
            referenceDf["falseCnt"] = referenceDf["false"].cumsum()
            ones = np.full(referenceDf.shape[0], 1.01)
            nines = np.full(referenceDf.shape[0], 0.99)
            progress = np.power(ones, referenceDf["trueCnt"]) * np.power(nines, referenceDf["falseCnt"])

        return progress.to_list()
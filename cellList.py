from PyQt6.QtWidgets import QHBoxLayout, QWidget
from PyQt6.QtCore import Qt, QDate

from contentCell import cellType
from binaryCell import binaryCell, binaryState
from benchmarkCell import benchmarkCell
import sqliteHelper as sql

from time import sleep

DEFAULT_NUM_IN_COLUMN = 14

# Layout of contentCells
class cellList(QWidget):
    """A row of contentCells."""
    def __init__(self, type, tableName = None, topDate = None, parentSettings = None):
        super().__init__()

        self.setFixedHeight(200)
        self.setStyleSheet("""
            QPushButton {
                width: 75px;
                height: 75px;
                border: 0px;
                background: transparent;
            }
            QPushButton#trueBtn {
                border-image: url(images/appIcons/check_trans.png);
            }
            QPushButton#falseBtn {
                border-image: url(images/appIcons/cross_trans.png);
            }
            QPushButton#markedBtn {
                width: 200px;
                height: 100px;
            }
            QLineEdit {
                border-radius: 5px;
                min-width: 50px;
                max-width: 50px;
                height: 50px;
                font-size: 12px;
            }
            QLineEdit[readOnly = 'true'] {
                background: grey;
                border-radius: 5px;
                min-width: 50px;
                max-width: 50px;
                height: 50px;
            }
            QLabel {
                background: transparent;
                min-width: 50px;
                max-width: 50px;
                height: 50px;
                font-size: 12px;
            }
            QLabel#divider {
                background: transparent;
                min-width: 80px;
                max-width: 80px;
                height: 50px;
                font-size: 30px;
            }
        """)

        self.cellType = type
        self.tableName = tableName
        self.parentSettings = parentSettings

        if topDate is not None and tableName is not None:
            self.initUI(topDate)
        else:
            self.initDefault()

    def initDefault(self):
        self.layout = QHBoxLayout()

        if self.cellType == cellType.binary:
            for i in range(DEFAULT_NUM_IN_COLUMN):
                newBinaryCell = binaryCell()
                self.layout.addWidget(newBinaryCell)
        elif self.cellType == cellType.benchmark:
            for i in range(DEFAULT_NUM_IN_COLUMN):
                newBenchmarkCell = benchmarkCell()
                self.layout.addWidget(newBenchmarkCell)
        else:
            print(f"EXCEPTION: {type} not in cellType enum; cellList.initDefault()")

        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)
        
    def initUI(self, topDate):
        self.topDate = topDate
        self.layout = QHBoxLayout()

        info = sql.fetchConsecutive(sql.connection, self.tableName, topDate.toString(Qt.DateFormat.ISODate), DEFAULT_NUM_IN_COLUMN)

        print(info)
        if self.cellType == cellType.binary:
            for i in range(DEFAULT_NUM_IN_COLUMN):
                if i < len(info):
                    newBinaryCell = binaryCell(info[i][1])
                    newBinaryCell.commitRequest.connect(self.commit)
                else:
                    newBinaryCell = binaryCell(binaryState.readOnly)
                self.layout.addWidget(newBinaryCell)
        elif self.cellType == cellType.benchmark:
            for i in range(DEFAULT_NUM_IN_COLUMN):
                if i < len(info):
                    print("Rules = ", self.parentSettings.value("rules"))
                    print("Index = ", QDate.fromString(info[i][0], "yyyy-MM-dd").dayOfWeek() - 1)
                    newBenchmarkCell = benchmarkCell(info[i][1], self.parentSettings.value("rules")[QDate.fromString(info[i][0], "yyyy-MM-dd").dayOfWeek() - 1])
                    newBenchmarkCell.commitRequest.connect(self.commit)
                else:
                    newBenchmarkCell = benchmarkCell(0.0)
                self.layout.addWidget(newBenchmarkCell)
        else:
            print(f"EXCEPTION: {type} not in cellType enum; cellList.initUI()")

        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

    def updateUI(self, newTopDate):
        self.topDate = newTopDate

        info = sql.fetchConsecutive(sql.connection, self.tableName, newTopDate.toString(Qt.DateFormat.ISODate), DEFAULT_NUM_IN_COLUMN)

        print("Length of info = ", len(info))
        if self.cellType == cellType.binary:
            for i in range(DEFAULT_NUM_IN_COLUMN):
                if i < len(info):
                    self.layout.itemAt(i).widget().updateUI(info[i][1])
                else:
                    self.layout.itemAt(i).widget().updateUI(binaryState.readOnly)
        else:
            print(f"EXCEPTION: {type} not in cellType enum.")

    def commit(self, newValue):
        print(f"self.sender() = {self.sender()}")
        index = self.layout.indexOf(self.sender())
        print(f"index = {index}")
        if index >= 0:
            print("Upserting")
            # Valid sender
            sql.upsertDay(sql.connection, self.tableName, self.topDate.addDays(-1 * index).toString(Qt.DateFormat.ISODate), newValue, 1.00)
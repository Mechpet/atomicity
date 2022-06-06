from PyQt6.QtWidgets import QHBoxLayout, QWidget
from PyQt6.QtCore import Qt
from contentCell import cellType
from binaryCell import binaryCell
from benchmarkCell import benchmarkCell
import sqliteHelper as sql

DEFAULT_NUM_IN_COLUMN = 14

# Layout of contentCells
class cellList(QWidget):
    """A row of contentCells."""
    def __init__(self, type, tableName, topDate):
        super().__init__()

        self.setFixedHeight(200)

        self.cellType = type
        self.tableName = tableName

        self.initUI(topDate)

    def initUI(self, topDate):
        layout = QHBoxLayout()

        print("topDate = ", topDate)

        info = sql.fetchConsecutive(sql.connection, self.tableName, topDate.toString(Qt.DateFormat.ISODate), DEFAULT_NUM_IN_COLUMN)
        print("Info = ", info)

        if self.cellType == cellType.binary:
            for i in range(DEFAULT_NUM_IN_COLUMN):
                layout.addWidget(binaryCell(info[i][1]))
        else:
            print(f"EXCEPTION: {type} not in cellType enum.")

        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)
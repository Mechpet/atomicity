from PyQt6.QtWidgets import QVBoxLayout, QWidget
from contentCell import cellType
from binaryCell import binaryCell
from benchmarkCell import benchmarkCell
import sqliteHelper as sql

DEFAULT_NUM_IN_COLUMN = 14

# Layout of contentCells in a vertical column
class contentColumn(QWidget):
    """A row of contentHeads."""
    def __init__(self, type, tableName, topDate):
        super().__init__()

        self.setFixedWidth(200)

        self.cellType = type
        self.tableName = tableName

        self.initUI(topDate)

    def initUI(self, topDate):
        layout = QVBoxLayout()

        info = sql.fetchConsecutive(sql.connection, self.tableName, topDate, DEFAULT_NUM_IN_COLUMN)

        if self.cellType == cellType.binary:
            for i in range(DEFAULT_NUM_IN_COLUMN):
                layout.addWidget(binaryCell(info[i][1]))
        else:
            print(f"EXCEPTION: {type} not in cellType enum.")

        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)
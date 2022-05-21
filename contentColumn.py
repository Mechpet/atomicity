from PyQt6.QtWidgets import QVBoxLayout, QWidget
from contentCell import cellType
from binaryCell import binaryCell
from benchmarkCell import benchmarkCell

DEFAULT_NUM_IN_COLUMN = 30

# Layout of contentCells in a vertical column
class contentColumn(QWidget):
    """A row of contentHeads."""
    def __init__(self, type):
        super().__init__()

        layout = QVBoxLayout()
        if type == cellType.binary:
            for i in range(DEFAULT_NUM_IN_COLUMN):
                layout.addWidget(binaryCell())
        elif type == cellType.benchmark:
            for i in range(DEFAULT_NUM_IN_COLUMN):
                layout.addWidget(benchmarkCell())
        else:
            print(f"EXCEPTION: {type} not in cellType enum.")

        self.setLayout(layout)
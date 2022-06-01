from PyQt6.QtWidgets import QHBoxLayout, QWidget
from contentCell import cellType
from contentColumn import contentColumn

DEFAULT_NUM_COLUMNS = 14
# Layout of contentCells in a vertical column
class contentGrid(QWidget):
    """A grid of contentCells."""
    def __init__(self, type):
        super().__init__()

        layout = QHBoxLayout()
        if type == cellType.binary:
            for i in range(DEFAULT_NUM_COLUMNS):
                layout.addWidget(contentColumn(type))
        elif type == cellType.benchmark:
            for i in range(DEFAULT_NUM_COLUMNS):
                layout.addWidget(contentColumn(type))
        else:
            print(f"EXCEPTION: {type} not in cellType enum.")

        self.setLayout(layout)
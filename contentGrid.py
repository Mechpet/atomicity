from PyQt6.QtWidgets import QHBoxLayout, QWidget
from PyQt6.QtCore import QSettings
from contentCell import cellType
from contentColumn import contentColumn

DEFAULT_NUM_COLUMNS = 14
# Layout of contentCells in a vertical column
class contentGrid(QWidget):
    """A grid of contentColumns."""
    def __init__(self):
        super().__init__()

        self.settings = QSettings("Mechpet", "Atomicity")
        self.settings.beginGroup("contentRow")

        layout = QHBoxLayout()
        for i in range(int(self.settings.value("num"))):
            layout.addWidget(contentColumn(cellType.binary))

        self.setLayout(layout)
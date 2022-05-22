from PyQt6.QtWidgets import QHBoxLayout, QWidget
from contentHead import contentHead

# Layout of contentHeaders in a horizontal row
class contentRow(QWidget):
    """A row of contentHeads."""
    def __init__(self, numCols):
        super().__init__()
        self.list = []

        self.layout = QHBoxLayout()
        for i in range(numCols):
            self.list.append(contentHead())
            self.layout.addWidget(self.list[-1])

        self.setLayout(self.layout)

    def addHeader(self):
        self.list.append(contentHead())
        self.layout.addWidget(self.list[-1])

        self.setLayout(self.layout)

        self.list[-1].settingsWindow()
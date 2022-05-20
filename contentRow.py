from PyQt6.QtWidgets import QHBoxLayout, QWidget
from contentHead import contentHead

# Layout of contentHeaders in a horizontal row
class contentRow(QWidget):
    """A row of contentHeads."""
    def __init__(self, numCols):
        super().__init__()

        layout = QHBoxLayout()
        for i in range(numCols):
            layout.addWidget(contentHead())

        self.setLayout(layout)
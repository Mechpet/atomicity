from PyQt6.QtWidgets import QHBoxLayout, QWidget
from contentHead import contentHead

# Layout of contentHeaders in a horizontal row
class contentRow(QWidget):
    """A row of contentHeads."""
    def __init__(self):
        super().__init__()

        layout = QHBoxLayout()
        layout.addWidget(contentHead())
        layout.addWidget(contentHead())
        layout.addWidget(contentHead())
        layout.addWidget(contentHead())

        self.setLayout(layout)
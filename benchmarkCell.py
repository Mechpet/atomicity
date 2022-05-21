from PyQt6.QtWidgets import QWidget, QPushButton, QHBoxLayout, QLineEdit, QLabel
from PyQt6.QtGui import QCursor
from PyQt6.QtCore import Qt

from contentCell import contentCell

class benchmarkCell(contentCell):
    """Measures the result of one habit on a specific date (numeric inputs only via line editing)"""
    def __init__(self):
        super().__init__()

        self.setStyleSheet("""
            QLineEdit {
                border-radius: 15px;
                background: transparent;
                width: 90px;
                height: 90px;
            }
        """)
        self.initWidgets()

    def initWidgets(self):
        self.input = QLineEdit(self)
        self.input.returnPressed.connect(self.test)
        self.btn = QPushButton(self)
        layout = QHBoxLayout(self)

        layout.addWidget(self.input)
        layout.addWidget(QLabel("50"), 0, Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignBottom)
        self.setLayout(layout)

    def test(self):
        print("Done")
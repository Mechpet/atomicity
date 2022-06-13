from PyQt6.QtWidgets import QHBoxLayout, QLineEdit, QLabel
from PyQt6.QtGui import QDoubleValidator
from PyQt6.QtCore import Qt, pyqtSignal

from contentCell import contentCell

class benchmarkCell(contentCell):
    commitRequest = pyqtSignal(float)
    """Measures the result of one habit on a specific date (numeric inputs only via line editing)"""
    def __init__(self, value = None):
        super().__init__()

        self.setStyleSheet("""
            QLineEdit {
                border-radius: 15px;
                width: 66px;
                height: 100px;
            }

            QLineEdit[readonly = 'true'] {
                background: transparent;
                width: 66px;
                height: 100px;
            }
        """)
        self.initWidgets(value)

    def initWidgets(self, value):
        self.input = QLineEdit(self)
        self.input.setPlaceholderText("None")
        self.input.setText(str(value))
        self.input.setValidator(QDoubleValidator())
        self.input.editingFinished.connect(self.updateProperties)

        self.benchmark = QLineEdit("50.0")
        self.benchmark.setReadOnly(True)
        
        layout = QHBoxLayout(self)

        layout.addWidget(self.input)
        layout.addWidget(self.benchmark, 0, Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignBottom)
        self.setLayout(layout)

    def updateProperties(self):
        self.commitRequest.emit(float(self.input.text()))
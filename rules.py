from PyQt6.QtWidgets import QWidget, QScrollArea, QLineEdit, QLabel, QVBoxLayout, QHBoxLayout

from dateList import dayNames

BENCHMARK_DEFAULT_VALUE = 0.0

class ruleSettings(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.dayLabels = [QLabel(dayName) for dayName in dayNames.values()]
        self.benchmarkEdit = [QLineEdit(str(BENCHMARK_DEFAULT_VALUE)) for label in self.dayLabels]

        self.layout = QHBoxLayout()
        for i in range(len(self.dayLabels)):
            vbox = QVBoxLayout()
            vbox.addWidget(self.dayLabels[i])
            vbox.addWidget(self.benchmarkEdit[i])
            self.layout.addLayout(vbox)

        self.setLayout(self.layout)


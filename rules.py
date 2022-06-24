from mimetypes import init
from PyQt6.QtWidgets import QWidget, QScrollArea, QLineEdit, QLabel, QVBoxLayout, QHBoxLayout
from PyQt6.QtGui import QDoubleValidator

from dateList import dayNames

BENCHMARK_DEFAULT_VALUE = 0.0

class ruleSettings(QWidget):
    def __init__(self, initRules = None):
        super().__init__()

        self.initUI(initRules)

    def initUI(self, initRules):
        self.dayLabels = [QLabel(dayName) for dayName in dayNames.values()]
        if initRules:
            self.benchmarkEdit = [QLineEdit(str(rule)) for rule in initRules]
        else:
            self.benchmarkEdit = [QLineEdit(str(BENCHMARK_DEFAULT_VALUE)) for label in self.dayLabels]

        self.layout = QHBoxLayout()
        for i in range(len(self.dayLabels)):
            vbox = QVBoxLayout()
            self.benchmarkEdit[i].setValidator(QDoubleValidator())
            vbox.addWidget(self.dayLabels[i])
            vbox.addWidget(self.benchmarkEdit[i])
            self.layout.addLayout(vbox)

        self.setLayout(self.layout)

    def ruleValues(self):
        return [float(edit.text()) for edit in self.benchmarkEdit]

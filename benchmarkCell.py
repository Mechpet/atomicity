from PyQt6.QtWidgets import QHBoxLayout, QLineEdit, QLabel
from PyQt6.QtGui import QDoubleValidator, QPainter, QPainterPath, QBrush, QPen, QColor
from PyQt6.QtCore import Qt, pyqtSignal, QRectF

import numpy as np

from contentCell import contentCell
from rules import BENCHMARK_DEFAULT_VALUE

class benchmarkCell(contentCell):
    commitRequest = pyqtSignal(float)
    """Measures the result of one habit on a specific date (numeric inputs only via line editing)"""
    def __init__(self, value = 0.0, benchmark = BENCHMARK_DEFAULT_VALUE):
        super().__init__()

        self.initWidgets(value, benchmark)

    def initWidgets(self, value, benchmark):
        self.input = QLineEdit(self)
        self.input.setPlaceholderText("None")
        self.input.setText(str(value))
        self.input.setValidator(QDoubleValidator())
        self.input.editingFinished.connect(self.updateProperties)

        slash = QLabel("/")
        slash.setObjectName("divider")
        slash.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.benchmark = QLabel(str(benchmark))
        self.benchmark.setAlignment(Qt.AlignmentFlag.AlignCenter)

        if benchmark == BENCHMARK_DEFAULT_VALUE:
            self.input.setReadOnly(True)
        
        layout = QHBoxLayout(self)

        layout.addWidget(self.input)
        layout.addWidget(slash)
        layout.addWidget(self.benchmark)
        layout.setContentsMargins(10, 0, 10, 0)
        self.setLayout(layout)

    def updateProperties(self):
        if not self.input.isReadOnly():
            self.commitRequest.emit(float(self.input.text()))

    def paintEvent(self, e):
        qp = QPainter(self)

        col = QColor(0, 0, 0)
        col.setNamedColor('#d4d4d4')

        qp.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        outerPath = QPainterPath()
        
        pen = QPen(col, 0.5)
        qp.setPen(pen)
        if self.benchmark.text() == str(BENCHMARK_DEFAULT_VALUE): 
            outerBrush = QBrush(self.palette["unmarked"])
        else:
            outerBrush = QBrush(self.palette["markedFalse"])
        qp.setBrush(outerBrush)

        outerRect = QRectF(0, 0, self.frameGeometry().width(), self.frameGeometry().height())
        outerRect.adjust(0.0, 0.0, 1, 1)
        outerPath.addRoundedRect(outerRect, 10, 10)
        qp.setClipPath(outerPath)
        qp.fillPath(outerPath, qp.brush())

        if self.input.text() != "None" and self.input.text() and float(self.input.text()) != 0.00 and float(self.input.text()) != np.inf and float(self.benchmark.text()) != 0.00:
            greenBrush = QBrush(QColor(0, 177, 0))
            qp.setBrush(greenBrush)
            greenRect = QRectF(0, 0, min(self.frameGeometry().width(), abs(int(self.frameGeometry().width() * (float(self.input.text()) / float(self.benchmark.text()))))),
                self.frameGeometry().height())
            greenRect.adjust(0.0, 0.0, 1, 1)
            greenPath = QPainterPath()
            greenPath.addRoundedRect(greenRect, 10, 10)
            qp.setClipPath(greenPath)
            qp.fillPath(greenPath, qp.brush())

        qp.end()
        self.update()

    def updateUI(self, newValue = 0.0, newBenchmark = BENCHMARK_DEFAULT_VALUE):
        """Update the appearance of the benchmarkCell"""
        self.input.setText(str(newValue))
        self.benchmark.setText(str(newBenchmark))
        if newBenchmark == BENCHMARK_DEFAULT_VALUE:
            self.input.setReadOnly(True)
        else:
            self.input.setReadOnly(False)
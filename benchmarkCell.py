from PyQt6.QtWidgets import QHBoxLayout, QLineEdit, QLabel
from PyQt6.QtGui import QDoubleValidator, QPainter, QPainterPath, QBrush, QPen, QColor
from PyQt6.QtCore import Qt, pyqtSignal, QRectF

from contentCell import contentCell
from rules import BENCHMARK_DEFAULT_VALUE

class benchmarkCell(contentCell):
    commitRequest = pyqtSignal(float)
    """Measures the result of one habit on a specific date (numeric inputs only via line editing)"""
    def __init__(self, value = None, benchmark = BENCHMARK_DEFAULT_VALUE):
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
        
        layout = QHBoxLayout(self)

        layout.addWidget(self.input)
        layout.addWidget(slash)
        layout.addWidget(self.benchmark)
        layout.setContentsMargins(10, 0, 10, 0)
        self.setLayout(layout)

    def updateProperties(self):
        self.commitRequest.emit(float(self.input.text()))

    def paintEvent(self, e):
        qp = QPainter(self)

        col = QColor(0, 0, 0)
        col.setNamedColor('#d4d4d4')

        qp.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        redPath = QPainterPath()
        
        pen = QPen(col, 0.5)
        qp.setPen(pen)
        redBrush = QBrush(QColor(177, 0, 0))
        qp.setBrush(redBrush)

        redRect = QRectF(0, 0, self.frameGeometry().width(), self.frameGeometry().height())
        redRect.adjust(0.0, 0.0, 1, 1)
        redPath.addRoundedRect(redRect, 10, 10)
        qp.setClipPath(redPath)
        qp.fillPath(redPath, qp.brush())

        if self.input.text() != "None" and self.input.text() and float(self.input.text()) != 0.00 and float(self.benchmark.text()) != 0.00:
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
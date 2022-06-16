from PyQt6.QtWidgets import QHBoxLayout, QLineEdit, QLabel
from PyQt6.QtGui import QDoubleValidator, QPainter, QPainterPath, QBrush, QPen, QColor
from PyQt6.QtCore import Qt, pyqtSignal, QRectF

from contentCell import contentCell

class benchmarkCell(contentCell):
    commitRequest = pyqtSignal(float)
    """Measures the result of one habit on a specific date (numeric inputs only via line editing)"""
    def __init__(self, value = None):
        super().__init__()

        self.initWidgets(value)

    def initWidgets(self, value):
        self.input = QLineEdit(self)
        self.input.setPlaceholderText("None")
        self.input.setText(str(value))
        self.input.setValidator(QDoubleValidator())
        self.input.editingFinished.connect(self.updateProperties)

        slash = QLabel("/")
        slash.setObjectName("divider")
        slash.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.benchmark = QLabel("50.0")
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
        path = QPainterPath()

        pen = QPen(col, 0.5)
        qp.setPen(pen)
        redBrush = QBrush(QColor(177, 0, 0))
        qp.setBrush(redBrush)

        redRect = QRectF(0, 0, self.frameGeometry().width(), self.frameGeometry().height())
        redRect.adjust(0.0, 0.0, 1, 1)
        path.addRoundedRect(redRect, 10, 10)
        qp.setClipPath(path)
        qp.fillPath(path, qp.brush())
        qp.strokePath(path, qp.pen())

        if self.input.text() != "None":
            greenBrush = QBrush(QColor(0, 177, 0))
            qp.setBrush(greenBrush)
            greenRect = QRectF(0, 0, int(self.frameGeometry().width() * (float(self.input.text()) / float(self.benchmark.text()))),
                self.frameGeometry().height())
            greenRect.adjust(0.0, 0.0, 1, 1)
            path.addRoundedRect(greenRect, 10, 10)
            qp.setClipPath(path)
            qp.fillPath(path, qp.brush())
            qp.strokePath(path, qp.pen())

        qp.end()
        self.update()
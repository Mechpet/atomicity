from PyQt6.QtWidgets import QWidget, QPushButton, QHBoxLayout, QStackedWidget
from PyQt6.QtGui import QPainter, QPainterPath, QBrush, QPen, QColor, QCursor
from PyQt6.QtCore import Qt, QRectF, QSize
import enum

class cellType(enum.Enum):
    """Determines the type of contentCell (and what layout it has, what functions it has)"""
    binary = 1
    benchmark = 2

# `value` = The user-inputted value for the contentCell; accepted options:
#           {binary} None, True, False 
#           {benchmark} None, float
class contentCell(QWidget):
    """Contains information about the activity on a certain day"""
    def __init__(self):
        super().__init__()

        self.palette = {
            "unmarkedBg" : QColor(155, 155, 155),
            "markedTrue" : QColor(0, 200, 0),
            "markedFalse" : QColor(200, 0, 0)
        }
        self.color = self.palette["unmarkedBg"]

        self.initUI()

    def initUI(self):
        """Initialize the appearance of the widgets (for now, only accepts binary-type)"""
        self.minSize = 100
        self.maxSize = 200
        self.setMinimumSize(self.minSize, self.minSize / 2)
        self.setMaximumSize(self.maxSize, self.maxSize / 2)

        self.value = None

    def paintEvent(self, e):
        qp = QPainter(self)
        #qp.begin(self)

        col = QColor(0, 0, 0)
        col.setNamedColor('#d4d4d4')

        qp.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        path = QPainterPath()

        pen = QPen(col, 0.5)
        qp.setPen(pen)
        brush = QBrush(self.color)
        qp.setBrush(brush)

        #rect = QRectF(e.rect())
        rect = QRectF(0, 0, self.frameGeometry().width(), self.frameGeometry().width() / 2)
        rect.adjust(0.0, 0.0, 1, 1)
        path.addRoundedRect(rect, 10, 10)
        qp.setClipPath(path)
        qp.fillPath(path, qp.brush())
        qp.strokePath(path, qp.pen())

        qp.end()
        self.update()
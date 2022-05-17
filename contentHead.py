# Header of each column (topmost block of data that is static to vertical scrolling)
import sys

from PyQt6.QtWidgets import QWidget, QTextEdit, QPushButton
from PyQt6.QtGui import QPainter, QPainterPath, QBrush, QPen, QColor, QTextOption
from PyQt6.QtCore import Qt, QRectF

# `size` = Width and height of the contentHead widget (box-shaped, user-customizable)
# `text` = Main description of the contentHead widget (to be displayed in the center)
class contentHead(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()


    def initUI(self):
        self.size = 200
        self.resize(self.size, self.size)
        self.text = "Wake up"
        
        self.show()

    def paintEvent(self, e):
        qp = QPainter(self)
        qp.begin(self)

        col = QColor(0, 0, 0)
        col.setNamedColor('#d4d4d4')

        col2 = QColor(0, 0, 0)

        qp.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        path = QPainterPath()


        pen = QPen(col, 3)
        qp.setPen(pen)
        brush = QBrush(col2)
        qp.setBrush(brush)

        rect = QRectF(e.rect())
        rect.adjust(1, 1, -1, -1)
        path.addRoundedRect(rect, 10, 10)
        qp.setClipPath(path)
        qp.fillPath(path, qp.brush())
        qp.strokePath(path, qp.pen())
        qp.drawText(rect, self.text, QTextOption(Qt.AlignmentFlag.AlignCenter))

        qp.end()
        #qp.setBrush(QColor(239, 222, 205))
    
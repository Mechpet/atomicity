# Header of each column (topmost block of data that is static to vertical scrolling)
import sys

from PyQt6.QtWidgets import QWidget, QTextEdit, QToolButton, QPushButton
from PyQt6.QtGui import QPainter, QPainterPath, QBrush, QPen, QColor, QTextOption, QIcon
from PyQt6.QtCore import Qt, QRectF

# `size` = Width and height of the contentHead widget (box-shaped, user-customizable)
# `text` = Main description of the contentHead widget (to be displayed in the center)
class contentHead(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()


    def initUI(self):
        self.size = 200
        self.setMinimumSize(self.size, self.size)
        self.text = "\nWake up"
        icon = QIcon(r"images\appIcons\cogwheel.png")

        btn = QPushButton(icon, None, self)
        btn.resize(btn.sizeHint())
        btn.move(0, self.size * 0.85)
        btn.setToolTip("<b>Settings</b>")
        btn.setStyleSheet("""
            QPushButton {
                border: 0px;
                background: transparent;
            }
        """)
        
        self.show()

    def paintEvent(self, e):
        qp = QPainter(self)
        qp.begin(self)

        col = QColor(0, 0, 0)
        col.setNamedColor('#d4d4d4')

        col2 = QColor(55, 55, 55)

        qp.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        path = QPainterPath()

        pen = QPen(col, 3)
        qp.setPen(pen)
        brush = QBrush(col2)
        qp.setBrush(brush)

        #rect = QRectF(e.rect())
        rect = QRectF(0, 0, 200, 200)
        rect.adjust(0.0, 0.0, 1, 1)
        path.addRoundedRect(rect, 10, 10)
        qp.setClipPath(path)
        qp.fillPath(path, qp.brush())
        qp.strokePath(path, qp.pen())
        qp.drawText(rect, self.text, QTextOption(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop))

        qp.end()

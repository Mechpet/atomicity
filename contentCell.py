from PyQt6.QtWidgets import QWidget, QPushButton, QHBoxLayout
from PyQt6.QtGui import QPainter, QPainterPath, QBrush, QPen, QColor
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

        self.color = QColor(55, 55, 55)
        self.setStyleSheet("""
            QPushButton {
                width: 90px;
                height: 90px;
                border: 0px;
                background: transparent;
            }
            QPushButton#trueBtn {
                border-image: url(images/appIcons/cogwheel_idle.png);
            }
            QPushButton#falseBtn {
                border-image: url(images/appIcons/add_trans.png);
            }
        """)

        self.initUI()

    def initUI(self):
        """Initialize the appearance of the widgets (for now, only accepts binary-type)"""
        self.size = 200
        self.setFixedSize(self.size, self.size)

        self.value = None
        self.trueBtn = QPushButton("", self)
        self.trueBtn.setObjectName("trueBtn")
        self.falseBtn = QPushButton("", self)
        self.falseBtn.setObjectName("falseBtn")

        layout = QHBoxLayout()
        layout.addWidget(self.trueBtn)
        layout.addWidget(self.falseBtn)
        self.setLayout(layout)

        self.show()

    def paintEvent(self, e):
        qp = QPainter(self)
        qp.begin(self)

        col = QColor(0, 0, 0)
        col.setNamedColor('#d4d4d4')

        qp.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        path = QPainterPath()

        pen = QPen(col, 0.5)
        qp.setPen(pen)
        brush = QBrush(self.color)
        qp.setBrush(brush)

        #rect = QRectF(e.rect())
        rect = QRectF(0, 0, 200, 200)
        rect.adjust(0.0, 0.0, 1, 1)
        path.addRoundedRect(rect, 10, 10)
        qp.setClipPath(path)
        qp.fillPath(path, qp.brush())
        qp.strokePath(path, qp.pen())

        qp.end()

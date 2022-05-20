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

        self.setStyleSheet("""
            QPushButton {
                width: 90px;
                height: 90px;
                border: 0px;
                background: transparent;
            }
            QPushButton#trueBtn {
                border-image: url(images/appIcons/check_trans.png);
            }
            QPushButton#falseBtn {
                border-image: url(images/appIcons/cross_trans.png);
            }
            QPushButton#markedBtn {
                width: 200px;
                height: 100px;
            }
        """)
        self.palette = {
            "unmarkedBg" : QColor(155, 155, 155),
            "markedTrue" : QColor(0, 255, 0),
            "markedFalse" : QColor(255, 0, 0)
        }
        self.color = self.palette["unmarkedBg"]

        self.initUI()

    def initUI(self):
        """Initialize the appearance of the widgets (for now, only accepts binary-type)"""
        self.size = 200
        self.setMaximumSize(self.size, self.size)

        self.value = None
        # contentCell binary-type:
        #   Unmarked cell: trueBtn / falseBtn
        #   Marked   cell: indicator of true / false
        
        # on click: swap to the opposite cell
        self.cell = QStackedWidget()

        # Unmarked cell:
        self.unmarked = QWidget(self)
        self.unmarked.setMaximumSize(self.size, self.size)

        self.trueBtn = QPushButton("", self)
        self.trueBtn.setObjectName("trueBtn")
        self.trueBtn.setToolTip("Complete!")
        self.trueBtn.clicked.connect(self.setTrue)
        self.trueBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.falseBtn = QPushButton("", self)
        self.falseBtn.setObjectName("falseBtn")
        self.falseBtn.setToolTip("Incomplete...")
        self.falseBtn.clicked.connect(self.setFalse)
        self.falseBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        layout = QHBoxLayout()
        layout.addWidget(self.trueBtn, 0, Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(self.falseBtn, 0, Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignRight)
        self.unmarked.setLayout(layout)

        # Marked cell:
        self.marked = QPushButton("", self)
        self.marked.setObjectName("markedBtn")
        self.marked.clicked.connect(self.resetMarked)
        self.marked.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.cell.addWidget(self.unmarked)
        self.cell.addWidget(self.marked)
        self.cell.setCurrentWidget(self.unmarked)

        layout2 = QHBoxLayout()
        layout2.addWidget(self.cell)
        self.setLayout(layout2)
        self.show()

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
        rect = QRectF(0, 0, self.size, self.size / 2)
        rect.adjust(0.0, 0.0, 1, 1)
        path.addRoundedRect(rect, 10, 10)
        qp.setClipPath(path)
        qp.fillPath(path, qp.brush())
        qp.strokePath(path, qp.pen())

        qp.end()
        self.update()
    
    def setTrue(self):
        self.value = True
        self.color = self.palette["markedTrue"]
        self.cell.setCurrentWidget(self.marked)

    def setFalse(self):
        self.value = False
        self.color = self.palette["markedFalse"]
        self.cell.setCurrentWidget(self.marked)

    def resetMarked(self):
        """If the user 'resets', but they don't actually do anything, the value is not lost"""
        self.cell.setCurrentWidget(self.unmarked)
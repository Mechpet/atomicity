# Header of each column (topmost block of data that is static to vertical scrolling)
from logging.handlers import QueueListener
import sys

from PyQt6.QtWidgets import QWidget, QTextEdit, QToolButton, QPushButton, QLineEdit, QGridLayout
from PyQt6.QtGui import QPainter, QPainterPath, QBrush, QPen, QColor, QTextOption, QIcon
from PyQt6.QtCore import Qt, QRectF
from window import Window
from settingsWindow import contentHeadSettingsWindow

# # # Attributes:
# `size` = Width and height of the contentHead widget (box-shaped, user-customizable)
# `text` = Main description of the contentHead widget (to be displayed in the center; adjustable via `settingsWindow`)
# `color` = Color of the contentHead widget's body (adjustable via `settingsWindow`)
class contentHead(QWidget):
    """A block that acts as the head of the list of contentCells."""
    def __init__(self):
        super().__init__()
        self.initUI()


    def initUI(self):
        self.size = 200
        self.setMinimumSize(self.size, self.size)
        self.text = "\nWake up"
        icon = QIcon(r"images\appIcons\cogwheel_trans.png")

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
        btn.clicked.connect(self.settingsWindow)
        
        self.show()

    def paintEvent(self, e):
        qp = QPainter(self)
        qp.begin(self)

        col = QColor(0, 0, 0)
        col.setNamedColor('#d4d4d4')

        col2 = QColor(55, 55, 55)

        qp.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        path = QPainterPath()

        pen = QPen(col, 0.5)
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

    def settingsWindow(self):
        self.window = contentHeadSettingsWindow(0, 0, 250, 250, self.text)
        self.window.apply.connect(self.updateData)
        self.window.show()

    def updateData(self, text):
        """[Slot] Update the contentHead's text"""
        self.text = text
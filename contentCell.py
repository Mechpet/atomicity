from PyQt6.QtWidgets import QWidget, QPushButton, QHBoxLayout, QStackedWidget
from PyQt6.QtGui import QPainter, QPainterPath, QBrush, QPen, QColor, QCursor
from PyQt6.QtCore import Qt, QRectF, QSize

from enum import IntEnum
import numpy as np

class cellType(IntEnum):
    """Determines the type of contentCell (and what layout it has, what functions it has)"""
    binary = 1
    benchmark = 2

palette = {
    "unmarked" : QColor(155, 155, 155),
    "markedTrue" : QColor(0, 200, 0),
    "markedFalse" : QColor(200, 0, 0),
    "null" : QColor(0, 0, 0)
}

# `value` = The user-inputted value for the contentCell; accepted options:
#           {binary} None, True, False 
#           {benchmark} None, float
class contentCell(QWidget):
    """Contains information about the activity on a certain day"""
    def __init__(self):
        super().__init__()

        self.palette = {
            "unmarked" : QColor(155, 155, 155),
            "markedTrue" : QColor(0, 200, 0),
            "markedFalse" : QColor(200, 0, 0),
            "null" : QColor(0, 0, 0)
        }
        self.color = palette["unmarked"]

        self.initUI()

    def initUI(self):
        """Initialize the appearance of the widgets"""
        self.size = 200
        self.setFixedSize(self.size, 100)

        self.value = np.nan


from PyQt6.QtWidgets import QScrollArea
from PyQt6.QtCore import Qt

class scroll(QScrollArea):
    def __init__(self):
        super().__init__()

    def wheelEvent(self, event):
        if event.modifiers() == Qt.KeyboardModifier.ShiftModifier:
            self.horizontalScrollBar().wheelEvent(event)
        else:
            self.verticalScrollBar().wheelEvent(event)

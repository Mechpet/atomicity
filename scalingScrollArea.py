from PyQt6.QtWidgets import QScrollArea
from PyQt6.QtCore import QEvent

class scalingScrollArea(QScrollArea):
    def __init__(self):
        super().__init__()
    
    def eventFilter(self, object, event):
        if object is self.widget():
            if event.type == QEvent.Type.Resize:
                print("Setting maximum width to ", self.width() - self.viewport().width() + self.widget().width())
                self.setMaximumWidth(self.width() - self.viewport().width() + self.widget().width())
        return super().eventFilter(object, event)

    
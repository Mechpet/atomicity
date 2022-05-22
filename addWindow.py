from PyQt6.QtWidgets import QPushButton, QGridLayout, QLineEdit
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor

from window import Window

ADD_WINDOW_NAME = "Add new header"
class addWindow(Window):
    def __init__(self, x, y, w, h):
        super().__init__(ADD_WINDOW_NAME, x, y, w, h)
        self.initUI(ADD_WINDOW_NAME, x, y, w, h)

        self.setWindowModality(Qt.WindowModality.ApplicationModal)
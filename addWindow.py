from PyQt6.QtWidgets import QPushButton, QHBoxLayout

from window import Window

ADD_WINDOW_NAME = "Add new header"
class addWindow(Window):
    def __init__(self, x, y, w, h):
        super().__init__(ADD_WINDOW_NAME, x, y, w, h)
        pushbtn = QPushButton("YO", self)
        layout = QHBoxLayout()
        layout.addWidget(pushbtn)
        self.setLayout(layout)
        
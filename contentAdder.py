from PyQt6.QtWidgets import QWidget, QPushButton, QVBoxLayout
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import QSize


class contentAdder(QWidget):
    """Fixed cell that allows adding new contentHeaders"""
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.width = 100
        self.height = 200
        self.setMinimumSize(self.width, self.height)


        icon = QIcon(r"images\appIcons\add_trans.png")
        self.btn = QPushButton(icon, None, self)
        self.btn.resize(self.width, self.height)
        self.btn.setIconSize(QSize(self.width, self.height))
        self.btn.setToolTip("<b>Add new item</b>")
        self.btn.setStyleSheet("""
            QPushButton {
                border: 0px;
                border-radius: 15px;
                background-color: transparent;
            }
            QPushButton:hover {
                border: 1px;
                background-color: grey;
            }
        """)

        self.show()
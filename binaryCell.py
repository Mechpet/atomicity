from PyQt6.QtWidgets import QWidget, QPushButton, QHBoxLayout, QStackedWidget
from PyQt6.QtGui import QCursor
from PyQt6.QtCore import Qt

from contentCell import contentCell

class binaryCell(contentCell):
    """Measures the result of one habit on a specific date (true or false inputs only via buttons)"""
    def __init__(self):
        super().__init__()

        self.setStyleSheet("""
            QPushButton {
                width: 75px;
                height: 75px;
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
        self.initUI()
        self.initWidgets()

    def initWidgets(self):
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
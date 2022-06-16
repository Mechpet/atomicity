from PyQt6.QtWidgets import QWidget, QPushButton, QHBoxLayout, QStackedWidget
from PyQt6.QtGui import QCursor
from PyQt6.QtCore import Qt, pyqtSignal
from timeit import default_timer as timer

from contentCell import contentCell, palette
from time import sleep
from enum import IntEnum

class binaryState(IntEnum):
    """Determines the type of contentCell (and what layout it has, what functions it has)"""
    readOnly = -1
    false = 0
    true = 1

class binaryCell(contentCell):
    commitRequest = pyqtSignal(bool)
    """Measures the result of one habit on a specific date (true or false inputs only via buttons)"""
    def __init__(self, state):
        super().__init__()

        self.initUI()
        self.value = state
        self.initWidgets()

    def initWidgets(self):
        # contentCell binary-type:
        #   Unmarked cell: trueBtn / falseBtn
        #   Marked   cell: indicator of true / false
        
        # on click: swap to the opposite cell
        self.cell = QStackedWidget(self)

        # Unmarked cell:
        self.unmarked = QWidget(self)

        self.trueBtn = QPushButton("", self)
        self.trueBtn.setObjectName("trueBtn")
        self.trueBtn.setToolTip("Complete!")
        self.trueBtn.clicked.connect(lambda: self.updateProperties(self.setTrue))
        self.trueBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.falseBtn = QPushButton("", self)
        self.falseBtn.setObjectName("falseBtn")
        self.falseBtn.setToolTip("Incomplete...")
        self.falseBtn.clicked.connect(lambda: self.updateProperties(self.setFalse))
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

        if self.value == binaryState.true.value:
            self.setTrue()
        elif self.value == binaryState.false.value:
            self.setFalse()
        elif self.value == binaryState.readOnly.value:
            print("IS READ ONLY")
            self.cell.hide()
        else:
            print("DIDNt do aything")

    def setReadOnly(self):
        start = timer()
        self.cell.hide()
        end = timer()
        print(f"Hiding took {end - start}")

    def updateUI(self, newValue):
        if newValue == binaryState.true.value:
            self.setTrue()
        elif newValue == binaryState.false.value:
            self.setFalse()
        elif newValue == None:
            self.resetMarked()
        elif newValue == binaryState.readOnly.value:
            self.setReadOnly()
    
    def setTrue(self):
        self.value = True
        self.color = palette["markedTrue"]
        self.cell.setCurrentWidget(self.marked)
        start = timer()
        self.cell.show()
        end = timer()
        print(f"Showing took {end - start}")

    def setFalse(self):
        self.value = False
        self.color = palette["markedFalse"]
        self.cell.setCurrentWidget(self.marked)
        start = timer()
        self.cell.show()
        end = timer()
        print(f"Showing took {end - start}")

    def updateProperties(self, fn):
        fn()
        self.commitRequest.emit(self.value)

    def resetMarked(self):
        """If the user 'resets', but they don't actually do anything, the value is not lost"""
        self.color = palette["unmarked"]
        self.cell.setCurrentWidget(self.unmarked)
        start = timer()
        self.cell.show()
        end = timer()
        print(f"Showing took {end - start}")
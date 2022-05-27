from PyQt6.QtCore import QDate, pyqtSignal
from PyQt6.QtWidgets import QCalendarWidget, QHBoxLayout, QVBoxLayout, QPushButton
from window import Window

CALENDAR_WINDOW_NAME = "Adjust date"
class calendarWindow(Window):
    apply = pyqtSignal(QDate)
    def __init__(self, x, y, w, h, initTopDate):
        super().__init__(CALENDAR_WINDOW_NAME, x, y, w, h)

        self.initUI(CALENDAR_WINDOW_NAME, x, y, w, h)
        self.initWidgets(initTopDate)

    def initWidgets(self, initTopDate):
        self.calendar = QCalendarWidget()
        # Focus the calendar on the topmost date
        self.calendar.setSelectedDate(initTopDate)
        
        self.todayBtn = QPushButton("Go to today", self)
        self.applyBtn = QPushButton("Apply", self)
        self.cancelBtn = QPushButton("Cancel", self)

        self.applyBtn.clicked.connect(self.sendDate)
        self.todayBtn.clicked.connect(lambda: self.calendar.setSelectedDate(QDate.currentDate()))
        self.cancelBtn.clicked.connect(self.close)
        
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.calendar)
        mainLayout.addWidget(self.todayBtn)
        hLayout1 = QHBoxLayout()
        hLayout1.addWidget(self.applyBtn)
        hLayout1.addWidget(self.cancelBtn)
        mainLayout.addLayout(hLayout1)

        self.setLayout(mainLayout)

    def sendDate(self):
        self.apply.emit(self.calendar.selectedDate())
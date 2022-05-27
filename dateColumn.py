from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QCalendarWidget, QScrollArea
from PyQt6.QtCore import Qt, QDate
from calendarWindow import calendarWindow

# Maps the dayOfWeek() -> Name of day
dayNames = {
    1 : "Monday",
    2 : "Tuesday",
    3 : "Wednesday",
    4 : "Thursday",
    5 : "Friday",
    6 : "Saturday",
    7 : "Sunday"
}

class dateColumn(QWidget):
    def __init__(self, firstDay = QDate.currentDate()):
        super().__init__()
        self.numDays = 14
        self.dialog = None

        self.setStyleSheet("""
            QLabel#dateLabel {
                font: 12pt Helvetica;
                font-weight: bold;
            }
            QLabel#dayLabel {
                font: 10pt Helvetica;
            }
        """)
        self.initUI(firstDay)

    def initUI(self, firstDay):
        self.size = 200
        self.setMinimumSize(self.size, self.size)

        self.topDate = firstDay
        self.dates = [self.topDate]
        self.dateLabels = []
        self.dayLabels = []
        for i in range(self.numDays):
            self.dates.append(self.dates[-1].addDays(-1))
        self.layout = QVBoxLayout(self)

        for date in self.dates:
            dateLabel = QLabel(date.toString(Qt.DateFormat.RFC2822Date), self)
            dateLabel.setObjectName("dateLabel")
            dateLabel.setWordWrap(True)
            dayLabel = QLabel(dayNames[date.dayOfWeek()], self)
            dayLabel.setWordWrap(True)
            dayLabel.setObjectName("dayLabel")
            self.dateLabels.append(dateLabel)
            self.dayLabels.append(dayLabel)
            self.layout.addWidget(dateLabel)
            self.layout.addWidget(dayLabel, 0, Qt.AlignmentFlag.AlignHCenter)
            self.layout.addSpacing(50)
        
        self.setLayout(self.layout)
    
    def updateDate(self, topDate):
        self.topDate = topDate
        self.dates = [self.topDate]
        for i in range(self.numDays):
            self.dateLabels[i].setText(self.dates[-1].toString(Qt.DateFormat.RFC2822Date))
            self.dayLabels[i].setText(dayNames[self.dates[-1].dayOfWeek()])
            self.dates.append(self.dates[-1].addDays(-1))

        if self.dialog:
            self.dialog.close()

    def setDate(self):
        self.dialog = calendarWindow(200, 200, 500, 500, self.topDate)
        self.dialog.apply.connect(self.updateDate)
        self.dialog.show()

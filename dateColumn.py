from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt, QDate, pyqtSignal
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
    topDateChanged = pyqtSignal(QDate)
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
        self.dayDates = []
        for i in range(self.numDays - 1):
            self.dates.append(self.dates[-1].addDays(-1))
        self.layout = QVBoxLayout(self)

        for date in self.dates:
            newDayDate = dayDate(date)
            self.dayDates.append(newDayDate)
            self.layout.addWidget(newDayDate)
        
        self.setLayout(self.layout)
    
    def updateDate(self, topDate):
        # Update the topmost date only if the selected date is not in the future
        if topDate != self.topDate:
            self.topDate = topDate
            self.dates = [self.topDate]
            for i in range(self.numDays):
                self.dayDates[i].updateDate(self.dates[-1])
                self.dates.append(self.dates[-1].addDays(-1))
            self.topDateChanged.emit(topDate)

        if self.dialog is not None:
            self.dialog.close()

    def setDate(self):
        self.dialog = calendarWindow(200, 200, 500, 500, self.topDate)
        self.dialog.apply.connect(self.updateDate)
        self.dialog.show()

class dayDate(QWidget):
    def __init__(self, date):
        super().__init__()

        self.initUI(date)
    
    def initUI(self, date):
        self.setFixedSize(200, 100)
        self.dateLabel = QLabel(date.toString(Qt.DateFormat.ISODate), self)
        self.dateLabel.setObjectName("dateLabel")
        self.dateLabel.setWordWrap(True)
        self.dayLabel = QLabel(dayNames[date.dayOfWeek()], self)
        self.dayLabel.setWordWrap(True)
        self.dayLabel.setObjectName("dayLabel")

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.dateLabel)
        self.layout.addWidget(self.dayLabel, 0, Qt.AlignmentFlag.AlignHCenter)
    
    def updateDate(self, newDate):
        self.dateLabel.setText(newDate.toString(Qt.DateFormat.ISODate))
        self.dayLabel.setText(dayNames[newDate.dayOfWeek()])
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QCalendarWidget, QScrollArea
from PyQt6.QtCore import Qt, QDate

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
    def __init__(self):
        super().__init__()
        self.numDays = 14
        self.setStyleSheet("""
            QLabel#dateLabel {
                font: 12pt Helvetica;
                font-weight: bold;
            }
            QLabel#dayLabel {
                font: 10pt Helvetica;
            }
        """)
        self.initUI()

    def initUI(self):
        self.scroll = QScrollArea()
        self.topDate = QDate.currentDate()
        self.dates = [self.topDate]
        for i in range(self.numDays):
            self.dates.append(self.dates[-1].addDays(-1))
        layout = QVBoxLayout(self)

        for date in self.dates:
            dateLabel = QLabel(date.toString(Qt.DateFormat.RFC2822Date), self)
            dateLabel.setObjectName("dateLabel")
            dayLabel = QLabel(dayNames[date.dayOfWeek()], self)
            dayLabel.setObjectName("dayLabel")
            layout.addWidget(dateLabel)
            layout.addWidget(dayLabel, 0, Qt.AlignmentFlag.AlignHCenter)
            layout.addSpacing(50)

        self.setLayout(layout)

        #Scroll Area Properties
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        #self.scroll.setWidget(self)

        self.show()

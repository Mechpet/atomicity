from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
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
        self.numDays = 7
        self.initUI()

    def initUI(self):
        self.topDate = QDate.currentDate()
        self.dates = [self.topDate]
        for i in range(self.numDays):
            self.dates.append(self.dates[-1].addDays(-1))
        layout = QVBoxLayout()

        for date in self.dates:
            # Plan to style each label differently but have them right above/below one another
            dateLabel = QLabel(date.toString(Qt.DateFormat.RFC2822Date), self)
            dayLabel = QLabel(dayNames[date.dayOfWeek()], self)
            newLabel = QLabel(date.toString(Qt.DateFormat.RFC2822Date) + '\n' + dayNames[date.dayOfWeek()], self)
            newLabel.setFixedHeight(100)
            layout.addWidget(newLabel)

        self.setLayout(layout)
        self.show()

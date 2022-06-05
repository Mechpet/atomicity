from PyQt6.QtCore import QDate, pyqtSignal, Qt
from PyQt6.QtWidgets import QCalendarWidget, QHBoxLayout, QVBoxLayout, QPushButton
from window import Window

CALENDAR_WINDOW_NAME = "Adjust date"
class calendarWindow(Window):
    apply = pyqtSignal(QDate)
    def __init__(self, x, y, w, h, initTopDate):
        super().__init__(CALENDAR_WINDOW_NAME, x, y, w, h)

        self.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.initUI(CALENDAR_WINDOW_NAME, x, y, w, h)
        self.initWidgets(initTopDate)

    def initWidgets(self, initTopDate):
        self.calendar = QCalendarWidget()
        # Focus the calendar on the topmost date
        self.calendar.setSelectedDate(initTopDate)
        self.calendar.setMaximumDate(QDate.currentDate())
        self.calendar.setStyleSheet("""
            QCalendarWidget QToolButton {
  	            height: 60px;
  	            width: 150px;
  	            color: white;
  	            font-size: 24px;
  	            icon-size: 56px, 56px;
  	            background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop: 0 #cccccc, stop: 1 #333333);
            }
            QCalendarWidget QMenu {
  	            width: 150px;
  	            left: 20px;
  	            color: white;
  	            font-size: 18px;
  	            background-color: rgb(100, 100, 100);
            }
            QCalendarWidget QSpinBox { 
  	            width: 150px; 
  	            font-size:24px; 
  	            color: white; 
  	            background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop: 0 #cccccc, stop: 1 #333333); 
  	            selection-background-color: rgb(136, 136, 136);
  	            selection-color: rgb(255, 255, 255);
            }
            QCalendarWidget QSpinBox::up-button { subcontrol-origin: border;  subcontrol-position: top right;  width:65px; }
            QCalendarWidget QSpinBox::down-button {subcontrol-origin: border; subcontrol-position: bottom right;  width:65px;}
            QCalendarWidget QSpinBox::up-arrow { width:56px;  height:56px; }
            QCalendarWidget QSpinBox::down-arrow { width:56px;  height:56px; }
   
            /* header row */
            QCalendarWidget QWidget { alternate-background-color: rgb(128, 128, 128); }
   
            /* normal days */
            QCalendarWidget QAbstractItemView:enabled {
  	            font-size:24px;  
  	            color: rgb(180, 180, 180);  
  	            background-color: black;  
  	            selection-background-color: rgb(64, 64, 64); 
  	            selection-color: rgb(0, 255, 0); 
            }
   
            /* days in other months */
            /* navigation bar */
            QCalendarWidget QWidget#qt_calendar_navigationbar { 
                background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop: 0 #cccccc, stop: 1 #333333); 
            }

            QCalendarWidget QAbstractItemView:disabled { 
                color: rgb(64, 64, 64); 
            }""")
        
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
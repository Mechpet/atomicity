from PyQt6.QtWidgets import QWidget, QGridLayout, QTabWidget, QLabel, QPushButton
from PyQt6.QtCore import Qt, QSettings

from window import Window

class preferences(Window):
    def __init__(self):
        super().__init__("Preferences", 250, 250, 500, 500)

        self.settings = QSettings("Mechpet", "Atomicity")
        self.settings.beginGroup("global")

        self.initWidgets()

    def initWidgets(self):
        """Initialize a window for setting user preferences"""
        centralWidget = QTabWidget()

        self.colorPref = colorPref()
        centralWidget.addTab(self.colorPref, "Colors")

        self.setCentralWidget(centralWidget)

class colorPref(QWidget):
    """The widget for setting color preferences (default colors)"""
    def __init__(self):
        super().__init__()

        self.initUI()
    
    def initUI(self):
        layout = QGridLayout()

        # Fetch the current default colors:
        cellColor, textColor = self.fetchColors()

        # Label that says 'Edit cell color:'
        self.cellColorLabel = QLabel("Edit default cell color:", self)

        # PushButton to the right of the colorLabel that allows editing of color
        self.cellColorEdit = QPushButton(self)
        self.cellColorEdit.setMinimumHeight(150)
        self.cellColorEdit.setStyleSheet (f"""
            QPushButton {{
                border: 0px;
                background: {cellColor.name()};
            }}
        """)

        # Label that says 'Edit text color:'
        self.textColorLabel = QLabel("Edit default text color:", self)

        # PushButton to the right of the colorLabel that allows editing of color
        self.textColorEdit = QPushButton(self)
        self.textColorEdit.setMinimumHeight(150)
        self.textColorEdit.setStyleSheet (f"""
            QPushButton {{
                border: 0px;
                background: {textColor.name()};
            }}
        """)

        layout.addWidget(self.cellColorLabel, 0, 0)
        layout.addWidget(self.cellColorEdit, 0, 1)
        layout.addWidget(self.textColorLabel, 1, 0)
        layout.addWidget(self.textColorLabel, 1, 1)

        self.setLayout(layout)

    def fetchColors(self):
        settings = QSettings("Mechpet", "Atomicity")
        settings.beginGroup("global")

        fetchedCellColor = settings.value("cellColor")
        fetchedTextColor = settings.value("textColor")

        return fetchedCellColor, fetchedTextColor

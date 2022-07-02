from PyQt6.QtWidgets import QWidget, QGridLayout, QTabWidget, QLabel, QPushButton, QColorDialog, QVBoxLayout, QLineEdit
from PyQt6.QtCore import Qt, QSettings, pyqtSlot, pyqtSignal
from PyQt6.QtGui import QColor, QIntValidator

from window import Window
import default

class preferences(Window):
    updateDateList = pyqtSignal()
    def __init__(self):
        super().__init__("Preferences", 250, 250, 500, 500)

        self.settings = QSettings("Mechpet", "Atomicity")
        self.settings.beginGroup("global")

        self.initWidgets()

    def initWidgets(self):
        """Initialize a window for setting user preferences"""
        centralWidget = QWidget()

        tabWidget = QTabWidget()

        self.colorPref = colorPref()
        tabWidget.addTab(self.colorPref, "Colors")

        self.datePref = datePref()
        tabWidget.addTab(self.datePref, "Dates")

        resetBtn = QPushButton("Reset to default")
        resetBtn.clicked.connect(self.resetPref)

        applyBtn = QPushButton("Apply")
        applyBtn.clicked.connect(self.commitPref)

        vbox = QVBoxLayout()
        vbox.addWidget(tabWidget)
        vbox.addWidget(resetBtn)
        vbox.addWidget(applyBtn)
        centralWidget.setLayout(vbox)

        self.setCentralWidget(centralWidget)

    def commitPref(self):
        self.settings.setValue("cellColor", self.colorPref.cellColorEdit.palette().button().color())
        self.settings.setValue("textColor", self.colorPref.textColorEdit.palette().button().color())
        self.settings.setValue("numDays", int(self.datePref.numDaysEdit.text()))
        self.updateDateList.emit()
        self.close()

    def resetPref(self):
        self.colorPref.cellColorEdit.setStyleSheet (f"""
            QPushButton {{
                border: 0px;
                background: {default.cellColor.name()};
            }}
        """)

        self.colorPref.textColorEdit.setStyleSheet (f"""
            QPushButton {{
                border: 0px;
                background: {default.textColor.name()};
            }}
        """)
        
        self.commitPref()


class colorPref(QWidget):
    """The widget for setting color preferences (default colors)"""
    def __init__(self):
        super().__init__()

        self.initUI()
    
    def initUI(self):
        layout = QGridLayout()

        # Fetch the current default colors:
        cellColor, textColor = default.fetchColors()

        # Label that says 'Edit cell color:'
        self.cellColorLabel = QLabel("Edit default cell color:", self)

        # PushButton to the right of the colorLabel that allows editing of color
        self.cellColorEdit = QPushButton(self)
        self.cellColorEdit.setStyleSheet (f"""
            QPushButton {{
                border: 0px;
                background: {cellColor.name()};
            }}
        """)
        self.cellColorEdit.clicked.connect(lambda: self.openColorDialog(self.cellColorEdit.palette().button().color()))

        # Label that says 'Edit text color:'
        self.textColorLabel = QLabel("Edit default text color:", self)

        # PushButton to the right of the colorLabel that allows editing of color
        self.textColorEdit = QPushButton(self)
        self.textColorEdit.setStyleSheet (f"""
            QPushButton {{
                border: 0px;
                background: {textColor.name()};
            }}
        """)
        self.textColorEdit.clicked.connect(lambda: self.openColorDialog(self.textColorEdit.palette().button().color()))

        layout.addWidget(self.cellColorLabel, 0, 0)
        layout.addWidget(self.cellColorEdit, 0, 1)
        layout.addWidget(self.textColorLabel, 1, 0)
        layout.addWidget(self.textColorEdit, 1, 1)

        self.setLayout(layout)

    @pyqtSlot(QColor)
    def openColorDialog(self, initColor):
        """Open a colorDialog that prompts the user for an inputted color for the cell color"""
        self.dialog = QColorDialog()
        self.dialog.setWindowModality(Qt.WindowModality.ApplicationModal)
        newColor = self.dialog.getColor(initColor, self, "Color Picker")

        # Valid color implies the user did not click 'Cancel'
        # Check for change before repainting widget
        if newColor.isValid() and newColor != initColor:
            # Update the widget's pushButton color to the new color
            self.sender().setStyleSheet (f"""
                QPushButton {{
                    border: 0px;
                    background: {newColor.name()};
                }}
            """)
        
        self.dialog = None

class datePref(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        layout = QGridLayout()

        numDays = default.fetchDays()

        numDaysLabel = QLabel("Number of days visible:")
        self.numDaysEdit = QLineEdit(str(numDays))
        self.numDaysEdit.setValidator(QIntValidator())
        self.numDaysEdit.textChanged.connect(self.validateNumDays)

        layout.addWidget(numDaysLabel, 0, 0)
        layout.addWidget(self.numDaysEdit, 0, 1)

        self.setLayout(layout)

    @pyqtSlot(str)
    def validateNumDays(self, newNumDays):
        if int(newNumDays) < default.minNumDays:
            self.numDaysEdit.setText(str(default.minNumDays))
from PyQt6.QtWidgets import QLineEdit, QGridLayout, QPushButton, QLabel, QColorDialog, QFileDialog, QButtonGroup, QRadioButton, QCalendarWidget,\
                            QVBoxLayout, QTabWidget, QWidget, QHBoxLayout
from PyQt6.QtCore import Qt, pyqtSignal, QFile, QDate
from PyQt6.QtGui import QColor, QIcon
import os
from window import Window
from contentCell import cellType
from rules import ruleSettings

SETTINGS_WINDOW_NAME = "Settings"
# Accepted file extensions for the icon image file:
acceptedExtensions = (
    ".jpg",
    ".png",
    ".xmp"
)

# `iconPath`    = Current icon path that the contentHead is using {str}.
# `color`       = Current color that the contentHead is using {QColor}.
# `dialog`      = Current opened dialog (if any).
class contentHeadSettingsWindow(Window):
    """A pop-up window that allows users to adjust the settings of contentHeads."""
    apply = pyqtSignal(str, QColor, QColor, str, int, QDate, list)
    delete = pyqtSignal()
    removeIconSignal = pyqtSignal()
    def __init__(self, x, y, w, h, name, cellColor, textColor, iconPath, type, startDate, instance):
        super().__init__(SETTINGS_WINDOW_NAME, x, y, w, h)

        self.setStyleSheet("""
        """)

        self.dialog = None
        self.instance = instance

        self.initUI(SETTINGS_WINDOW_NAME, x, y, w, h)
        
        # Block inputs to the mainWindow
        self.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.initLayout(name, cellColor, textColor, iconPath, type, startDate)

    def initLayout(self, name, initCellColor, initTextColor, iconPath, type, startDate):
        """Initialize the variable types of the window based on the appearance of the instance"""
        layout = QVBoxLayout()
        globalButtonLayout = QHBoxLayout()
        self.tabs = QTabWidget()

        # Tab widgets:
        general = QWidget()
        self.rules = None

        generalGrid = QGridLayout()

        # Label that says 'Name:'
        self.nameLabel = QLabel("Name:", self)

        # Line edit box to the right of the nameLabel
        self.nameEdit = QLineEdit(name, self)

        # Label that says 'Edit cell color:'
        self.cellColorLabel = QLabel("Edit cell color:", self)

        # PushButton to the right of the colorLabel that allows editing of color
        self.cellColorEdit = QPushButton(self)
        self.cellColorEdit.clicked.connect(lambda: self.openColorDialog(initCellColor, self.cellColorEdit))
        self.cellColorEdit.setMinimumHeight(150)
        self.cellColorEdit.setStyleSheet (f"""
            QPushButton {{
                border: 0px;
                background: {initCellColor.name()};
            }}
        """)

        # Label that says 'Edit text color:'
        self.textColorLabel = QLabel("Edit text color:", self)

        # PushButton to the right of the colorLabel that allows editing of color
        self.textColorEdit = QPushButton(self)
        self.textColorEdit.clicked.connect(lambda: self.openColorDialog(initTextColor, self.textColorEdit))
        self.textColorEdit.setMinimumHeight(150)
        self.textColorEdit.setStyleSheet (f"""
            QPushButton {{
                border: 0px;
                background: {initTextColor.name()};
            }}
        """)

        # Line that allows editing of the icon 
        self.iconLine = QLineEdit(iconPath, self)

        # PushButton that allows editing of the icon that represents the habit
        icon = QIcon(r"images\appIcons\icon_edit.png")
        self.iconEdit = QPushButton(icon, "Edit icon", self)
        self.iconEdit.clicked.connect(self.openFileDialog)

        self.typeLabel = QLabel("Type of habit:", self)

        # RadioButtons that allow changing what type of habit it is (binary or benchmark)
        self.cellTypeOption = QButtonGroup()
        self.binary = QRadioButton("Binary", self)
        self.benchmark = QRadioButton("Benchmark", self)

        self.cellTypeOption.addButton(self.binary, cellType.binary.value)
        self.cellTypeOption.addButton(self.benchmark, cellType.benchmark.value)

        # If the benchmark is picked, make sure the rules tab is available
        self.benchmark.pressed.connect(self.enableRules)

        # If the head has a type already, it has been initialized already
        if type == cellType.binary:
            self.binary.setChecked(True)
            self.binary.setEnabled(False)
            self.benchmark.setEnabled(False)
        elif type == cellType.benchmark:
            self.benchmark.setChecked(True)
            self.binary.setEnabled(False)
            self.benchmark.setEnabled(False)
        else:
            # Default to binary type if the head is new
            self.binary.setChecked(True)

        # Calendar widget to select the starting date
        self.calendar = QCalendarWidget()
        if startDate is not None:
            self.calendar.setSelectedDate(startDate)
            self.calendar.setSelectionMode(QCalendarWidget.SelectionMode.NoSelection)
        else:
            self.calendar.setMaximumDate(QDate.currentDate())

        # PushButton on the bottom-left corner to delete the contentHead and all of its associated data
        self.delButton = QPushButton("Delete", self)
        self.delButton.clicked.connect(self.openConfirmDialog)

        # PushButton on the bottom-right corner that allows applying the settings
        self.applyButton = QPushButton("Apply", self)
        self.applyButton.clicked.connect(self.sendData)

        # PushButton on the bottom-right corner to cancel 
        self.cancelButton = QPushButton("Cancel", self)
        self.cancelButton.clicked.connect(self.close)

        # Format the widgets in a gridLayout
        generalGrid.addWidget(self.nameLabel, 0, 0)
        generalGrid.addWidget(self.nameEdit, 0, 1, 1, -1)
        generalGrid.addWidget(self.cellColorLabel, 1, 0)
        generalGrid.addWidget(self.cellColorEdit, 1, 1, 1, 1)
        generalGrid.addWidget(self.textColorLabel, 1, 2, 1, 1)
        generalGrid.addWidget(self.textColorEdit, 1, 3, 1, 1)
        generalGrid.addWidget(self.iconLine, 2, 0, 1, 3)
        generalGrid.addWidget(self.iconEdit, 2, 4)
        generalGrid.addWidget(self.typeLabel, 3, 0, 1, 1)
        generalGrid.addWidget(self.binary, 3, 2, 1, 1)
        generalGrid.addWidget(self.benchmark, 3, 3, 1, 1)
        generalGrid.addWidget(self.calendar, 4, 0, 2, 4)
        generalGrid.setVerticalSpacing(10)
    
        general.setLayout(generalGrid)

        self.tabs.addTab(general, "General")
        if self.benchmark.isChecked():
            self.rules = ruleSettings()
            self.tabs.addTab(self.rules, "General")

        layout.addWidget(self.tabs)
        globalButtonLayout.addWidget(self.delButton)
        globalButtonLayout.addWidget(self.applyButton)
        globalButtonLayout.addWidget(self.cancelButton)
        layout.addLayout(globalButtonLayout)

        self.setLayout(layout)

    def sendData(self):
        """[Slot] Communicate backward to associated contentHead the text and color, then force close window to immediately update."""
        newText = self.nameEdit.text()
        if newText and newText[0] != '\n':
            newText = '\n\n' + newText
        newIconPath = self.iconLine.text()
        if self.rules is not None:
            newRules = self.rules.ruleValues()
        else:
            newRules = []
        self.apply.emit(newText, self.cellColorEdit.palette().button().color(), self.textColorEdit.palette().button().color(), newIconPath, self.cellTypeOption.checkedId(), self.calendar.selectedDate(), newRules)
        self.close()

    def openColorDialog(self, initColor, widget):
        """Open a colorDialog that prompts the user for an inputted color for the cell color"""
        self.dialog = QColorDialog()
        self.dialog.setWindowModality(Qt.WindowModality.ApplicationModal)
        newColor = self.dialog.getColor(initColor, self, "Color Picker")

        # Valid color implies the user did not click 'Cancel'
        # Check for change before repainting widget
        if newColor.isValid() and newColor != initColor:
            # Update the widget's pushButton color to the new color
            widget.setStyleSheet (f"""
                QPushButton {{
                    border: 0px;
                    background: {newColor.name()};
                }}
            """)
        
        self.dialog = None

    def openFileDialog(self):
        """Open a fileDialog that prompts the user for a file"""

        # Initialize the file dialog for a single image
        self.dialog = QFileDialog()
        # Set initial filter to image file extensions only
        self.dialog.setNameFilter(self.tr("Images (*.png *.xpm *.jpg)"))
        # Accept only one single file
        self.dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        # Instead of 'Open' button, use 'Save' button
        self.dialog.setAcceptMode(QFileDialog.AcceptMode.AcceptSave)
        # Set the initial directory to whatever directory the current iconPath resides in, if any
        if QFile.exists(self.iconLine.text()):
            self.dialog.setDirectory(os.path.split(self.iconLine.text())[0])

        self.dialog.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.dialog.fileSelected.connect(self.iconLine.setText)
        self.dialog.show()

    def openConfirmDialog(self):
        """Opens a confirmation window that asks for the user to confirm deletion"""
        self.dialog = Window("Confirmation", 500, 500, 300, 300)

        queryLabel = QLabel("Are you sure you want to delete this habit?")
        confirmBtn = QPushButton("Confirm")
        confirmBtn.clicked.connect(self.instance.delData)
        cancelBtn = QPushButton("Cancel")
        cancelBtn.clicked.connect(self.dialog.close)

        layout = QGridLayout()
        layout.addWidget(queryLabel, 0, 0, 3, 1)
        layout.addWidget(confirmBtn, 1, 0, 1, 1)
        layout.addWidget(cancelBtn, 1, 2, 1, 1)

        self.dialog.setLayout(layout)
        self.dialog.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.dialog.show()

    def verifyFile(self, fileName):
        """Verify that the chosen file is an image."""
        # Must end with certain compatible extensions
        if fileName:
            return fileName.lower().endswith(acceptedExtensions)

    def setIconPath(self):
        """Set the textEdit to the icon path selected in the fileDialog"""
        self.iconLine.setText(self.dialog.selectedFiles()[0])

    def enableRules(self):
        """Adds the rules tab if not already added"""
        if self.rules is None:
            self.rules = ruleSettings()
            self.tabs.addTab(self.rules, "Rules")

    def disableRules(self):
        """Deletes the rules tab if already added"""
        if self.rules is not None and self.tabs.indexOf(self.rules) != -1:
            self.tabs.removeTab(self.tabs.indexOf(self.rules))
            self.rules.close()
            self.rules = None

from PyQt6.QtWidgets import QLineEdit, QGridLayout, QPushButton, QLabel, QColorDialog, QFileDialog
from PyQt6.QtCore import Qt, pyqtSignal, QFile
from PyQt6.QtGui import QColor, QIcon
import os
from window import Window

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
    apply = pyqtSignal(str, QColor, QColor, str)
    removeIconSignal = pyqtSignal()
    def __init__(self, x, y, w, h, name, cellColor, textColor, iconPath):
        super().__init__(SETTINGS_WINDOW_NAME, x, y, w, h)

        self.dialog = None

        self.initUI(SETTINGS_WINDOW_NAME, x, y, w, h)
        
        # Block inputs to the mainWindow
        self.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.initLayout(name, cellColor, textColor, iconPath)

    def initLayout(self, name, initCellColor, initTextColor, iconPath):
        grid = QGridLayout()

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

        # PushButton on the bottom-right corner that allows applying the settings
        self.applyButton = QPushButton("Apply", self)
        self.applyButton.clicked.connect(self.sendData)

        # PushButton on the bottom-right corner to cancel 
        self.cancelButton = QPushButton("Cancel", self)
        self.cancelButton.clicked.connect(self.close)

        # Format the widgets in a gridLayout
        grid.addWidget(self.nameLabel, 0, 0)
        grid.addWidget(self.nameEdit, 0, 1, 1, -1)
        grid.addWidget(self.cellColorLabel, 1, 0)
        grid.addWidget(self.cellColorEdit, 1, 1, 2, 2)
        grid.addWidget(self.textColorLabel, 3, 0)
        grid.addWidget(self.textColorEdit, 3, 1, 1, 1)
        grid.addWidget(self.iconLine, 4, 0, 1, 3)
        grid.addWidget(self.iconEdit, 4, 3)
        grid.addWidget(self.applyButton, 5, 2, 1, 1)
        grid.addWidget(self.cancelButton, 5, 3, 1, 1)

        self.setLayout(grid)

    def sendData(self):
        """[Slot] Communicate backward to associated contentHead the text and color, then force close window to immediately update."""
        newText = self.nameEdit.text()
        if newText and newText[0] != '\n':
            newText = '\n' + newText
        newIconPath = self.iconLine.text()
        # Pass the currently selected colors (apparent in the pushButtons)
        self.apply.emit(newText, self.cellColorEdit.palette().button().color(), self.textColorEdit.palette().button().color(), newIconPath)
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
            print("Set widget's color")
        
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
        self.dialog.fileSelected.connect(self.setIconPath)
        self.dialog.show()

    def verifyFile(self, fileName):
        """Verify that the chosen file is an image."""
        # Must end with certain compatible extensions
        if fileName:
            return fileName.lower().endswith(acceptedExtensions)

    def setIconPath(self):
        """Set the textEdit to the icon path selected in the fileDialog"""
        self.iconLine.setText(self.dialog.selectedFiles()[0])

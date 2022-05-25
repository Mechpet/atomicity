from posixpath import split
from PyQt6.QtWidgets import QLineEdit, QGridLayout, QPushButton, QLabel, QColorDialog, QFileDialog
from PyQt6.QtCore import Qt, pyqtSignal, QFile
from PyQt6.QtGui import QColor, QIcon
import os
from window import Window

SETTINGS_WINDOW_NAME = "Settings"
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
    apply = pyqtSignal(str, QColor, str)
    def __init__(self, x, y, w, h, name, cellColor, textColor):
        super().__init__(SETTINGS_WINDOW_NAME, x, y, w, h)

        self.dialog = None
        self.iconPath = None
        self.cellColor = cellColor
        self.textColor = textColor

        self.initUI(SETTINGS_WINDOW_NAME, x, y, w, h)
        
        # Block inputs to the mainWindow
        self.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.initLayout(name)

    def initLayout(self, name):
        grid = QGridLayout()

        # Label that says 'Name:'
        self.nameLabel = QLabel("Name:", self)

        # Line edit box to the right of the nameLabel
        self.nameEdit = QLineEdit(name, self)

        # Label that says 'Edit cell color:'
        self.cellColorLabel = QLabel("Edit cell color:", self)

        # PushButton to the right of the colorLabel that allows editing of color
        self.cellColorEdit = QPushButton(self)
        self.cellColorEdit.clicked.connect(lambda color, type: self.openCellColorDialog(color, self.cellColorEdit))
        self.cellColorEdit.setMinimumHeight(150)
        self.cellColorEdit.setStyleSheet (f"""
            QPushButton {{
                border: 0px;
                background: {self.cellColor.name()};
            }}
        """)

        # Label that says 'Edit text color:'
        self.textColorLabel = QLabel("Edit text color:", self)

        # PushButton to the right of the colorLabel that allows editing of color
        self.textColorEdit = QPushButton(self)
        self.textColorEdit.clicked.connect(self.openTextColorDialog)
        self.textColorEdit.setMinimumHeight(150)
        self.textColorEdit.setStyleSheet (f"""
            QPushButton {{
                border: 0px;
                background: {self.textColor.name()};
            }}
        """)

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
        grid.addWidget(self.iconEdit, 2, 0)
        grid.addWidget(self.applyButton, 3, 1, 1, 1)
        grid.addWidget(self.cancelButton, 3, 2, 1, 1)

        self.setLayout(grid)

    def sendData(self):
        """[Slot] Communicate backward to associated contentHead the text and color, then force close window to immediately update."""
        newText = self.nameEdit.text()
        if newText[0] != '\n':
            newText = '\n' + newText
        if self.dialog:
            newIconPath = self.dialog.selectedFiles()[0]
        else:
            newIconPath = None
        self.apply.emit(newText, self.cellColor, newIconPath)
        self.close()

    def openColorDialog(self, initColor, widget):
        """Open a colorDialog that prompts the user for an inputted color for the cell color"""
        self.dialog = QColorDialog()
        self.dialog.setWindowModality(Qt.WindowModality.ApplicationModal)
        newColor = self.dialog.getColor(self.cellColor, self, "Color Picker")

        # Valid color implies the user did not click 'Cancel'
        if newColor.isValid() and newColor != self.cellColor:
            self.cellColor = newColor
            # Update the pushButton's color for colorEdit
            self.cellColorEdit.setStyleSheet (f"""
                QPushButton {{
                    border: 0px;
                    background: {newColor.name()};
                }}
            """)
        
        self.dialog = None

    def openTextColorDialog(self):
        """Open a colorDialog that prompts the user for an inputted color for the cell color"""
        self.dialog = QColorDialog()
        self.dialog.setWindowModality(Qt.WindowModality.ApplicationModal)
        newColor = self.dialog.getColor(self.cellColor, self, "Color Picker")

        # Valid color implies the user did not click 'Cancel'
        if newColor.isValid() and newColor != self.cellColor:
            self.cellColor = newColor
            # Update the pushButton's color for colorEdit
            self.cellColorEdit.setStyleSheet (f"""
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
        if QFile.exists(self.iconPath):
            self.dialog.setDirectory(os.path.split(self.iconPath)[0])

        self.dialog.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.dialog.show()

    def verifyFile(self, fileName):
        """Verify that the chosen file is an image."""
        # Must end with certain compatible extensions
        if fileName:
            return fileName.lower().endswith(acceptedExtensions)

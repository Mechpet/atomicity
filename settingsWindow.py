from PyQt6.QtWidgets import QLineEdit, QGridLayout, QPushButton, QLabel, QColorDialog, QFileDialog
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QColor, QIcon
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
    def __init__(self, x, y, w, h, name, color):
        super().__init__(SETTINGS_WINDOW_NAME, x, y, w, h)

        self.dialog = None
        self.iconPath = None
        self.color = color

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

        # Label that says 'Edit color:'
        self.colorLabel = QLabel("Edit color:", self)

        # PushButton to the right of the colorLabel that allows editing of color
        self.colorEdit = QPushButton(self)
        self.colorEdit.clicked.connect(self.openColorDialog)
        self.colorEdit.setMinimumHeight(150)
        self.colorEdit.setStyleSheet (f"""
            QPushButton {{
                border: 0px;
                background: {self.color.name()};
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
        grid.addWidget(self.colorLabel, 1, 0)
        grid.addWidget(self.colorEdit, 1, 1, 2, 2)
        grid.addWidget(self.iconEdit, 2, 0)
        grid.addWidget(self.applyButton, 3, 1, 1, 1)
        grid.addWidget(self.cancelButton, 3, 2, 1, 1)

        self.setLayout(grid)

    def sendData(self):
        """[Slot] Communicate backward to associated contentHead the text and color, then force close window to immediately update."""
        newText = self.nameEdit.text()
        if newText[0] != '\n':
            newText = '\n' + newText
        newIconPath = self.dialog.selectedFiles()[0]
        self.apply.emit(newText, self.color, newIconPath)
        self.close()

    def openColorDialog(self):
        """Open a colorDialog that prompts the user for an inputted color"""
        self.dialog = QColorDialog()
        self.dialog.setWindowModality(Qt.WindowModality.ApplicationModal)
        newColor = self.dialog.getColor(self.color, self, "Color Picker")

        # Valid color implies the user did not click 'Cancel'
        if newColor.isValid() and newColor != self.color:
            self.color = newColor
            # Update the pushButton's color for colorEdit
            self.colorEdit.setStyleSheet (f"""
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

        self.dialog.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.dialog.show()

    def verifyFile(self, fileName):
        """Verify that the chosen file is an image."""
        # Must end with certain compatible extensions
        return fileName.lower().endswith(acceptedExtensions)

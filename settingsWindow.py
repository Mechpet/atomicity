from PyQt6.QtWidgets import QLineEdit, QGridLayout, QPushButton, QLabel, QColorDialog
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QColor
from window import Window

SETTINGS_WINDOW_NAME = "Settings"
class contentHeadSettingsWindow(Window):
    """A pop-up window that allows users to adjust the settings of contentHeads."""
    apply = pyqtSignal(str)
    def __init__(self, x, y, w, h, name, color):
        super().__init__(SETTINGS_WINDOW_NAME, x, y, w, h)
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
        self.colorEdit.setStyleSheet (f"""
            QPushButton {{
                border: 0px;
                background: {self.color.name()};
            }}
        """)

        # PushButton on the bottom-right corner that allows applying the settings
        self.applyButton = QPushButton("Apply", self)
        self.applyButton.clicked.connect(self.sendData)


        # Format the widgets in a gridLayout
        grid.addWidget(self.nameLabel, 1, 0)
        grid.addWidget(self.nameEdit, 1, 1)
        grid.addWidget(self.colorLabel, 2, 0)
        grid.addWidget(self.colorEdit, 2, 1)
        grid.addWidget(self.applyButton, 3, 1)

        self.setLayout(grid)

    def sendData(self):
        """[Signal] apply"""
        """[Slot] Communicate backward to associated contentHead the new text"""
        newText = self.nameEdit.text()
        if newText[0] != '\n':
            newText = '\n' + newText
        self.apply.emit(newText)

    def openColorDialog(self):
        self.dialog = QColorDialog()
        self.dialog.setCurrentColor(self.color)
        self.dialog.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.dialog.show()
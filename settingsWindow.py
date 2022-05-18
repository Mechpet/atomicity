from PyQt6.QtWidgets import QLineEdit, QGridLayout, QPushButton
from PyQt6.QtCore import Qt, pyqtSignal
from window import Window

SETTINGS_WINDOW_NAME = "Settings"
class contentHeadSettingsWindow(Window):
    """A pop-up window that allows users to adjust the settings of contentHeads."""
    apply = pyqtSignal(str)
    def __init__(self, x, y, w, h, name):
        super().__init__(SETTINGS_WINDOW_NAME, x, y, w, h)

        self.initUI(SETTINGS_WINDOW_NAME, x, y, w, h)
        
        # Block inputs to the mainWindow
        self.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.initLayout(name)

    def initLayout(self, name):
        grid = QGridLayout()

        self.nameEdit = QLineEdit(name)
        grid.addWidget(self.nameEdit, 1, 0)
        self.applyButton = QPushButton("Apply", self)
        self.applyButton.clicked.connect(self.sendData)
        grid.addWidget(self.applyButton, 2, 0)

        self.setLayout(grid)

    def sendData(self):
        """[Signal] apply"""
        """[Slot] Communicate backward to associated contentHead the new text"""
        newText = self.nameEdit.text()
        if newText[0] != '\n':
            newText = '\n' + newText
        self.apply.emit(newText)

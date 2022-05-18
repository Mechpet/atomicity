from PyQt6.QtWidgets import QLineEdit, QGridLayout
from PyQt6.QtCore import Qt
from window import Window

SETTINGS_WINDOW_NAME = "Settings"
class contentHeadSettingsWindow(Window):
    """A pop-up window that allows users to adjust the settings of contentHeads."""
    def __init__(self, x, y, w, h, name):
        super().__init__(SETTINGS_WINDOW_NAME, x, y, w, h)

        self.initUI(SETTINGS_WINDOW_NAME, x, y, w, h)
        
        # Block inputs to the mainWindow
        self.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.initLayout(name)

    def initLayout(self, name):
        grid = QGridLayout()

        nameEdit = QLineEdit(name)
        grid.addWidget(nameEdit, 1, 0)

        self.setLayout(grid)

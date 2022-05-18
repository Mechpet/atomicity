# The main window of the application 
import sys
import ctypes

from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout
from PyQt6.QtGui import QIcon

APP_ID = "Atomicity"

# Common window of the application (sharing the same appId)
class Window(QWidget):
    """A new window that share the same appID with all other `Windows`."""
    def __init__(self, name, x, y, w, h):
        super().__init__()

        self.initUI(name, x, y, w, h)

    def initUI(self, name, x, y, w, h):
        # Set the window icon and taskbar icon
        self.setWindowIcon(QIcon(r"images\icon3_trans.png"))
        self.setWindowTitle(name)
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(APP_ID)

        self.setMinimumSize(w, h)
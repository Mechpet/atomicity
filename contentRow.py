from PyQt6.QtWidgets import QHBoxLayout, QWidget
from PyQt6.QtCore import QSettings
from contentHead import contentHead

# Layout of contentHeaders in a horizontal row
class contentRow(QWidget):
    """A row of contentHeads."""
    def __init__(self):
        super().__init__()
        self.settings = QSettings("Mechpet", "Atomicity")
        self.settings.beginGroup("contentRow")

        self.list = []

        self.layout = QHBoxLayout()
        for i in range(len(self.list)):
            self.list.append(contentHead(i))
            self.layout.addWidget(self.list[-1])

        self.setLayout(self.layout)

    def addHeader(self):
        # Create a new contentHead devoid of settings
        self.list.append(contentHead(len(self.list)))
        # Set the index of the contentHead to be at the end of the row
        self.layout.addWidget(self.list[-1])
        self.settings.setValue("num", len(self.list))
        print(self.settings.value("num"))

        self.setLayout(self.layout)

        self.list[-1].settingsWindow()

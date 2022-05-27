from PyQt6.QtWidgets import QHBoxLayout, QWidget
from PyQt6.QtCore import QSettings, QEvent, Qt
from contentHead import contentHead

# Layout of contentHeaders in a horizontal row
class contentRow(QWidget):
    """A row of contentHeads."""
    def __init__(self):
        super().__init__()
        self.installEventFilter(self)
        self.settings = QSettings("Mechpet", "Atomicity")
        self.settings.beginGroup("contentRow")

        self.list = []

        self.layout = QHBoxLayout()

        if self.settings.value("num"):
            for i in range(int(self.settings.value("num"))):
                self.list.append(contentHead(i))
                self.layout.addWidget(self.list[-1])
        else:
            # The key "num" is not a QString of an integer
            self.settings.setValue("num", 0)

        self.setLayout(self.layout)

    def addHeader(self):
        # Create a new contentHead devoid of settings
        self.list.append(contentHead(-(len(self.list) + 1)))
        # Set the index of the contentHead to be at the end of the row
        self.layout.addWidget(self.list[-1])
        self.settings.setValue("num", len(self.list))
        print(self.settings.value("num"))

        self.setLayout(self.layout)

        self.list[-1].settingsWindow()

    def eventFilter(self, object, event):
        """Filter mouse events"""
        if event.type() == QEvent.Type.MouseButtonPress:
            self.mousePressEvent(event)
        return super().eventFilter(object, event)
    
    def mousePressEvent(self, event):
        """When the mouse left-clicks on a contentHead, store information about the item being moved"""
        if event.button() == Qt.MouseButton.LeftButton:
            #self.showAllGeometries()
            self.selectedIndex = self.getIndex(event.position().x(), event.position().y())

    def getIndex(self, x, y):
        """Get the item index of the content"""
        for item in self.list:
            # Iterate through list of contentHeads, looking for the one that the user selected
            print(f"Geometry = {item.geometry()}")
            if item.geometry().contains(x, y):
                self.layout.removeWidget(item)
        return None

    def showAllGeometries(self):
        for item in self.list:
            print(f"Geometry = {item.geometry()}")
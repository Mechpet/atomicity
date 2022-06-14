from PyQt6.QtWidgets import QVBoxLayout, QWidget, QLayout, QScrollArea, QFrame, QSizePolicy
from PyQt6.QtCore import QSettings, Qt, QMimeData, pyqtSignal, QObject, QTimer, QThread, QPoint, QEvent
from PyQt6.QtGui import QDrag, QPixmap, QPainter
from math import floor
import os

from contentHead import contentHead
from contentCell import cellType

# Layout of contentHeads 
class headList(QWidget):
    """A row of contentHeads."""
    append = pyqtSignal(int)
    deleteRow = pyqtSignal(int)
    rearrangeRow = pyqtSignal(int, int)
    def __init__(self):
        super().__init__()

        self.settings = QSettings("Mechpet", "Atomicity")
        self.settings.beginGroup("headList")

        self.setMinimumSize(200, 200)
        print("Height = ", self.height())

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSizeConstraint(QLayout.SizeConstraint.SetMinAndMaxSize)

        if self.settings.value("num"):
            for i in range(int(self.settings.value("num"))):
                self.layout.addWidget(contentHead(i, self))
        else:
            # The key "num" is not a QString of an integer
            self.settings.setValue("num", 0)

        self.setLayout(self.layout)

    def rearrange(self, selected, target):
        targetIndex = self.layout.indexOf(target)
        self.layout.removeWidget(selected)
        self.layout.insertWidget(targetIndex, selected)
        self.rearrangeRow.emit(selected.index, targetIndex)
        temp = target.index
        target.index = selected.index
        selected.index = temp
        
    def addHeader(self):
        """Append a new contentHead to the list"""
        # Create a new contentHead devoid of settings
        newContentHead = contentHead(self.layout.count(), self)
        self.layout.addWidget(newContentHead)
        self.settings.setValue("num", self.layout.count())

        self.setLayout(self.layout)

        newContentHead.settingsWindow()
        newContentHead.window.apply.connect(lambda: self.append.emit(self.layout.count() - 1))


    def getSelectedBinary(self, x, y):
        """Get the item index of the content using binary search"""
        low = 0
        high = self.layout.count() - 1

        while low <= high:
            mid = floor((high + low) / 2)
        
            if self.layout.itemAt(mid).geometry().contains(x, y):
                return self.layout.itemAt(mid).widget()
            elif self.layout.itemAt(mid).geometry().y() < y:
                low = mid + 1
            elif self.layout.itemAt(mid).geometry().y() > y:
                high = mid - 1
        return None

    def deleteHead(self, index):
        """Deletes a contentHead from the row; assumes that the contentHead exists"""
        # Delete all references to the widget
        self.layout.itemAt(index).widget().close()
        self.layout.removeWidget(self.layout.itemAt(index).widget())
        self.deleteRow.emit(index)
        self.settings.setValue("num", self.layout.count())

    def renameHeads(self, start, end):
        """Rename all the contentHead ini files starting from the given index assuming the given setting file is neglible"""
        filePrefix = "contentHead"
        if end < 0:
            # Signals to rename to the end
            end = self.layout.count()
        if start >= end:
            step = -1
        else:
            step = 1
        # Shift the start position by 1 widget (rightward if moving right, leftward if moving left) 
        for i in range(start + step, end + step, step):
            os.rename(f"{filePrefix}{str(i)}.ini", f"{filePrefix}{str(i - step)}.ini")
            self.layout.itemAt(i - step).widget().index = i - step

    def hoverMoveEvent(self, event):
        print("Executing a hover move event on the widget.")

    def hoverEnterEvent(self, event):
        print("Executing a hover enter event on the widget.")

class headListScroll(QScrollArea):
    """QScrollArea built specifically for the headList and its dragging functions"""
    def __init__(self):
        super().__init__()

        self.thread = QThread()
        self.worker = None

        self.setFixedWidth(200)
        self.setWidgetResizable(True)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.horizontalScrollBar().setDisabled(True)
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
        self.setFrameShape(QFrame.Shape.NoFrame)

    def installWidget(self, widget):
        self.setWidget(widget)
        self.setFixedWidth(widget.width())
        self.setAcceptDrops(True)
        self.setMouseTracking(True)
        self.threshold = 0.15
        self.selected = None
        self.change = False
        self.widget = widget
        self.installEventFilter(self)
    
    def eventFilter(self, object, event):
        """Filter mouse events"""
        if object is self:
            if self.worker is not None:
                self.clearThread()
        return super().eventFilter(object, event)

    def mousePressEvent(self, event):
        """When the mouse left-clicks on a contentHead, store information about the item being moved"""
        if event.button() == Qt.MouseButton.LeftButton and self.widget.height():
            self.selected = self.widget.getSelectedBinary(event.position().x(), event.position().y() + (self.verticalScrollBar().value() / self.widget.height()) * self.widget.height())

    def mouseMoveEvent(self, event):
        """When the mouse moves and has selected a widget, enable dragging and dropping of the widget"""
        # If the user just selected a widget: (must initialize the drag instance)
        if event.buttons() & Qt.MouseButton.LeftButton and self.selected is not None:
            # Grab a pixmap of the full widget
            pixmapOpaque = self.selected.grab()

            # Create an empty transparent pixmap to paint on
            pixmap = QPixmap(self.selected.geometry().width(), self.selected.geometry().height())
            pixmap.fill(Qt.GlobalColor.transparent)

            # Paint in a transparent version of the widget to be dragged
            painter = QPainter(pixmap)
            painter.setOpacity(0.33)
            painter.drawPixmap(0, 0, pixmapOpaque)
            painter.end()

            mimedata = QMimeData()
            mimedata.setImageData(pixmap)

            self.dragged = QDrag(self.selected)
            self.dragged.setMimeData(mimedata)
            self.dragged.setPixmap(pixmap)

            # Set the drag image at the cursor location
            hotspotPos = QPoint(0, 0)
            self.dragged.setHotSpot(hotspotPos)
            self.dragged.exec()

            # Clear the instances after execution is over
            self.dragged = None
            self.selected = None

    def dragEnterEvent(self, event):
        """Display the cursor as accepting drag-and-drop events"""
        self.change = False
        event.accept()

    def dragMoveEvent(self, event):
        """As the dragged widget moves, show the preview of the contentRow"""
        if event.position().y() < self.height() * self.threshold:
            closeness = 1 - event.position().y() / (self.height() * self.threshold)
            self.worker = Worker(closeness)
            self.worker.moveToThread(self.thread)
            self.worker.ready.connect(self.weightedScroll)
            self.thread.start()
        elif event.position().y() > self.height() * (1 - self.threshold):
            closeness = -(event.position().y() - (self.height() * (1 - self.threshold))) / (self.height() * self.threshold)
            self.worker = Worker(closeness)
            self.worker.moveToThread(self.thread)
            self.worker.ready.connect(self.weightedScroll)
            self.thread.start()
        else:
            if self.worker is not None:
                self.clearThread()
            hovering = self.widget.getSelectedBinary(event.position().x(), event.position().y() + (self.verticalScrollBar().value() / self.widget.height()) * self.widget.height())

            if hovering is not None and self.selected is not None and hovering is not self.selected:
                # Re-arrange the layout:
                self.widget.rearrange(self.selected, hovering)
                self.change = True

    def weightedScroll(self, closeness):
        newValue = self.verticalScrollBar().value() - 10.0 * closeness
        if newValue < 0.0:
            newValue = 0.0
        elif newValue > self.widget.height():
            newValue = self.widget.height()
        self.verticalScrollBar().setValue(newValue)

    def dropEvent(self, event):
        """After the drag completes, save the settings"""
        # If there may have been a change to the layout, rewrite the settings
        if self.change:
            # Rename the dragged widget's settings to a temporary file
            os.rename(f"contentHead{self.selected.index}.ini", "temp.ini")
            # Rename all the involved files
            self.widget.renameHeads(self.selected.index, self.widget.layout.indexOf(self.selected))
            # Finalize the dragged widget's setting file name
            os.rename("temp.ini", f"contentHead{self.widget.layout.indexOf(self.selected)}.ini")

    def clearThread(self):
        self.thread.quit()
        self.thread.wait()
        self.worker = None

class Worker(QObject):
    ready = pyqtSignal(float)
    def __init__(self, closeness):
        super().__init__()
        self.closeness = closeness
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.proc)
        self.timer.start(10)

    def proc(self):
        print("PROC")
        self.ready.emit(self.closeness)

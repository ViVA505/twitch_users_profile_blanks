from PyQt5.QtWidgets import QPushButton, QColorDialog
from PyQt5.QtGui import QColor, QPainter, QBrush
from PyQt5.QtCore import Qt, pyqtSignal

class ColorButton(QPushButton):
    color_changed = pyqtSignal(tuple)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._color = QColor(255, 215, 0, 255)
        self.clicked.connect(self.choose_color)
        self.setMinimumSize(60, 30)

    def choose_color(self):
        color = QColorDialog.getColor(self._color, self)
        if color.isValid():
            self.set_color(color)
            self.color_changed.emit((
                color.red(),
                color.green(),
                color.blue(),
                color.alpha()
            ))

    def set_color(self, color):
        if isinstance(color, QColor):
            self._color = color
        else:
            self._color = QColor(*color)
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setBrush(QBrush(self._color))
        painter.drawRect(self.rect().adjusted(1, 1, -1, -1))
        painter.end()
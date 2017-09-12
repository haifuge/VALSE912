from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class VerticalLine(QWidget):
    def __init__(self, _width, _height, parent=None):
        super().__init__(parent)
        self.height=_height
        self.width=_width
        self.setMinimumSize(self.width,self.height)
        
    def paintEvent(self, qp):
        qp=QPainter()
        qp.begin(self)
        qp.setPen(QPen(QColor(0,0,0), 1, Qt.SolidLine));
        qp.drawLine(self.width/2, 0, self.width/2, self.height) 
        qp.end()

    def setHeight(self, _height):
        self.height=_height
        self.repaint()
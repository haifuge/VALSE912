from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from Common import CommonMethod
from Common import CommonTools

class MarkerButton(QPushButton):
    def __init__(self, parent=None, shape=CommonTools.Shape.square, color=CommonTools.Color.red):
        super().__init__(parent)
        self.resize(20,20)
        self.shape=shape
        self.color=color
    def paintEvent(self,e):
        qp=QPainter()
        qp.begin(self)
        CommonMethod.DrawMarker(10,10,qp,self.shape,self.color,16)
        qp.end()
    def SetColor(self, color):
        self.color=color
        self.repaint()
    def SetShape(self, shape):
        self.shape=shape
        self.repaint()
    def SetMarker(self, color, shape):
        self.color=color
        self.shape=shape
        self.repaint()
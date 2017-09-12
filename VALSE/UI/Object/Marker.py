import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from Common import CommonMethod
from Common import CommonTools

class Marker(QWidget):
    weight=1
    timeStamp=0
    def __init__(self, _color, _shape, _x=10, _y=10, _size=16, parent=None):
        super().__init__(parent)
        self.color=_color
        self.shape=_shape
        self.xPos=_x
        self.yPos=_y
        self.size=_size

        self.setMinimumSize(self.size,self.size) 
        #self.move(300,300)
        
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setStyleSheet("background:transparent")


    def paintEvent(self, e):
        qp=QPainter()
        qp.begin(self)
        CommonMethod.DrawMarker(self.xPos,self.yPos,qp,self.shape,self.color,self.size, self.weight)
        qp.end()
    def SetMarker(self, _color, _shape):
        self.color=_color
        self.shape=_shape
        self.repaint()
    def setPositionTip(self, tip):
        QToolTip.setFont(QFont('SansSerif',10))
        toolTip=tip
        self.setToolTip(toolTip)
    def setBold(self, _weight):
        self.weight=_weight
        self.repaint()


if __name__=='__main__':
    app=QApplication(sys.argv)
    ex=Marker(CommonTools.Color.red, CommonTools.Shape.square, 10,10)
    ex.show()
    sys.exit(app.exec_())


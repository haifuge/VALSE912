from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class EventGrid(QWidget):
    cWidth=30
    gridstep=0
    def __init__(self, _data=[]):
        super().__init__()
        self.data=_data
        self.initUI()

    def initUI(self):
        self.eventNum=len(self.data)
        self.rowHeight=50
        self.rowWidth=self.size().width()
        self.setMinimumHeight(120)
        
    def paintEvent(self, e):
        qp=QPainter()
        qp.begin(self)
        self.drawGrids(qp)
        qp.end()

    def drawGrids(self,qp):
        # row width
        width = self.size().width()
        cHeight=self.rowHeight
        height=self.eventNum*self.rowHeight
        # grid left blank margin
        
        # gird right position
        grWidth=int(width-15)
        qp.setPen(QPen(Qt.black, 1, Qt.SolidLine))
        
        # draw horizontal lines
        for i in range(self.eventNum):
            qp.drawLine(0, i*cHeight, width, i*cHeight)
        qp.drawLine(0, self.eventNum * cHeight-1, width, self.eventNum * cHeight-1)
        # width of each column
        self.gridstep = (width-45) * 0.1
        # draw vertical lines
        qp.setPen(QColor(210,210,222))
        for i in range(11):
            qp.drawLine(self.cWidth+i*self.gridstep, 0, self.cWidth+i*self.gridstep, self.eventNum * cHeight)
        # draw middle horizontal lines
        for i in range(self.eventNum):
            qp.drawLine(0,(i+0.5)*cHeight, width, (i+0.5)*cHeight)
        # draw left and right vertical lines and shadow area behind left and right button
        brush = QBrush(Qt.Dense6Pattern)
        pen = QPen(QColor(122, 122, 32))
        qp.setPen(pen)
        qp.setBrush(brush)
        qp.drawRect(self.cWidth, 0, self.leftXPos-self.cWidth, height)
        qp.drawRect(self.rightXPos,0,grWidth-self.rightXPos, height)

    def setLeftLineXPos(self, xPos):
        self.leftXPos=xPos
    def setRightLineXPos(self, xPos):
        self.rightXPos=xPos
    def getcWidth(self):
        return self.cWidth
    def getgridstep(self):
        return self.gridstep


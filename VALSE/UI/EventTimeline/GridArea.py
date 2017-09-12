from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from UI.EventTimeline import EventGrid
from UI.EventTimeline import DragButton
from Common import CommonMethod
from UI.EventTimeline import VerticalLine

class GridArea(QWidget):
    startTimeChanged=pyqtSignal(int)
    # grid time range
    timeRangeMin=0
    timeRangeMax=24*3600
    timeRange=24*3600
    # grid start time and end time
    startTime=0
    endTime=0
    # grid left blank width.
    lbWidth=0
    # grid column width
    columndWidth=0
    # tag for initializing left and right button position
    initialPosition=True
    def __init__(self, _data):
        super().__init__()
        self.data=_data
        self.initUI()

    def initUI(self):
        self.setContentsMargins(QMargins(0,0,0,0))
        self.widget=EventGrid.EventGrid(self.data)
        #self.widget.setGeometry(0,0,self.size().width(), self.widget.eventNum*self.widget.rowHeight)
        scroll=QScrollArea()
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        # scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll.setWidgetResizable(False)
        scroll.setContentsMargins(QMargins(0,0,0,0))
        scroll.setWidget(self.widget)
        vlayout=QVBoxLayout(self)
        vlayout.setContentsMargins(QMargins(0,0,0,0))
        vlayout.addWidget(scroll)
        self.setLayout(vlayout)

        # verticle line moves as time goes from left btn to right btn.
        self.vline=VerticalLine.VerticalLine(2,self.size().height(),self)
        self.vline.move(20,0)
        self.vline.setVisible(False)

        self.leftbtn=DragButton.DragButton("|", self)
        self.leftbtn.resize(10, 30)

        self.rightbtn=DragButton.DragButton("|", self)
        self.rightbtn.resize(10, 30)
        
        self.leftbtn.setRightBtn(self.rightbtn)
        self.rightbtn.setLeftBtn(self.leftbtn)
        self.leftbtn.mouseReleaseSignal.connect(self.leftbtnRelease)
        self.rightbtn.mouseReleaseSignal.connect(self.rightbtnRelease)
        self.leftbtn.mouseMoveSignal.connect(self.leftbtnMove)
        self.rightbtn.mouseMoveSignal.connect(self.rightbtnMove)

    # move verticle line right 1 unit
    # return False indicates reaching right btn, hide line, and stop timer; 
    # rerturn True indicates not reaching right btn and keep moving;
    moving=False
    def moveVLine(self):
        xpos=0
        if self.moving:
            xpos=self.vline.x()+1
            if xpos<self.rightbtn.x():
                self.vline.move(xpos,0)
            else:
                self.vline.setVisible(False)
                self.moving = False
        else:
            xpos=self.leftbtn.x()+self.leftbtn.size().width()-1
            self.vline.setVisible(True)
            self.vline.move(self.leftbtn.x()+self.leftbtn.size().width()-1,0)
            self.moving = True
        self.columndWidth=self.widget.getgridstep()
        x=(xpos-self.lbWidth)*self.timeRange/(10*self.columndWidth) 
        # change time to seconds
        vlineTime=int(x)+self.timeRangeMin
        return [self.moving, vlineTime]

    def resetVLine(self):
        self.vline.setVisible(False)
        self.vline.move(self.leftbtn.x()+self.leftbtn.size().width()-1,0)
        self.moving=False

    resizetimes=0
    def resizeEvent(self, QResizeEvent):

        self.vline.setHeight(self.size().height())

        gridwidth=self.size().width()-25
        self.widget.setGeometry(0, 0, gridwidth, self.widget.eventNum * self.widget.rowHeight)
        # set leftbtn and rightbtn position and moving range
        self.lbWidth=self.widget.getcWidth()
        leftRange=self.lbWidth-self.leftbtn.size().width()+2
        self.columndWidth=self.widget.getgridstep()
        rightRange=gridwidth*0.97
        yPos=self.size().height()/2-self.leftbtn.size().height()/2;
        self.leftbtn.setYpos(yPos)
        self.rightbtn.setYpos(yPos)
        self.resizetimes=self.resizetimes+1
        if self.initialPosition:
            self.leftbtn.move(leftRange, yPos)
            self.rightbtn.move(rightRange-self.rightbtn.x(), yPos)
            # calculate range is from self.lbWidth to self.size().width()-25-15, 25 is width of scrollbar, 15 is right blank 
            self.leftbtnXPosRatio = (self.leftbtn.x()+self.leftbtn.size().width()-self.lbWidth-2) / (gridwidth-self.lbWidth-15)
            self.rightbtnXPosRatio = (self.rightbtn.x()-self.lbWidth) / (gridwidth-self.lbWidth-15)
            self.initialPosition=False
        else:
            if self.resizetimes==2:
                self.leftbtn.move(leftRange,yPos)
                self.rightbtn.move(rightRange, yPos)
                self.leftbtnXPosRatio = (self.leftbtn.x()+self.leftbtn.size().width()-self.lbWidth-2) / (gridwidth-self.lbWidth-15)
                self.rightbtnXPosRatio = (self.rightbtn.x()-self.lbWidth) / (gridwidth-self.lbWidth-15)
            else:
                self.leftbtn.move(self.leftbtnXPosRatio*(gridwidth-self.lbWidth-15)+self.lbWidth-self.leftbtn.size().width()+2, yPos)
                self.rightbtn.move(self.rightbtnXPosRatio*(gridwidth-self.lbWidth-15)+self.lbWidth, yPos)
        self.leftbtn.setXrange(leftRange, self.rightbtn.x()-self.leftbtn.size().width()+0.5)
        self.rightbtn.setXrange(self.leftbtn.x()+self.leftbtn.size().width()-0.5, rightRange)
        self.widget.setRightLineXPos(self.rightbtn.x())
        self.widget.setLeftLineXPos(self.leftbtn.x()+self.leftbtn.size().width()-2)
        self.lbWidth=self.widget.getcWidth()
        self.columndWidth=self.widget.getgridstep()
        
    def leftbtnRelease(self):
        self.leftbtnXPosRatio = (self.leftbtn.x()+self.leftbtn.size().width()-self.lbWidth) / (self.size().width()-25-self.lbWidth-15)
        # as start time of grid changes, main window need to know when is start time so that it won't show markers before start time
        self.startTimeChanged.emit(self.startTime)

    def rightbtnRelease(self):
        self.rightbtnXPosRatio=(self.rightbtn.x()-self.lbWidth)/(self.size().width()-25-self.lbWidth-15)
        
    def leftbtnMove(self):
        self.vline.setVisible(False)
        self.moving = False
        self.widget.setLeftLineXPos(self.leftbtn.x()+self.leftbtn.size().width()-2)
        # show time as btn moves
        point=self.leftbtn.rect().topRight()
        global_point=self.leftbtn.mapToGlobal(point)
        self.columndWidth=self.widget.getgridstep()
        leftbtnPos=self.leftbtn.x()+self.leftbtn.size().width()-2;
        if leftbtnPos<self.lbWidth:
            self.startTime=self.timeRangeMin
        else:
            x=(leftbtnPos-self.lbWidth)*self.timeRange/(10*self.columndWidth)
            # change time to seconds
            self.startTime=int(x)+self.timeRangeMin
        QToolTip.showText(QPoint(global_point), CommonMethod.Second2Time(self.startTime))
        self.leftbtn.setToolTip(CommonMethod.Second2Time(self.startTime))

        self.widget.repaint()
        
    def rightbtnMove(self):
        self.vline.setVisible(False)
        self.moving = False
        self.widget.setRightLineXPos(self.rightbtn.x()+0.5)
        # show time as btn moves
        point=self.rightbtn.rect().topRight()
        self.columndWidth=self.widget.getgridstep()
        global_point=self.rightbtn.mapToGlobal(point)
        rightbtnPos=self.rightbtn.x()+0.5
        if rightbtnPos>(self.lbWidth+self.columndWidth*10):
            self.endTime=self.timeRangeMax
        else:
            x=(rightbtnPos-self.lbWidth)*self.timeRange/(10*self.columndWidth)
            # change time to seconds
            self.endTime=int(x)+self.timeRangeMin
        self.rightbtn.setToolTip(CommonMethod.Second2Time(self.endTime))
        QToolTip.showText(QPoint(global_point), CommonMethod.Second2Time(self.endTime))
        self.rightbtn.setToolTip(CommonMethod.Second2Time(self.endTime))

        self.widget.repaint()
    
    # sTime, eTime are second as type of int.
    def setTimeRange(self, sTime, eTime):
        self.timeRangeMin=sTime
        self.timeRangeMax=eTime
        self.timeRange=eTime-sTime

        self.columndWidth=self.widget.getgridstep()
        leftbtnPos=self.leftbtn.x()+self.leftbtn.size().width()-2;
        if leftbtnPos<self.lbWidth:
            self.startTime=self.timeRangeMin
        else:
            x=(leftbtnPos-self.lbWidth)*self.timeRange/(10*self.columndWidth)
            # change time to seconds
            self.startTime=int(x)+self.timeRangeMin

        rightbtnPos=self.rightbtn.x()+0.5
        if rightbtnPos>(self.lbWidth+self.columndWidth*10):
            self.endTime=self.timeRangeMax
        else:
            x=(rightbtnPos-self.lbWidth)*self.timeRange/(10*self.columndWidth)
            # change time to seconds
            self.endTime=int(x)+self.timeRangeMin

        self.leftbtn.setToolTip(CommonMethod.Second2Time(self.startTime))
        self.rightbtn.setToolTip(CommonMethod.Second2Time(self.endTime))

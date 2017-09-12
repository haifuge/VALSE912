from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from UI.EventTimeline import DragButton
from Common import CommonMethod

# the bottom timeline
class Tileline(QWidget):
    timeRangeChanged=pyqtSignal()
    # one unit of timeline
    timelineStep=0
    # timeline start time, seconds
    startTime=0
    # timelien end time, seconds
    endTime=24*3600
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # tag for initializing left and right button position
        self.initialPosition=True
        self.setContentsMargins(QMargins(0,0,0,0))
        self.setMinimumSize(350, 50)

        self.btn_y = 3
        self.leftbtn = DragButton.DragButton("|", self)
        self.leftbtn.resize(10, 20)
        self.leftbtn.setYpos(self.btn_y)

        self.rightbtn = DragButton.DragButton("|", self)
        self.rightbtn.resize(10, 20)
        self.rightbtn.setYpos(self.btn_y)

        self.leftbtn.setRightBtn(self.rightbtn)
        self.rightbtn.setLeftBtn(self.leftbtn)
        self.leftbtn.mouseReleaseSignal.connect(self.leftbtnRelease)
        self.rightbtn.mouseReleaseSignal.connect(self.rightbtnRelease)
        self.leftbtn.mouseMoveSignal.connect(self.leftbtnMove)
        self.rightbtn.mouseMoveSignal.connect(self.rightbtnMove)

    def resizeEvent(self, QResizeEvent):
        if self.initialPosition==True:
            self.leftbtn.move(0, self.btn_y)
            self.rightbtn.move(self.size().width()-10, self.btn_y)
            self.initialPosition=False
            self.leftbtnXPosRatio = self.leftbtn.x() / self.size().width()
            self.rightbtnXPosRatio = self.rightbtn.x() / self.size().width()
        else:
            self.rightbtn.move(self.rightbtnXPosRatio*self.size().width(), self.btn_y)
            self.leftbtn.move(self.leftbtnXPosRatio*self.size().width(), self.btn_y)
            self.rightbtn.setXrange(self.leftbtn.x()+self.leftbtn.size().width(), self.size().width()-self.rightbtn.size().width())
            self.leftbtn.setXrange(0, self.rightbtn.x()-self.leftbtn.size().width())

    def leftbtnRelease(self):
        self.leftbtnXPosRatio=self.leftbtn.x()/self.size().width()
            
    def rightbtnRelease(self):
        self.rightbtnXPosRatio=self.rightbtn.x()/self.size().width()
        

    def leftbtnMove(self):
        leftbtnPos=self.leftbtn.x()+self.leftbtn.size().width();
        if leftbtnPos<self.timelineStep:
            self.startTime=0.0
        else:
            x=(leftbtnPos-self.timelineStep)/self.timelineStep
            # change time to seconds
            self.startTime=int(x*3600)
        # inform grid that time range is changed
        self.timeRangeChanged.emit()
        point=self.leftbtn.rect().topRight()
        global_point=self.leftbtn.mapToGlobal(point)
        QToolTip.showText(QPoint(global_point), CommonMethod.Second2Time(self.startTime))
        self.leftbtn.setToolTip(CommonMethod.Second2Time(self.startTime))
        
        self.repaint()

    def rightbtnMove(self):
        if self.rightbtn.x()>self.timelineStep*25:
            self.endTime=24.0*3600
        else:
            x=(self.rightbtn.x()-self.timelineStep)/self.timelineStep
            # change time to seconds
            self.endTime=int(x*3600)
        self.timeRangeChanged.emit()
        point=self.rightbtn.rect().topRight()
        global_point=self.rightbtn.mapToGlobal(point)
        QToolTip.showText(QPoint(global_point), CommonMethod.Second2Time(self.endTime))
        self.rightbtn.setToolTip(CommonMethod.Second2Time(self.endTime))
        
        self.repaint()

    def getTimePeriodRange(self):
        return (self.startTime, self.endTime)

    def paintEvent(self, e):
        qp=QPainter()
        qp.begin(self)
        self.drawTimeline(qp)
        self.drawShadowArea(qp)
        qp.end()

    def drawShadowArea(self, qp):
        brush = QBrush(Qt.Dense6Pattern)
        pen = QPen(QColor(122, 122, 32))
        qp.setPen(pen)
        qp.setBrush(brush)
        qp.drawRect(0, 0, self.leftbtn.x()+self.leftbtn.size().width()-1, self.size().height()/2)
        qp.drawRect(self.rightbtn.x(),0,self.size().width()-self.rightbtn.x(), self.size().height()/2)

    def drawTimeline(self, qp):
        #borderPen=QPen(QColor(255,255,255), 2, Qt.SolidLine)
        width=self.size().width()
        height=self.size().height()
        # draw timeline
        timeline_y=self.size().height()/2
        qp.drawLine(0, timeline_y, width, timeline_y)
        self.timelineStep=width/26
        timelineNumbers=['00:00','04:00','08:00','12:00','16:00','20:00','24:00']
        self.start_x=self.timelineStep
        for i in range(0,25):
            j=i%4
            if(j==0):
                qp.setFont(QFont('Lucida',7))
                metrics = qp.fontMetrics()
                fw = metrics.width(timelineNumbers[int(i/4)])
                qp.drawText(self.timelineStep*i+self.start_x - fw / 2, timeline_y+20, timelineNumbers[int(i/4)])
                qp.drawLine(self.timelineStep * (i) + self.start_x, timeline_y, self.timelineStep * (i) + self.start_x,
                            timeline_y + 7)
            else:
                qp.drawLine(self.timelineStep * (i) + self.start_x, timeline_y, self.timelineStep * (i) + self.start_x,
                            timeline_y + 4)



import sys
import time
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from UI.EventTimeline import GridArea
from UI.EventTimeline import Tileline
from Common import CommonMethod

class TimeLine(QWidget):
    timeSignal=pyqtSignal(int)
    startTimeChanged=pyqtSignal(int)
    resetSignal=pyqtSignal()
    def __init__(self, _data=[]):
        super().__init__()
        self.data=_data
        self.initUI()
    def initUI(self):
        self.setMinimumSize(500,270)
        #self.setFixedSize(500,270)
        self.tab=QTabWidget(self)
        self.tab.move(0,0)
        self.tab.size().width=self.size().width()
        self.tab.size().height=self.size().height()
        verfiedTab=VerifiedTab(self.data)
        self.tab.addTab(verfiedTab,"Verified")
        verfiedTab.timeSignal.connect(self.timeSignalChanging)
        verfiedTab.startTimeChanged.connect(self.onStartTimeChanged)
        verfiedTab.resetSignal.connect(self.onResetSignal) 
        #unverifiedTab=VerifiedTab(self.data)
        #self.tab.addTab(unverifiedTab,"Unverified")

    def timeSignalChanging(self, time):
        self.timeSignal.emit(time)

    def onStartTimeChanged(self, stime):
        self.startTimeChanged.emit(stime)

    def resizeEvent(self, e):
        self.tab.resize(e.size()+QSize(1,1))

    def onResetSignal(self):
        self.resetSignal.emit()

class VerifiedTab(QWidget):
    timeSignal=pyqtSignal(int)
    startTimeChanged=pyqtSignal(int)
    resetSignal=pyqtSignal()
    def __init__(self, _data=[]):
        super().__init__()
        self.data=_data
        self.initUI()

    def initUI(self):
        self.originalSpeed=100
        self.speed=100
        self.speedTimes=1.0
        self.start=False
        self.timer=QTimer()
        self.timer.setInterval(self.speed)
        self.timer.timeout.connect(self.timerTick)

        palette=self.palette()
        palette.setColor(self.backgroundRole(), Qt.white)
        self.setPalette(palette)
        
        self.hlb=QHBoxLayout()
        self.hlb.setSizeConstraint(QLayout.SetFixedSize)
        self.hlb.setContentsMargins(QMargins(5,5,0,5))
        self.playbtn=QPushButton()
        self.playbtn.setIcon(QIcon(r'Pictures/play.png'))
        self.playbtn.clicked.connect(self.playbtnClicked)
        self.stopbtn=QPushButton()
        self.stopbtn.setIcon(QIcon(r'Pictures/stop.png'))
        self.stopbtn.clicked.connect(self.timerReset)
        self.fforwardbtn=QPushButton()
        self.fforwardbtn.setIcon(QIcon(r'Pictures/fforward.png'))
        self.fforwardbtn.clicked.connect(self.timerSpeedUp)
        self.freversebtn=QPushButton()
        self.freversebtn.setIcon(QIcon(r'Pictures/freverse.png'))
        self.freversebtn.clicked.connect(self.timerSlowDown)

        self.hlb.addWidget(self.freversebtn)
        self.hlb.addWidget(self.playbtn)
        self.hlb.addWidget(self.stopbtn)
        self.hlb.addWidget(self.fforwardbtn)
        self.hlb.addStretch(1)

        self.lblTime=QLabel()
        self.lblTime.setText('00:00:00')
        self.lblTime.setContentsMargins(QMargins(0,0,20,0))
        self.hlb.addWidget(self.lblTime)

        self.vlb=QVBoxLayout()
        self.vlb.setSpacing(0)
        self.vlb.setContentsMargins(QMargins(0,0,0,0))
        self.vlb.addLayout(self.hlb)
        self.grid=GridArea.GridArea(self.data)
        self.grid.startTimeChanged.connect(self.onStartTimeChanged)
        self.grid.setGeometry(0,0,self.size().width(),self.size().height() - 15)
        self.vlb.addWidget(self.grid)

        self.timeline=Tileline.Tileline()
        self.timeline.setGeometry(0, 0, self.size().width(), 20)
        self.timeline.timeRangeChanged.connect(self.timeRangeChanging)
        self.vlb.addWidget(self.timeline)

        self.setLayout(self.vlb)

    def onStartTimeChanged(self, sTime):
        self.startTimeChanged.emit(sTime)

    def timerTick(self):
        if self.keepMoving:
            # [True/False, time of moving vertical line]
            result=self.grid.moveVLine()
            self.keepMoving=result[0]
            #print(CommonMethod.Second2Time(result[1]))
            self.timeSignal.emit(result[1]*1000)
            self.lblTime.setText(CommonMethod.Second2Time(result[1]))
        else:
            self.start=False
            self.timer.stop()
            self.playbtn.setIcon(QIcon(r'Pictures/play.png'))


    def playbtnClicked(self):
        if self.start:
            self.start=False
            self.timer.stop()
            self.playbtn.setIcon(QIcon(r'Pictures/play.png'))
        else:
            self.start=True
            self.keepMoving=True
            self.timer.start()
            self.playbtn.setIcon(QIcon(r'Pictures/pause.png'))

    def timerReset(self):
        self.timer.stop()
        self.playbtn.setIcon(QIcon(r'Pictures/play.png'))
        self.grid.resetVLine()
        self.resetSignal.emit()

    def timerSpeedUp(self):
        self.speedTimes=self.speedTimes/2
        self.speed=self.originalSpeed*self.speedTimes
        self.timer.setInterval(self.speed)

    def timerSlowDown(self):
        self.speedTimes = self.speedTimes * 2
        self.speed=self.originalSpeed*self.speedTimes
        self.timer.setInterval(self.speed)

    def timeRangeChanging(self):
        value=self.timeline.getTimePeriodRange()
        self.startTime=value[0]
        self.endTime=value[1]
        self.grid.setTimeRange(self.startTime, self.endTime)
        
    def SetData(self, _data):
        self.data=_data

if __name__=='__main__':
    app=QApplication(sys.argv)
    ex=TimeLine([1,2,3])
    #ex=GridArea()
    #ex=EventGrid()
    # ex=TestDragButton()
    #ex=Tileline()
    ex.show()
    sys.exit(app.exec_())
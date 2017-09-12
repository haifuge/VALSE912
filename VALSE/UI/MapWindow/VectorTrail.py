import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from Common import CommonMethod
from Common import CommonTools
from UI.Object import Marker
import copy

class VectorTrail(QWidget):
    max_x=300.0
    max_y=300.0
    width=600.0
    height=400.0
    x_ratio=1.0
    y_ratio=1.0
    map_path=''
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setMinimumSize(self.width, self.height)
        #self.map=QPixmap('Maps/testMap.png')
        self.setWindowTitle('Map')
        #self.initTimer()
        self.lmap=Map(self)
        self.lmap.setImage('Maps/testMap.png');
        self.lmap.setScaledContents(True)
        self.lmap.resize(self.width,self.height)
        self.lmap.move(0,0)

        # test for visible and highlight marker
        #marker=Marker.Marker(CommonTools.Color.red, CommonTools.Shape.circle, 10,10, 10, self)
        #marker.move(100,100)
        #marker.setVisible(True)
        #marker.setPositionTip('100, 100')
        #marker.setBold(2)
        #marker.setBold(1)

        #marker3=Marker.Marker(CommonTools.Color.green, CommonTools.Shape.circle,10,10,10,self)
        #marker3.move(150,100)
        #marker3.setVisible(True)
        #marker3.setPositionTip('150, 100')

        #marker2=Marker.Marker(CommonTools.Color.blue, CommonTools.Shape.circle,10,10,10,self)
        #marker2.move(200,100)
        #marker2.setVisible(True)
        #marker2.setPositionTip('200, 100')

        #end test

    def SetMap(self,  maxx, maxy, map_path):
        self.max_x=maxx
        self.max_y=maxy
        self.x_ratio=self.max_x/self.width
        self.y_ratio=self.max_y/self.height
        
        self.lmap.setImage('Maps/'+map_path);
        print(self.lmap.imgHeight, self.lmap.imgWidth)
        self.x_ratio=self.lmap.imgWidth/self.max_x
        self.y_ratio=self.lmap.imgHeight/self.max_y
        self.lmap.setScaledContents(True)
        self.lmap.resize(self.width,self.height)
        self.lmap.move(0,0)

    def SetSize(self, _width, _height):
        self.width=_width
        self.height=_height;
        self.resize(self.width,self.height)
        
    def resizeEvent(self, e):
        self.lmap.resize(self.size())
        self.x_ratio=self.lmap.imgWidth/self.max_x
        self.y_ratio=self.lmap.imgHeight/self.max_y

    def initTimer(self):
        self.timer=QTimer()
        self.timer.setInterval(500)
        self.timer.timeout.connect(self.click)
        self.i=1
        self.n=10
        self.step=30
        self.setFixedSize(self.size())
        self.timer.start()

    def click(self):
        self.repaint()
        self.i=self.i+1
        if self.i==self.n:
            self.timer.stop()
            self.setFixedSize(QWIDGETSIZE_MAX, QWIDGETSIZE_MAX)

    def SetData(self, _data):
        self.data=_data

    def drawMarkers(self):
        for p in self.data:
            p.markers=[]
            for d in p.data:
                # copy.deepcopy(p.marker)
                marker=Marker.Marker(p.color, p.shape,10,10,12,self)
                marker.move(d[0]*self.x_ratio,d[1]*self.y_ratio)
                marker.setVisible(False)
                marker.timeStamp=d[2]
                p.markers.append(marker)

    def changeMarker(self, changes):
        if changes[1]=='marker':
            for p in self.data:
                if changes[0]==p.id:
                    for m in p.markers:
                        m.SetMarker(changes[2], changes[3])
        elif changes[1]=='visible':
            for p in self.data:
                if changes[0]==p.id:
                    for m in p.markers:
                        m.setVisible(changes[2])
        elif changes[1]=='light':
            for p in self.data:
                if changes[0]==p.id:
                    for m in p.markers:
                        m.setBold(2 if changes[2] else 1)
    def setStartTime(self, sTime):
        self.startTime=sTime
        for p in self.data:
            for i in range(len(p.markers)):
                if self.startTime>p.markers[i].timeStamp:
                    p.index=i-1;
                    break;
    # show markers from current index to time
    # index is 0 default, or number of last shown marker
    def showMarkers(self, time):
        for p in self.data:
            for i in range(p.index, len(p.markers)):
                if time>=int(p.markers[i].timeStamp):
                    p.markers[i].setVisible(True)
                else:
                    p.index=i
                    break
    def hideAllMarkers(self):
        for p in self.data:
            for m in p.markers:
                m.setVisible(False)

class Map(QLabel):

    def __init__(self, parent=None):
        super().__init__(parent);
        
    def setMapInfo(self, _mapData):
        self.mapData=_mapData;

    def setImage(self, path):
        self.img=QPixmap(path)
        self.imgWidth=self.img.size().width()
        self.imgHeight=self.img.size().height()

    def setData(self, arr):
        self.positions=arr;

    def paintEvent(self, e):
        qp=QPainter()
        qp.begin(self)
        #CommonMethod.DrawMarker(self.i*self.step, self.i*self.step, qp, CommonTools.Shape.cross, CommonTools.Color.red, 15)
        #qp.setPen(QPen(QColor.black))
        qp.drawPixmap(0,0,self.pix)
        #qp.drawRect(10,10,10,10)
        qp.end()
    
    def resizeEvent(self, e):
        self.pix=self.img.scaled(self.size(),Qt.IgnoreAspectRatio, Qt.SmoothTransformation)

    def Draw(self, timestamp):
        self.timestamp=timestamp
        self.repaint()

if __name__=='__main__':
    app=QApplication(sys.argv)
    ex=VectorTrail()
    ex.show()
    sys.exit(app.exec_())
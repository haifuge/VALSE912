import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from UI.EventTimeline import TimeLine
from UI.DateMenu import DateMenu
from UI.Sidebar import PeopleSidebar
from UI.MapWindow import VectorTrail
from Common import DBOperation
from UI.Object import Person
from Common import CommonTools

class MainWindow(QMainWindow):
    count=0
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('VALSE')
        self.resize(1200, 700)
        self.mdi=QMdiArea()
        self.setCentralWidget(self.mdi)
        bar=self.menuBar()
        file=bar.addMenu("File")
        file.addAction("New")
        file.addAction("Cascade")
        file.addAction("Tiled")
        file.triggered[QAction].connect(self.windowAction)

        datePanel=bar.addMenu("Date Panel")
        datePanel.addAction("Show Date Panel")
        datePanel.triggered[QAction].connect(self.windowAction)

        sidebars=bar.addMenu("Sidebars")
        sidebars.addAction("People")
        sidebars.triggered[QAction].connect(self.windowAction)

        map=bar.addMenu("Map")
        map.addAction("Map")
        map.triggered[QAction].connect(self.windowAction)

        

    def windowAction(self, q):
        if q.text()=="New":
            self.count=self.count+1
            sub=QMdiSubWindow()
            sub.setWidget(TimeLine.TimeLine())
            sub.setWindowTitle("TimeLine")
            self.mdi.addSubWindow(sub)
            sub.show()
        if q.text()=='Cascade':
            self.mdi.cascadeSubWindows()
        if q.text()=='Titled':
            self.mdi.tileSubWindows()
        if q.text()=='Show Date Panel':
            self.dateMenu=QMdiSubWindow()
            self.dateWindow=DateMenu.DateMenu()
            self.dateWindow.closeSignal.connect(self.dateWindowClose)
            self.dateMenu.setWidget(self.dateWindow)
            self.dateMenu.setWindowTitle("Date Selection")
            self.dateMenu.setWindowFlags(Qt.Window | Qt.WindowTitleHint | Qt.CustomizeWindowHint)
            self.dateMenu.setMaximumWidth(265)
            self.dateMenu.setMaximumHeight(340)
            self.mdi.addSubWindow(self.dateMenu)
            self.dateMenu.show()
        if q.text()=='People':
            peoplesb=QMdiSubWindow()
            peoplesb.setWidget(PeopleSidebar.PeopleSidebar())
            peoplesb.setWindowFlags(Qt.Window | Qt.WindowTitleHint | Qt.CustomizeWindowHint)
            peoplesb.setMaximumWidth(265)
            self.mdi.addSubWindow(peoplesb)
            peoplesb.show()
        if q.text()=='Map':
            mapWindow=QMdiSubWindow()
            mapWindow.setWidget(VectorTrail.VectorTrail())
            mapWindow.setWindowFlags(Qt.Window|Qt.WindowTitleHint|Qt.CustomizeWindowHint)
            self.mdi.addSubWindow(mapWindow)
            mapWindow.show()


    def dateWindowClose(self, l):
        # [startDate, endDate, weekday, location]
        print('main: ',l)
        self.dateInfo=l
        self.dateMenu.close()
        if len(l)==1:
            pass
        else:
            self.getData()

    def getData(self):
        dbop=DBOperation.DBOperator()
        self.mapInfo=dbop.ExecSql('select location_id, max_x, max_y, map_url from location where name=\''+self.dateInfo[3]+'\';',4)
        location_id=str(self.mapInfo[0][0])
        sql=''
        bsql=' {} select d.target_id, d.x, d.y, d.ts-{} from target t, detection d where t.location_id={} and t.target_id=d.target_id and d.ts between {} and {} '
        if self.dateInfo[2][0]==1:
            # date time to long 
            startDate=QDateTime.fromString(self.dateInfo[0],'MM/dd/yyyy').toOffsetFromUtc(QDateTime().offsetFromUtc()).toMSecsSinceEpoch()
            endDate=QDateTime.fromString(self.dateInfo[1],'MM/dd/yyyy').addDays(1).toOffsetFromUtc(QDateTime().offsetFromUtc()).toMSecsSinceEpoch()
            sql=bsql.format('', str(startDate), location_id, str(startDate), str(endDate))
        else:
            # cusomize date
            startDate=QDate.fromString(self.dateInfo[0],'MM/dd/yyyy')
            endDate=QDate.fromString(self.dateInfo[1],'MM/dd/yyyy').addDays(1)
            sql='select target_id, x, y, ts from detection where target_id=-1 '
            if len(self.dateInfo[2])==7 or len(self.dateInfo[2])==31:
                # weekly, monthly count by day
                t=startDate
                while t<endDate:
                    if self.dateInfo[2][t.dayOfWeek()-1]!=0:
                        sDate=QDateTime(t).toOffsetFromUtc(QDateTime().offsetFromUtc()).toMSecsSinceEpoch()
                        eDate=QDateTime(t.addDays(1)).toOffsetFromUtc(QDateTime().offsetFromUtc()).toMSecsSinceEpoch()
                        sql+=bsql.format(' union all ', str(startDate), location_id, str(startDate), str(endDate))
                    t=t.addDays(1)
                
            elif len(self.dateInfo[2])==12:
                # yearly count by month
                # deal with first month of date period
                if self.dateInfo[2][startDate.month()-1]!=0:
                        sDate=QDateTime(startDate).toOffsetFromUtc(QDateTime().offsetFromUtc()).toMSecsSinceEpoch()
                        eDate=QDateTime(startDate.year(), startDate.month()+1, 1, 0,0).toOffsetFromUtc(QDateTime().offsetFromUtc()).toMSecsSinceEpoch()
                        if eDate>endDate.toOffsetFromUtc(QDateTime().offsetFromUtc()).toMSecsSinceEpoch():
                            eDate=endDate.toOffsetFromUtc(QDateTime().offsetFromUtc()).toMSecsSinceEpoch()
                        sql+=bsql.format(' union all ', str(startDate), location_id, str(startDate), str(endDate))
                t=startDate.addMonths(1)
                t=QDate(t.year(), t.month(), t.day())
                while t<endDate:
                    if t.month()==endDate.month():
                        break;
                    if self.dateInfo[2][t.month()-1]!=0:
                        sDate=QDateTime(t).toOffsetFromUtc(QDateTime().offsetFromUtc()).toMSecsSinceEpoch()
                        eDate=QDateTime(t.year, startDate.month+1, 1, 0,0).toOffsetFromUtc(QDateTime().offsetFromUtc()).toMSecsSinceEpoch()
                        sql+=bsql.format(' union all ', str(startDate), location_id, str(startDate), str(endDate))
                    t=t.addMonths(1)
                # deal with last month of date period
                if self.dateInfo[2][t.month()-1]!=0:
                    sDate=QDateTime(t).toOffsetFromUtc(QDateTime().offsetFromUtc()).toMSecsSinceEpoch()
                    eDate=QDateTime(endDate).toOffsetFromUtc(QDateTime().offsetFromUtc()).toMSecsSinceEpoch()
                    sql+=bsql.format(' union all ', str(startDate), location_id, str(startDate), str(endDate))
        self.objInfo=dbop.ExecSql(sql, 4)
        # [target_id, x, y, timestamp]
        #print(self.objInfo)
        persons, personsData = self.processData(self.objInfo)

        # show people item
        peoplesb=QMdiSubWindow()
        psb=PeopleSidebar.PeopleSidebar()
        psb.SetObjectData(persons)
        psb.peopleItemChanged.connect(self.sidebarItemChanged)
        peoplesb.setWidget(psb)
        peoplesb.setWindowFlags(Qt.Window | Qt.WindowTitleHint | Qt.CustomizeWindowHint)
        peoplesb.setMaximumWidth(265)
        self.mdi.addSubWindow(peoplesb)
        peoplesb.show()

        # show map
        mapWindow=QMdiSubWindow()
        #mapWindow.resize(500,300)
        self.mapContent=VectorTrail.VectorTrail()
        self.mapContent.SetMap(self.mapInfo[0][1], self.mapInfo[0][2], self.mapInfo[0][3])
        self.mapContent.SetData(personsData)
        self.mapContent.drawMarkers()
        #mapContent.SetSize(500,300);
        mapWindow.setWidget(self.mapContent)
        mapWindow.setWindowFlags(Qt.Window|Qt.WindowTitleHint|Qt.CustomizeWindowHint)
        self.mdi.addSubWindow(mapWindow)
        mapWindow.show()

        # show timeline
        sub=QMdiSubWindow()
        self.timeline=TimeLine.TimeLine(personsData)
        self.timeline.timeSignal.connect(self.showingMarkers)
        self.timeline.startTimeChanged.connect(self.startTimeChanged)
        self.timeline.resetSignal.connect(self.resetMap)
        sub.setWidget(self.timeline)
        sub.setWindowTitle("TimeLine")
        self.mdi.addSubWindow(sub)
        sub.show()

    def showingMarkers(self, timeStamp):
        self.mapContent.showMarkers(timeStamp)
        #print(timeStamp)
    def startTimeChanged(self, sTime):
        self.mapContent.setStartTime(sTime)
        print(sTime)

    def resetMap(self):
        self.mapContent.hideAllMarkers() 

    def sidebarItemChanged(self, changes):
        #[id, changename, value]
        self.mapContent.changeMarker(changes)
        #self.timeline.changeMarker(changes)

    # convert data[] to object[] (Person[])
    def processData(self, data):
        # [target_id, x, y, timestamp]
        # sidebar data [id, name, color, shape], id to identify whose name has been changed, that equals to k of personsData[0].name('Person'+k)
        persons=[]
        # map data [(id, name, color, shape, [x, y, time ... ]), ...]
        personsData=[]
        dId=-1
        k=1
        for i in range(len(data)):
            if dId!=data[i][0]:
                dId=data[i][0]
                p=Person.Person(dId, 'Person'+str(k), CommonTools.marks[k][0], CommonTools.marks[k][1])
                p.data=[]
                p.data.append([data[i][1], data[i][2], data[i][3]])
                personsData.append(p)
                persons.append([dId, 'Person'+str(k), CommonTools.marks[k][0], CommonTools.marks[k][1]])
                k=k+1
            else:
                p.data.append([data[i][1], data[i][2], data[i][3]])
        #print(persons)
        #print(personsData)
        return persons, personsData


if __name__=='__main__':
    app=QApplication(sys.argv)
    ex=MainWindow()
    ex.show()
    sys.exit(app.exec_())

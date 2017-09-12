from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class DateSelector(QDialog):
    signal=pyqtSignal(str)
    def __init__(self, parent=None):
        super().__init__()
        self.initUI()
    def initUI(self):
        self.cal=QCalendarWidget(self)
        self.cal.setGridVisible(True)
        self.cal.setGeometry(0,0,390,250)
        self.cal.clicked[QDate].connect(self.emitDate)
        self.lbl=QLabel(self)
        self.resize(self.cal.size())
        self.setWindowTitle('Calendar')
    def emitDate(self, date):
        self.close()
        self.signal.emit(date.toString('MM/dd/yyyy'))
    def setPosition(self, x,y):
        self.move(x,y)
    def setDate(self, sdate):
        self.cal.setSelectedDate(QDate.fromString(sdate,'MM/dd/yyyy'));

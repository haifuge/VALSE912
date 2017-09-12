from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

# custom panel, buttons of 7-day panel
class WeeklySelectionPanel(QWidget):
    customDays=[0,0,0,0,0,0,0]
    def __init__(self):
        super().__init__()
        self.initUI()
    def initUI(self):
        self.setMinimumSize(220,80)
        self.setMaximumSize(220,80)
        btnsTxt=['S','M','T','W','T','F','S']
        lblevery=QLabel(self)
        lblevery.setText('Every')
        lblevery.move(10,5)
        lblevery.adjustSize()
        self.txtTimes=QTextEdit(self)
        self.txtTimes.move(45,1)
        self.txtTimes.resize(QSize(35,28))
        self.txtTimes.setText('1')
        lblUnit=QLabel(self)
        lblUnit.setText('week(s) on:')
        lblUnit.move(85,5)
        lblUnit.adjustSize()
        a=25
        btns=[]
        self.btnSun=QPushButton(self)
        self.btnSun.clicked.connect(lambda: self.weekClicked(0))
        self.btnMon=QPushButton(self)
        self.btnMon.clicked.connect(lambda: self.weekClicked(1))
        self.btnTue=QPushButton(self)
        self.btnTue.clicked.connect(lambda: self.weekClicked(2))
        self.btnWed=QPushButton(self)
        self.btnWed.clicked.connect(lambda: self.weekClicked(3))
        self.btnThu=QPushButton(self)
        self.btnThu.clicked.connect(lambda: self.weekClicked(4))
        self.btnFri=QPushButton(self)
        self.btnFri.clicked.connect(lambda: self.weekClicked(5))
        self.btnSat=QPushButton(self)
        self.btnSat.clicked.connect(lambda: self.weekClicked(6))
        btns=[self.btnSun, self.btnMon,self.btnTue,self.btnWed,self.btnThu,self.btnFri,self.btnSat]
        for i in range(len(btns)):
            btns[i].setText(btnsTxt[i])
            btns[i].setCheckable(True)
            btns[i].resize(QSize(a,a))
            btns[i].move(25+i*27, 40)
        
    def weekClicked(self, n):
        s=self.sender()
        if s.isChecked():
            self.customDays[n]=n
        else:
            self.customDays[n]=0
    def getTimes(self):
        return self.txtTimes.toPlainText()

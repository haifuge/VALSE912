from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


#custom panel, buttons of 12-month 
class YearlySelectionPanel(QWidget):
    customDays=[0,0,0,0,0,0,
                0,0,0,0,0,0]
    def __init__(self):
        super().__init__()
        self.initUI()
    def initUI(self):
        self.setMinimumSize(220,170)
        self.setMaximumSize(220,170)
        lblevery=QLabel(self)
        lblevery.setText('Every')
        lblevery.move(10,5)
        lblevery.adjustSize()
        self.txtTimes=QTextEdit(self)
        self.txtTimes.move(45,1)
        self.txtTimes.resize(QSize(35,28))
        self.txtTimes.setText('1')
        lblUnit=QLabel(self)
        lblUnit.setText('year(s) on:')
        lblUnit.move(85,5)
        lblUnit.adjustSize()
        btnsTxt=['JAN','FEB','MAR','APR','MAY','JUN',
                 'JUL','AUG','SEP','OCT','NOV','DEC']
        a=40
        btns=[]
        self.btnJan=QPushButton(self)
        self.btnJan.clicked.connect(lambda: self.weekClicked(0))
        self.btnFeb=QPushButton(self)
        self.btnFeb.clicked.connect(lambda: self.weekClicked(1))
        self.btnMar=QPushButton(self)
        self.btnMar.clicked.connect(lambda: self.weekClicked(2))
        self.btnApr=QPushButton(self)
        self.btnApr.clicked.connect(lambda: self.weekClicked(3))
        self.btnMay=QPushButton(self)
        self.btnMay.clicked.connect(lambda: self.weekClicked(4))
        self.btnJun=QPushButton(self)
        self.btnJun.clicked.connect(lambda: self.weekClicked(5))
        self.btnJul=QPushButton(self)
        self.btnJul.clicked.connect(lambda: self.weekClicked(6))
        self.btnAug=QPushButton(self)
        self.btnAug.clicked.connect(lambda: self.weekClicked(7))
        self.btnSep=QPushButton(self)
        self.btnSep.clicked.connect(lambda: self.weekClicked(8))
        self.btnOct=QPushButton(self)
        self.btnOct.clicked.connect(lambda: self.weekClicked(9))
        self.btnNov=QPushButton(self)
        self.btnNov.clicked.connect(lambda: self.weekClicked(10))
        self.btnDec=QPushButton(self)
        self.btnDec.clicked.connect(lambda: self.weekClicked(11))
        btns=[self.btnJan, self.btnFeb, self.btnMar, self.btnApr, self.btnMay, self.btnJun,
              self.btnJul, self.btnAug, self.btnSep, self.btnOct, self.btnNov, self.btnDec]
        for i in range(len(btns)):
            btns[i].setText(btnsTxt[i])
            btns[i].setCheckable(True)
            btns[i].resize(QSize(a,a))
            btns[i].move(25+(i%4)*42, 40+42*(i//4))

    def weekClicked(self, n):
        s=self.sender()
        if s.isChecked():
            self.customDays[n]=n
        else:
            self.customDays[n]=0
    def getTimes(self):
        return self.txtTimes.toPlainText()

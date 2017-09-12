from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from UI.DateMenu import FrequencySelectionBtns
from UI.DateMenu import WeeklySelectionPanel
from UI.DateMenu import MonthlySelectionPanel
from UI.DateMenu import YearlySelectionPanel

class CustomFrequencyPanel(QDialog):
    # weekly height
    weeklyHeight=230
    monthlyHeight=380
    yearlyHeight=350
    signal=pyqtSignal(list)
    def __init__(self, parent=None):
        super().__init__()
        self.initUI()
    def initUI(self):
        self.vlayout=QVBoxLayout()
        self.h1layout=QHBoxLayout()
        self.cf=FrequencySelectionBtns.FrequencySelectionBtns()
        self.cf.resize(QSize(250,160))
        self.cf.daysSelection[str].connect(self.daysSelected)
        self.h1layout.addWidget(self.cf)
        self.h1layout.setSizeConstraint(QLayout.SetFixedSize)
        self.vlayout.addLayout(self.h1layout)

        self.ws=WeeklySelectionPanel.WeeklySelectionPanel()
        self.vlayout.addWidget(self.ws)
        self.vlayout.addStretch(1)
        self.hlayout=QHBoxLayout()
        self.btnCancel=QPushButton()
        self.btnCancel.setText('Cancel')
        self.btnCancel.resize(QSize(60,27))
        self.btnCancel.clicked.connect(self.btnClicked)
        self.hlayout.addWidget(self.btnCancel)
        self.hlayout.addStretch(1)
        self.btnConfirm=QPushButton()
        self.btnConfirm.setText('Confirm')
        self.btnConfirm.resize(QSize(60,27))
        self.btnConfirm.clicked.connect(self.btnClicked)
        self.hlayout.addWidget(self.btnConfirm)
        self.vlayout.addLayout(self.hlayout)
        self.setLayout(self.vlayout)
        
    def daysSelected(self, days):
        self.vlayout.removeWidget(self.ws)
        self.ws.deleteLater()
        self.ws=None
        if days=='weekly':
            self.ws=WeeklySelectionPanel.WeeklySelectionPanel()
        if days=='monthly':
            self.ws=MonthlySelectionPanel.MonthlySelectionPanel()
        if days=='yearly':
            self.ws=YearlySelectionPanel.YearlySelectionPanel()
        self.vlayout.insertWidget(1,self.ws)
        self.resize(QSize(220,200))

    def setPosition(self, x,y):
        self.move(x,y)
    def btnClicked(self):
        s=self.sender()
        if s==self.btnCancel:
            self.close()
        if s==self.btnConfirm:
            self.close()
            frequency=self.ws.customDays
            # does not count every times, set default 1, need confirm with requirement
            #frequency.append(self.ws.customDays)
            #frequency.append(self.ws.getTimes())
            print(self.ws.getTimes())
            self.signal.emit(frequency)

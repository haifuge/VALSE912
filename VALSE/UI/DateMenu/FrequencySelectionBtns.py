from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class FrequencySelectionBtns(QWidget):
    daysSelection=pyqtSignal(str)
    def __init__(self):
        super().__init__()
        self.initUI()
    def initUI(self):
        self.setMinimumSize(QSize(220,100))
        self.setMaximumSize(QSize(220,100))
        txtX=85
        txtY=15
         # textEdit size
        txtWidth=120
        txtHeight=27
        # row height
        yInterval=30
        lblFrequency=QLabel(self)
        lblFrequency.setText('Frequency:')
        lblFrequency.adjustSize()
        lblFrequency.move(10,txtY)
        self.btnWeekly=QPushButton(self)
        self.btnWeekly.setText('Weekly')
        self.btnWeekly.setCheckable(True)
        self.btnWeekly.move(txtX,txtY)
        self.btnWeekly.resize(txtWidth,txtHeight)
        self.btnWeekly.setChecked(True)

        txtY=txtY+yInterval-4;
        self.btnMonthly=QPushButton(self)
        self.btnMonthly.setText('Monthly')
        self.btnMonthly.setCheckable(True)
        self.btnMonthly.move(txtX,txtY)
        self.btnMonthly.resize(txtWidth,txtHeight)
        
        txtY=txtY+yInterval-4;
        self.btnYearly=QPushButton(self)
        self.btnYearly.setText('Yearly')
        self.btnYearly.setCheckable(True)
        self.btnYearly.move(txtX,txtY)
        self.btnYearly.resize(txtWidth,txtHeight)

        self.btnWeekly.clicked.connect(self.frequencyClicked)
        self.btnMonthly.clicked.connect(self.frequencyClicked)
        self.btnYearly.clicked.connect(self.frequencyClicked)

    def frequencyClicked(self):
        self.freqSender=self.sender();
        if self.freqSender==self.btnWeekly:
            self.btnWeekly.setChecked(True)
            self.btnMonthly.setChecked(False)
            self.btnYearly.setChecked(False)
            self.daysSelection.emit('weekly')
        if self.freqSender==self.btnMonthly:
            self.btnWeekly.setChecked(False)
            self.btnMonthly.setChecked(True)
            self.btnYearly.setChecked(False)
            self.daysSelection.emit('monthly')
        if self.freqSender==self.btnYearly:
            self.btnWeekly.setChecked(False)
            self.btnMonthly.setChecked(False)
            self.btnYearly.setChecked(True)
            self.daysSelection.emit('yearly')
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

# custom panel, buttons of 31-day panel
class MonthlySelectionPanel(QWidget):
    customDays=[0,0,0,0,0,
                0,0,0,0,0,
                0,0,0,0,0,
                0,0,0,0,0,
                0,0,0,0,0,
                0,0,0,0,0,0]
    def __init__(self):
        super().__init__()
        self.initUI()
    def initUI(self):
        self.setMinimumSize(220,180)
        self.setMaximumSize(220,180)
        lblevery=QLabel(self)
        lblevery.setText('Every')
        lblevery.move(10,5)
        lblevery.adjustSize()
        self.txtTimes=QTextEdit(self)
        self.txtTimes.move(45,1)
        self.txtTimes.resize(QSize(35,28))
        self.txtTimes.setText('1')
        lblUnit=QLabel(self)
        lblUnit.setText('month(s) on:')
        lblUnit.move(85,5)
        lblUnit.adjustSize()
        a=25
        for i in range(len(self.customDays)):
            btn=QPushButton(self)
            btn.setText(str(i+1))
            btn.setCheckable(True)
            btn.resize(QSize(a,a))
            btn.move(25+(i%7)*27, 40+27*(i//7))
            btn.clicked.connect(self.btnClicked)
        
    def btnClicked(self):
        s=self.sender()
        if s.isChecked():
            self.customDays[int(s.text())]=int(s.text())
        else:
            self.customDays[int(s.text())]=0
    def getTimes(self):
        return self.txtTimes.toPlainText()

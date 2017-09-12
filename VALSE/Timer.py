import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.speed=1000
        self.setGeometry(300,300,100,100)
        self.btn=QPushButton('start',self)
        self.btn.move(20,20)
        self.timer=QTimer()
        self.timer.setInterval(self.speed)
        self.btn.clicked.connect(self.btnClicked)
        self.timer.timeout.connect(self.click)
        self.n=0
        self.start=False
        self.btnSpeedUp=QPushButton('Speed up', self)
        self.btnSpeedUp.move(20,50)
        self.btnSpeedUp.clicked.connect(self.timerSpeedUp)
        self.btnSlowDown=QPushButton('Slow down',self)
        self.btnSlowDown.move(20,80)
        self.btnSlowDown.clicked.connect(self.timerSlowDown)
    def timerSpeedUp(self):
        self.speed=self.speed/2
        self.timer.setInterval(self.speed)
    def timerSlowDown(self):
        self.speed=self.speed*2
        self.timer.setInterval(self.speed)
    def btnClicked(self):
        if self.start:
            self.start=False
            self.btn.setText('start')
            self.timer.stop()
        else:
            self.start=True
            self.timer.start()
            self.btn.setText('stop')
    def click(self):
        print(self.n)
        self.n=self.n+1

if __name__=='__main__':
    app=QApplication(sys.argv)
    ex=Window()
    ex.show()
    sys.exit(app.exec_())
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class DragButton(QPushButton):
    # button move range
    minX=0
    maxX=0
    # button y_position at
    ypos=0
    # mouse release signal
    mouseReleaseSignal=pyqtSignal()
    mouseMoveSignal=pyqtSignal()
    def setYpos(self, value):
        self.ypos=value

    def setXrange(self, minX, maxX):
        self.minX=minX
        self.maxX=maxX

    # there are two buttons, left button and right button. left button moving range is from 0 to right button x_pox; right button moving range is from right button to left
    # so right button needs to set its left range when left button moves; left button needs to set its right range when right button moves
    def setLeftRange(self, leftX):
        self.minX=leftX

    def setRightRange(self, rightX):
        self.maxX=rightX

    # these two functions are to set the other button, left or right button.
    # self means its self. no self means the other button.
    # this function means self is right button and set the other button left.
    def setLeftBtn(self, lbtn):
        self.leftBtn=lbtn
        self.rightBtn=self

    # this function means self is left, and set the other is right.
    def setRightBtn(self, rbtn):
        self.rightBtn=rbtn
        self.leftBtn=self;

    def mousePressEvent(self, event):
        self.__mousePressPos=None
        self.__mouseMovePos=None
        if event.button()==Qt.LeftButton:
            self.__mousePressPos=event.globalPos()
            self.__mouseMovePos=event.globalPos()

        super(DragButton, self).mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if event.buttons()==Qt.LeftButton:
            currPos=self.mapToGlobal(self.pos())
            globalPos=event.globalPos()
            diff=globalPos-self.__mouseMovePos
            newPos=self.mapFromGlobal(currPos+diff)
            newPos.setY(self.ypos)
            if newPos.x()<self.minX:
                newPos.setX(self.minX)
            if newPos.x()>self.maxX:
                newPos.setX(self.maxX)
            self.move(newPos)
            self.__mouseMovePos=globalPos
            # self is right button
            if self.leftBtn != self:
                self.leftBtn.setRightRange(newPos.x()-self.rightBtn.size().width())
            # self is left button
            if self.rightBtn!=self:
                self.rightBtn.setLeftRange(newPos.x()+self.leftBtn.size().width())

        super(DragButton, self).mouseMoveEvent(event)
        self.mouseMoveSignal.emit()

    def mouseReleaseEvent(self, event):
        if self.__mousePressPos is not None:
            moved=event.globalPos()-self.__mousePressPos
            if moved.manhattanLength()>3:
                event.ignore()
                self.mouseReleaseSignal.emit()
                return

        super(DragButton, self).mouseReleaseEvent(event)
        self.mouseReleaseSignal.emit()

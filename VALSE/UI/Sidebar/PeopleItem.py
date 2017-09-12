import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from UI.Sidebar import MarkerButton
from UI.Sidebar import MarkerSelection
from Common import CommonTools

class PeopleItem(QWidget):
    visible=True;
    selected=False;
    # list [id, changename, value], eg. [light, visible, marker]
    itemChanged=pyqtSignal(list)
    def __init__(self, tId, _name='Person 1', _color=CommonTools.Color.red, _shape=CommonTools.Shape.square):
        super().__init__();
        self.id=tId
        self.markerColor=_color
        self.markerShape=_shape
        self.initUI(_name)

    def initUI(self, _name):
        self.height=25
        self.width=250
        self.setMinimumSize(self.width,self.height)
        self.setMaximumSize(self.width,self.height)
        self.setGeometry(300,300,self.width, self.height)

        self.txtName=QtText(self)
        self.txtName.move(2,1)
        self.txtName.setText(_name)
        self.txtName.setReadOnly(True)
        self.txtName.setFrame(False)
        self.bgColor=self.palette().color(QPalette.Background)
        self.txtName.setStyleSheet('background-color: ' + self.bgColor.name())
        self.txtName.setBackgroundColor(self.bgColor.name())
        #self.txtName.click.connect(self.mouseClick)

        self.btnMarker=MarkerButton.MarkerButton(self, self.markerShape, self.markerColor)
        self.btnMarker.setGeometry(QRect(175,2,20,20))
        self.btnMarker.clicked.connect(self.markerClicked)
        self.btnMarker.setStyleSheet('background-color: ' + self.bgColor.name()+'; border:none;')

        self.btnVisible=QPushButton(self)
        self.btnVisible.setIcon(QIcon(r'Pictures/visible.png'))
        self.btnVisible.clicked.connect(self.visibleClicked)
        self.btnVisible.setGeometry(200,2,20,20)
        self.btnVisible.setStyleSheet('background-color: ' + self.bgColor.name()+'; border:none;')
        self.visible=True

        self.btnLight=QPushButton(self)
        self.btnLight.setIcon(QIcon(r'Pictures/light_normal.png'))
        self.btnLight.clicked.connect(self.lightClicked)
        self.btnLight.setGeometry(225,2,20,20)
        self.btnLight.setStyleSheet('background-color: ' + self.bgColor.name()+'; border:none;')
        self.lighter=False;


    def markerClicked(self):
        ms=MarkerSelection.MarkerSelection()
        ms.setWindowFlags(Qt.FramelessWindowHint)
        point=self.btnMarker.rect().topRight()
        global_point=self.btnMarker.mapToGlobal(point)
        ms.move(global_point.x(),global_point.y())
        ms.signal.connect(self.markerSelected)
        ms.SetMarker(self.markerColor, self.markerShape)
        ms.exec_()

    def markerSelected(self, markerInfo):
        self.markerColor=markerInfo[0]
        self.markerShape=markerInfo[1]
        self.btnMarker.SetMarker(self.markerColor, self.markerShape)

        self.itemChanged.emit([self.id, 'marker',self.markerColor, self.markerShape])

    def SetMarker(self, _color, _shape):
        self.markerColor=_color
        self.markerShape=_shape
        self.btnMarker.SetMarker(self.markerColor, self.markerShape)

    def visibleClicked(self):
        if self.visible:
            self.visible=False
            self.btnVisible.setIcon(QIcon(r'Pictures/invisible.png'))
        else:
            self.visible=True
            self.btnVisible.setIcon(QIcon(r'Pictures/visible.png'))

        self.itemChanged.emit([self.id, 'visible',self.visible])
            
    def lightClicked(self):
        if self.lighter:
            self.lighter=False;
            self.btnLight.setIcon(QIcon(r'Pictures/light_normal.png'))
        else:
            self.lighter=True
            self.btnLight.setIcon(QIcon(r'Pictures/lighter.png'))

        self.itemChanged.emit([self.id, 'light',self.lighter])



class QtText(QLineEdit):
    click=pyqtSignal()
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(23)
        self.setFixedWidth(160)
    def focusOutEvent(self, e):
        self.setReadOnly(True)
        self.setStyleSheet('background-color: ' +self.bgColor)
        self.setSelection(0,0)
    def mouseDoubleClickEvent(self, e):
        if self.isReadOnly():
            self.setReadOnly(False)
            self.setStyleSheet('background-color: white' )
        else:
            self.setReadOnly(True)
            self.setStyleSheet('background-color: ' +self.bgColor)
            self.setSelection(0,0)
    def keyPressEvent (self, e):
        if e.key()==Qt.Key_Return:
            self.setReadOnly(True)
            self.setStyleSheet('background-color: ' +self.bgColor)
            self.setSelection(0,0)
        else:
            super().keyPressEvent(e)

    def setBackgroundColor(self, color):
        self.bgColor=color

    def mousePressEvent(self, QMouseEvent):
        self.click.emit()



if __name__=='__main__':
    app=QApplication(sys.argv)
    ex=PeopleItem()
    ex.show()
    sys.exit(app.exec_())

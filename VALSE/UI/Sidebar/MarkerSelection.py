import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from Common import CommonTools
from Common import CommonMethod

class MarkerSelection(QDialog):
    signal=pyqtSignal(list)
    def __init__(self):
        super().__init__()
        self.initUI()
    def initUI(self):
        self.setMinimumSize(150,150)
        self.setMaximumSize(150,150)
        self.vlayout=QVBoxLayout();
        self.marker=Marker()
        self.vlayout.addWidget(self.marker)
        self.colorSelection=QComboBox()
        self.colorSelection.addItems(CommonTools.colorItems)
        self.colorSelection.resize(100,20)
        self.colorSelection.currentTextChanged.connect(self.colorChanged)
        self.vlayout.addWidget(self.colorSelection)
        self.shapeSelection=QComboBox()
        self.shapeSelection.addItems(CommonTools.shapeItems)
        self.shapeSelection.resize(100,20)
        self.shapeSelection.currentTextChanged.connect(self.shapeChanged)
        self.vlayout.addWidget(self.shapeSelection)
        self.hlayout=QHBoxLayout();
        btnCancel=QPushButton('Cancel',self)
        btnCancel.clicked.connect(self.cancelClicked)
        self.hlayout.addWidget(btnCancel)
        btnOk=QPushButton('OK',self)
        btnOk.clicked.connect(self.okClicked)
        self.hlayout.addWidget(btnOk)
        self.vlayout.addLayout(self.hlayout)
        self.setLayout(self.vlayout)

    def colorChanged(self, e):
        self.marker.SetColor(CommonTools.Color(self.colorSelection.currentIndex()))
    def shapeChanged(self, e):
        self.marker.SetShape(CommonTools.Shape(self.shapeSelection.currentIndex()))
    def cancelClicked(self):
        self.close()
    def okClicked(self):
        self.close()
        markerInfo=[CommonTools.Color(self.colorSelection.currentIndex()), CommonTools.Shape(self.shapeSelection.currentIndex())]
        self.signal.emit(markerInfo)
    def SetMarker(self, color, shape):
        self.color=color
        self.shape=shape
        self.colorSelection.setCurrentIndex(color.value)
        self.shapeSelection.setCurrentIndex(shape.value)

class Marker(QWidget):
    def __init__(self, _color=CommonTools.Color.red, _shape=CommonTools.Shape.square):
        super().__init__()
        #self.setMaximumSize(20,20)
        self.setMinimumSize(20,20)
        self.color=_color
        self.shape=_shape

    def SetSize(self, width, height):
        #self.setMaximumSize(width, height)
        self.setMinimumSize(width, height)

    def SetColor(self, _color):
        self.color=_color
        self.repaint()

    def SetShape(self, _shape):
        self.shape=_shape
        self.repaint()

    def paintEvent(self, e):
        qp=QPainter()
        qp.begin(self)
        CommonMethod.DrawMarker(self.size().width()/2,10,qp,self.shape,self.color,16)
        qp.end()


if __name__=='__main__':
    app=QApplication(sys.argv)
    ex=MarkerSelection()
    ex.setGeometry(300,300,100,100)
    ex.show()
    sys.exit(app.exec_())
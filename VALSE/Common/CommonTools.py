from enum import Enum
from PyQt5.Qt import *
from PyQt5.QtCore import *
from Common import CommonTools

class Color(Enum):
    red = 0
    blue = 1
    yellow = 2
    black = 3
    green = 4
    gray=5
    
colors=[QColor(Qt.red), QColor(Qt.blue), QColor(Qt.yellow), QColor(Qt.black), QColor(Qt.green), QColor(Qt.gray)]
colorss=[Color.red, Color.blue, Color.yellow, Color.black, Color.green, Color.gray]
# color selection items whose content same with colors
colorItems=['Red','Blue','Yellow','Black','Green','Gray']

class Shape(Enum):
    square=0
    circle=1
    triangle=2
    cross=3
    
shapes=[Shape.square, Shape.circle, Shape.triangle, Shape.cross]
# shape select items whose content same with shapes
shapeItems=['Square','Circle','Triangle','Cross']

class MapInfo(object):
    # positions: x, y, timeStamp
    positions=[[0,0,0]]
    shapes=[CommonTools.Shape.cross]
    colors=[CommonTools.Color.red]
    # 0: invisible, 1: visible
    visible=[1]
    # 0: normal, 1: highlight
    highlight=[0]
    # data: positions, shapes, colors, visible, highlight
    data=[positions, shapes, colors, visible, highlight]
    def setShape(self, i, shape):
        self.shapes[i]=shape
    def setColor(self, i, color):
        self.colors[i]=color
    def setVisible(self,i, visible=1):
        self.visible[i]=visible
    def setHighlight(self, i, highlight=1):
        self.highlight[i]=highlight


import itertools

#colors=[Color.red, Color.black, Color.blue, Color.yellow, Color.green, Color.gray]
#shapes=[Shape.square, Shape.circle, Shape.triangle, Shape.cross]
marks=[]
for x in itertools.product(colorss, shapes):
    marks.append(x)
def printMakrs(self):
    for m in self.marks:
        print(m)

#class Marker(object):
#    shape=Shape.shapes(0)
#    color=Color.colors(0)

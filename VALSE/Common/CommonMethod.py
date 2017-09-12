from Common import CommonTools
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import math

def Second2Time(second):
    hour=int(second/3600)
    minute=int((second-hour*3600)/60)
    sec=second%60
    return str(hour)+':'+str(minute)+':'+str(int(sec))


def DrawMarker(x,y, qp, shape, color, a, weight=1):
    _color=CommonTools.colors[color.value]
    if shape==CommonTools.Shape.square:
        drawSquare(qp,x,y,_color, a, weight)
    elif shape==CommonTools.Shape.circle:
        drawCircle(qp,x,y,_color,a, weight)
    elif shape==CommonTools.Shape.triangle:
        drawTriangle(qp,x,y,_color,a, weight)
    elif shape==CommonTools.Shape.cross:
        drawCross(qp,x,y,_color,a, weight)
    
def drawCircle(qp, x, y, color, a, weight):
    r=a
    x=x-r/2
    y=y-r/2
    qp.setPen(QPen(color,weight,Qt.SolidLine))
    qp.drawEllipse(x,y,r,r)

def drawSquare(qp, x,y,color,a, weight):
    length=a
    x=x-length/2
    y=y-length/2
    qp.setPen(QPen(color, weight, Qt.SolidLine))
    qp.drawRect(x,y,length,length)

def drawCross(qp, x, y, color,a, weight):
    length=a
    x=x-length/2
    y=y-length/2
    qp.setPen(QPen(color,weight,Qt.SolidLine))
    qp.drawLine(x,y,x+length,y+length)
    qp.drawLine(x+length,y,x,y+length)

def drawTriangle(qp, x, y, color, a, weight):
    r=a/2+2
    x1,y1=x,y-r
    x2,y2=x-r*math.sqrt(3)/2,y+r/2
    x3,y3=x+r*math.sqrt(3)/2,y+r/2
    qp.setPen(QPen(color,weight,Qt.SolidLine))
    points=QPolygon([QPoint(x1,y1),QPoint(x2,y2),QPoint(x3,y3)])
    qp.drawPolygon(points)

from UI.Object import Marker
from Common import CommonTools
import copy

class Person:
    name=''
    #[x, y, time]
    data=[]
    markers=[]
    id=0
    index=0
    def __init__(self, _id, _name, _color, _shape):
        self.id=_id
        self.name=_name
        self.color=_color
        self.shape=_shape
        self.marker=Marker.Marker(self.color, self.shape)

    def SetMarker(self,_color, _shape): 
        self.color=_color
        self.shape=_shape
        self.marker=Marker.Marker(self.color, self.shape)

    def SetName(self, _name):
        self.name=_name

    def initMarkers(self):
        for i in self.data:
            self.markers.append(copy.deepcopy(self.marker))
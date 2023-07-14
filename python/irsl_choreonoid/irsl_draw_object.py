from cnoid.Util import SgPosTransform
# from cnoid.DrawInterface import GeneralDrawInterface as GDI

from cnoid.IRSLCoords import coordinates

class A(object):
    def __init__(self):
        print('A')
class B(object):
    def __init__(self):
        print('B')
class C(A, B):
    def __init__(self):
        print('C')

#class MOGE(coordinates, GDI):
#    def __init__(self, *args, **kwargs):
#        coordinates.__init__(self)
#        GDI.__init__(self)
## newcoords
## translate
## rotate
## transform
class HOGE(SgPosTransform, coordinates):
    def __init__(self, *args, **kwargs):
        coordinates.__init__(self, *args, **kwargs)
        SgPosTransform.__init__(self)
    def newcoords(self, cds):
        super().newcoords(cds)

class coordsWrapper(coordinates):
    def __init__(self, child):
        self.__child = child

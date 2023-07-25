import cnoid.DrawInterface as di
import numpy as np

from .irsl_draw_object import *
from .robot_util import make_coordinates

###
class DrawCoords(object):
##    """deprecated, use DrawCoordsList"""
    def __init__(self, color=None, width=None):
        self.width = width
        if color is None:
            self.XLine = di.DrawInterface(np.array([1, 0, 0]))
            self.YLine = di.DrawInterface(np.array([0, 1, 0]))
            self.ZLine = di.DrawInterface(np.array([0, 0, 1]))
        elif type(color) is np.ndarray:
            self.XLine = di.DrawInterface(color)
            self.YLine = di.DrawInterface(color)
            self.ZLine = di.DrawInterface(color)
        elif (type(color) is list) and ( (type(color[0]) is int) or (type(color[0]) is float) ):
            self.XLine = di.DrawInterface(np.array(color))
            self.YLine = di.DrawInterface(np.array(color))
            self.ZLine = di.DrawInterface(np.array(color))
        elif (type(color) is list) and (type(color[0]) is np.ndarray):
            self.XLine = di.DrawInterface(color[0])
            self.YLine = di.DrawInterface(color[1])
            self.ZLine = di.DrawInterface(color[2])
        elif (type(color) is list) and (type(color[0]) is list):
            self.XLine = di.DrawInterface(np.array(color[0]))
            self.YLine = di.DrawInterface(np.array(color[1]))
            self.ZLine = di.DrawInterface(np.array(color[2]))
        else:
            self.XLine = di.DrawInterface(np.array([1, 0, 0]))
            self.YLine = di.DrawInterface(np.array([0, 1, 0]))
            self.ZLine = di.DrawInterface(np.array([0, 0, 1]))

    def __del__(self):
        # print('del: {:X}'.format(id(self)))
        self.hide()
        self.XLine = None
        self.YLine = None
        self.ZLine = None
    def __repr__(self):
        return '<DrawCoords {:X}({:X},{:X},{:X})>'.format(id(self), id(self.XLine), id(self.YLine), id(self.ZLine))

    def hide(self, flush = True):
        self.XLine.hide(False)
        self.YLine.hide(False)
        self.ZLine.hide(False)
        if flush:
            di.flush()
    def show(self, flush = True):
        self.XLine.show(False)
        self.YLine.show(False)
        self.ZLine.show(False)
        if flush:
            di.flush()
    def hide_and_show(self, flush = True):
        self.XLine.hide_and_show()
        self.YLine.hide_and_show()
        self.ZLine.hide_and_show()
        if flush:
            di.flush()
    def draw_simple(self, coords, length=0.1, flush=True):
        # self.hide(flush=flush)
        if not self.width is None:
            self.XLine.setLineWidth(self.width)
            self.YLine.setLineWidth(self.width)
            self.ZLine.setLineWidth(self.width)
        self.XLine.drawAxis(coords, 0, length)
        self.YLine.drawAxis(coords, 1, length)
        self.ZLine.drawAxis(coords, 2, length)
        self.show(flush=flush)
    def draw(self, coords, length = 0.1, axis_size = 0.02, flush=True):
        self.hide(flush=flush)
        rot = iu.Position_rotation(coords)
        ax_x = length * rot[:3, 0]
        ax_y = length * rot[:3, 1]
        ax_z = length * rot[:3, 2]
        ax_vec = length * iu.normalizeVector(rot.dot(np.array([1, 1, 1])))
        pp = iu.Position_translation(coords)
        if not self.width is None:
            self.XLine.setLineWidth(self.width)
            self.YLine.setLineWidth(self.width)
            self.ZLine.setLineWidth(self.width)
        self.XLine.drawArrow(pp, pp + ax_x, axis_size, ax_vec, 15)
        self.YLine.drawArrow(pp, pp + ax_y, axis_size, ax_vec, 15)
        self.ZLine.drawArrow(pp, pp + ax_z, axis_size, ax_vec, 15)
        self.show(flush=flush)

# class DrawCoordsList(object):
#     def __init__(self):
#         self.coords_list = []
#         self.count = 0
#     def flush(self):
#         di.flush()
#     def hide(self, start=0, length=0):
#         if length == 0:
#             end = None
#         else:
#             end = start + length
#         for l in self.coords_list[start:end]:
#             l.hide(flush=False)
#         di.flush()
#     def show(self, start=0, length=0):
#         if length == 0:
#             end = None
#         else:
#             end = start + length
#         for l in self.coords_list[start:end]:
#             l.show(flush=False)
#         di.flush()
#     def clear(self):
#         for l in self.coords_list:
#             l.hide(flush=False)
#         di.flush()
#         self.coords_list = []
#         self.count = 0
#     def generatePointFunction(self, length=0.1, maxlength=0, flush=True):
#         def closure_func__(lst, **kwargs):
#             pos = np.array(lst[0][1:])
#             cd = DrawCoords()
#             cds_ = iu.coordinates(pos)
#             cd.draw_simple(cds_, length=length, flush=flush)
#             self.coords_list.append(cd)
#             self.count += 1
#         return closure_func__
#     def generateCoordsFunction(self, length=0.1, maxlength=0, flush=True):
#         def closure_func__(lst, **kwargs):
#             lst = lst[0]
#             pos = np.array(lst[1:4])
#             rpy = np.array(lst[4:7])
#             cd = DrawCoords()
#             cds_ = iu.coordinates(pos)
#             cds_.setRPY(rpy)
#             cd.draw_simple(cds_, length=length, flush=flush)
#             self.coords_list.append(cd)
#             self.count += 1
#        return closure_func__

class DrawCoordsList(object):
    """DrawCoordsList(object):
    """
    def __init__(self, x_color=np.array([1,0,0]), y_color=np.array([0,1,0]), z_color=np.array([0,0,1]), length=0.1, width=None):
        """DrawCoordsList(initializer)

        Args:
            x_color (numpy.array, default = [1, 0, 0] ) : color of x-axis
            y_color (numpy.array, default = [0, 1, 0] ) : color of y-axis
            z_color (numpy.array, default = [0, 0, 1] ) : color of z-axis
            length  (float, default = 0.1) : length of axis
            width   (float, optional) : width of axis

        """
        self.__x_color = x_color
        self.__y_color = y_color
        self.__z_color = z_color
        self.__length = length
        if width is None:
            self.__width = 1
        else:
            self.__width = width
        self.reset()

    def __del__(self):
        self.hide()
        self.__interface = None
    @property
    def T(self):
        return self.__interface.T
    @T.setter
    def T(self, _in):
        self.__interface.T = _in
    @property
    def interface(self):
        return self.__interface
    def setOrigin(self, coords):
        """setOrigin(self, coords):

        Args:

        Returns:

        """
        self.__interface.setOrigin(coords)

    def getOrigin(self):
        """getOrigin(self):

        Args:

        Returns:

        """
        return self.__interface.getOrigin()

    def setLineWidth(self, _width):
        """setLineWidth(self, _width):

        Args:

        Returns:

        """
        self.__interface.setLineWidth(_width)
        self.__width = _width

    def reset(self):
        """reset(self):

        Args:

        Returns:

        """
        self.__interface = di.DrawInterface(self.__x_color)
        self.__x_color_index = 0
        self.__y_color_index = self.__interface.addColor(self.__y_color)
        self.__z_color_index = self.__interface.addColor(self.__z_color)
        self.__interface.setLineWidth(self.__width)
        self.__count = 0

    def flush(self):
        """flush(self):

        Args:

        Returns:

        """
        self.__interface.flush()
        self.__interface.render()

    def hide(self, start=0, length=0):
        """hide(self, start=0, length=0):

        Args:

        Returns:

        """
        self.__interface.hide(True)
        self.flush()

    def show(self, start=0, length=0):
        """show(self, start=0, length=0):

        Args:

        Returns:

        """
        self.__interface.show(True)
        self.flush()

    def clear(self):
        """clear(self):

        Args:

        Returns:

        """
        self.__interface.hide(True)
        self.flush()
        self.reset()

    def addCoords(self, coords, flush=False):
        """addCoords(self, coords, flush=False):

        Args:

        Returns:

        """
        if flush:
            self.__interface.hide(False)
        self.__interface.addAxis3(coords, self.__length, self.__x_color_index, self.__y_color_index, self.__z_color_index)
        if flush:
            self.__interface.show(True)
            self.flush()
        self.__count += 1

    def addCross(self, coords, flush=False):
        """addCross(self, coords, flush=False):

        Args:

        Returns:

        """
        if flush:
            self.__interface.hide(False)
        self.__interface.addBDAxis3(coords, self.__length, self.__x_color_index, self.__y_color_index, self.__z_color_index)
        if flush:
            self.__interface.show(True)
            self.flush()
        self.__count += 1

    def generatePointFunction(self, length=0.1, maxlength=0, index=0, flush=True):
        """generatePointFunction(self, length=0.1, maxlength=0, index=0, flush=True):

        Args:

        Returns:

        """
        def closure_func__(lst, **kwargs):
            pos = np.array(lst[index][1:])
            cds_ = iu.coordinates(pos)
            self.addCross(cds_,flush=flush)
        return closure_func__

    def generateCoordsFunction(self, length=0.1, maxlength=0, index=0, flush=True):
        """generateCoordsFunction(self, length=0.1, maxlength=0, index=0, flush=True):

        Args:

        Returns:

        """
        def closure_func__(lst, **kwargs):
            lst = lst[index]
            pos = np.array(lst[1:4])
            rpy = np.array(lst[4:7])
            cds_ = iu.coordinates(pos)
            cds_.setRPY(rpy)
            self.addCoords(cds_,flush=flush)
        return closure_func__

class DrawCoordsListWrapped(DrawCoordsList, coordsWrapper):
    """DrawCoordsListWrapped(DrawCoordsList, coordsWrapper):
    """
    def __init__(self, **kwargs):
        """__init__(self, **kwargs):

        Args:

        """
        DrawCoordsList.__init__(self, **kwargs)
        cds = None
        if len(kwargs) > 0:
            try:
                cds = make_coordinates(kwargs)
            except Exception as e:
                pass
        coordsWrapper.__init__(self, self, cds, update_callback=lambda : self.flush())

class GeneralDrawInterfaceWrapped(di.GeneralDrawInterface, coordsWrapper):
    """GeneralDrawInterfaceWrapped(di.GeneralDrawInterface, coordsWrapper):
    """
    def __init__(self, **kwargs):
        """__init__(self, **kwargs):

        Args:

        """
        di.GeneralDrawInterface.__init__(self)
        cds = None
        if len(kwargs) > 0:
            try:
                cds = make_coordinates(kwargs)
            except Exception as e:
                pass
        coordsWrapper.__init__(self, self, cds, update_callback=lambda : self.flush())

    def flush(self):
        """flush(self):

        Args:

        Returns:

        """
        super().flush()
        super().render()

    def addObject(self, obj, update=False):
        self.addPyObject(obj, update=update)
    def removeObject(self, obj, update=False):
        self.removePyObject(obj, update=update)

    def addPyObject(self, obj, update=False):
        """addPyObject(self, obj, update=False):

        Args:

        Returns:

        """
        if type(obj) is coordsWrapper:
            super().addPyObject(obj.target, update)
            obj.setUpdateCallback( lambda : self.flush() )
        else:
            super().addPyObject(obj, update)

    def removePyObject(self, obj, update=False):
        """removePyObject(self, obj, update=False):

        Args:

        Returns:

        """
        if type(obj) is coordsWrapper:
            super().removePyObject(obj.target, update)
        else:
            super().removePyObject(obj, update)

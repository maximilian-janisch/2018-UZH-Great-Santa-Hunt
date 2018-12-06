"""
GUI
Authors: Atsuhiro Funatsu, Maximilian Janisch
"""

import PyQt5.Qt
import PyQt5.QtGui
import PyQt5.QtWidgets

from logs import *


class Santa_GUI(PyQt5.QtWidgets.QMainWindow):
    
    def __init__(self, world):
        """Initialises the class 'Santa_GUI'."""
        
        super().__init__()

        self.setWindowTitle('Visualisation (Santa)')
        self.resize(800, 800)
        self.show()

        self.world = world

    def paintEvent(self, QPaintEvent):
        # note: the name of this function is important since it overwrites
        #       paintEvent in QWidget on thus gets called on repaint
        """Draws the map."""
        
        world = self.world

        pen = PyQt5.QtGui.QPen()
        qp = PyQt5.QtGui.QPainter()
        qp.begin(self)

        # region plot Santa's house
        # body
        qp.setBrush(PyQt5.Qt.QColor(255,0,0))
        qp.drawRect(world.scale * (world.santa_house.center[0] - world.N / 40),
                    world.scale * (world.santa_house.center[1] - world.N / 40),
                    world.scale * world.N / 20,
                    world.scale * world.N / 20)
        # roof
        qp.setBrush(PyQt5.Qt.QColor(0,0,0))
        qp.drawLine(world.scale * (world.santa_house.center[0] - world.N / 40),
                    world.scale * (world.santa_house.center[1] - world.N / 40),
                    world.scale * (world.santa_house.center[0] + world.N / 40),
                    world.scale * (world.santa_house.center[1] + world.N / 40))
        qp.drawLine(world.scale * (world.santa_house.center[0] + world.N / 40),
                    world.scale * (world.santa_house.center[1] - world.N / 40),
                    world.scale * (world.santa_house.center[0] - world.N / 40),
                    world.scale * (world.santa_house.center[1] + world.N / 40))
        # endregion

        # region plot deers            
        for deer in world.deers:
            if deer.loaded == 0:
                qp.setBrush(PyQt5.Qt.QColor(0,0,0))
            else:
                qp.setBrush(PyQt5.Qt.QColor(178,34,34)) # Alternatively, we could also draw deers by the colour of resource
            qp.drawEllipse(world.scale * deer.position[0] - 5,
                           world.scale * deer.position[1] - 5,
                           10,
                           10)
        # endregion

        # region plot kids' houses
        for house in world.kids_houses:  # todo: change house colour once toy is delivered
            qp.setBrush(PyQt5.Qt.QColor(0,0,0))
            qp.drawRect(world.scale * (house.center[0] - house.size / 2),
                        world.scale * (house.center[1] - house.size / 2),
                        world.scale * house.size,
                        world.scale * house.size)
        # endregion

        # region plot resource locations
        for location in world.locations:
            qp.setBrush(PyQt5.Qt.QColor(
                world.colours[location.resource.name][0],
                world.colours[location.resource.name][1],
                world.colours[location.resource.name][2]))
            qp.drawEllipse(
                world.scale * (location.center[0] - location.radius),
                world.scale * (location.center[1] - location.radius),
                world.scale * location.radius * 2,
                world.scale * location.radius * 2)
        # endregion

        # region plot markers
        pen.setWidth(5)
        for marker in world.markers:
            pen.setColor(PyQt5.QtGui.QColor(
                world.colours[marker.location.resource.name][0],
                world.colours[marker.location.resource.name][1],
                world.colours[marker.location.resource.name][2],
                51))
            qp.setPen(pen)
            qp.drawLine(world.scale * marker.endpoint[0],
                        world.scale * marker.endpoint[1],
                        world.scale * marker.startpoint[0],
                        world.scale * marker.startpoint[1])
        # endregion

        qp.end()

    def update_world(self, world):
        """
        Updates the map.
        
        Args:
            world: An instance of the class 'World', describing the world.
        """
        
        self.world = world
        mainlog.debug("Update world called")
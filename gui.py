"""
GUI
Authors: Atsuhiro Funatsu, Maximilian Janisch
"""

import PyQt5.QtWidgets as Wid
import PyQt5.Qt as Qt
import PyQt5.QtGui

from logs import *


class Santa_GUI(Wid.QMainWindow):
    def __init__(self, world):
        """
        Initialises the class 'Santa_GUI'.
        """
        super().__init__()

        self.setWindowTitle('Visualisation (Santa)')
        self.resize(800, 800)
        self.show()

        self.world = world

        #self.p = Qt.QPainter()
        #self.p.begin(self)

    # def plot_santa_house(self):
    #     """
    #     Plots Santa's house into the map.
    #     """
    #     world = self.world
    #     # body
    #     self.p.setBrush(Qt.QColor(255, 0, 0))
    #     self.p.drawRect(world.scale * (world.santa_house.center[0] - world.N / 40),
    #                     world.scale * (world.santa_house.center[1] - world.N / 40),
    #                     world.scale * world.N / 20,
    #                     world.scale * world.N / 20)
    #     # roof
    #     self.p.setBrush(Qt.QColor(0, 0, 0))
    #     self.p.drawLine(world.scale * (world.santa_house.center[0] - world.N / 40),
    #                     world.scale * (world.santa_house.center[1] - world.N / 40),
    #                     world.scale * (world.santa_house.center[0] + world.N / 40),
    #                     world.scale * (world.santa_house.center[1] + world.N / 40))
    #     self.p.drawLine(world.scale * (world.santa_house.center[0] + world.N / 40),
    #                     world.scale * (world.santa_house.center[1] - world.N / 40),
    #                     world.scale * (world.santa_house.center[0] - world.N / 40),
    #                     world.scale * (world.santa_house.center[1] + world.N / 40))
    #
    # def plot_resources(self, world):
    #     """
    #     Plots resource locations into the map.
    #
    #     Args:
    #         world: An instance of the class 'World', describing the world.
    #     """
    #
    #     for location in world.locations:
    #         self.p.setBrush(Qt.QColor(1
    #             # world.colours[location.resource.name][0],
    #             # world.colours[location.resource.name][1],
    #             # world.colours[location.resource.name][2]
    #                                  )
    #         )
    #         self.p.drawEllipse(
    #             world.scale * (location.center[0] - location.radius),
    #             world.scale * (location.center[1] - location.radius),
    #             world.scale * location.radius * 2,
    #             world.scale * location.radius * 2)
    #
    # def plot_kids_houses(self, world):
    #     """
    #     Plots kids' houses into the map.
    #
    #     Args:
    #         world: An instance of the class 'World', describing the world.
    #     """
    #
    #     for house in world.kids_houses:  # todo: change house colour once toy is delivered
    #         self.p.setBrush(Qt.QColor(0, 0, 0))
    #         self.p.drawRect(world.scale * (house.center[0] - house.size / 2),
    #                         world.scale * (house.center[1] - house.size / 2),
    #                         world.scale * house.size,
    #                         world.scale * house.size)

    def paintEvent(self, QPaintEvent):  # currently replaces plot_deers
        # note: the name of this function is important since it overwrites paintEvent in QWidget on thus gets called
        # on repaint
        # I think it is best if you just put all the plotting in here
        """
        Plots deers and houses into the map.
        """
        world = self.world

        qp = PyQt5.QtGui.QPainter()
        qp.begin(self)

        # region plot Santa's house
        # body
        qp.setBrush(Qt.QColor(255, 0, 0))
        qp.drawRect(world.scale * (world.santa_house.center[0] - world.N / 40),
                        world.scale * (world.santa_house.center[1] - world.N / 40),
                        world.scale * world.N / 20,
                        world.scale * world.N / 20)
        # roof
        qp.setBrush(Qt.QColor(0, 0, 0))
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
            if deer.loaded:
                # change color
                pass
            qp.setBrush(Qt.QColor(178, 34, 34))
            qp.drawEllipse(world.scale * deer.position[0] - 5,
                           world.scale * deer.position[1] - 5,
                           10, 10)
        # endregion

        # region plot houses
        for house in world.kids_houses:  # todo: change house colour once toy is delivered
            qp.setBrush(Qt.QColor(0, 0, 0))
            qp.drawRect(world.scale * (house.center[0] - house.size / 2),
                        world.scale * (house.center[1] - house.size / 2),
                        world.scale * house.size,
                        world.scale * house.size
                        )
        # endregion

        # region plot locations
        for location in world.locations:
            qp.setBrush(Qt.QColor(1,1,1
                        # world.colours[location.resource.name][0],
                        # world.colours[location.resource.name][1],
                        # world.colours[location.resource.name][2]
                                             )
                    )
            qp.drawEllipse(
                world.scale * (location.center[0] - location.radius),
                world.scale * (location.center[1] - location.radius),
                world.scale * location.radius * 2,
                world.scale * location.radius * 2
            )
        # endregion

        # region plot markers
        qp.setOpacity(0.2)
        for marker in world.markers:
            qp.setBrush(Qt.QColor(1,1,1
                # world.colours[marker.location.resource.name][0],
                # world.colours[marker.location.resource.name][1],
                # world.colours[marker.location.resource.name][2]
                ))
            qp.drawLine(world.scale * marker.endpoint[0],
                            world.scale * marker.endpoint[1],
                            world.scale * marker.startpoint[0],
                            world.scale * marker.startpoint[1])
        qp.setOpacity(1.0)

        qp.end()

    # def plot_markers(self):
    #     """
    #     Plots markers into the map.
    #     """
    #     world = self.world
    #     self.p.setOpacity(0.2)
    #     for marker in world.markers:
    #         self.p.setBrush(Qt.QColor(1
    #             # world.colours[marker.location.resource.name][0],
    #             # world.colours[marker.location.resource.name][1],
    #             # world.colours[marker.location.resource.name][2]
    #             ))
    #         self.p.drawLine(world.scale * marker.endpoint[0],
    #                         world.scale * marker.endpoint[1],
    #                         world.scale * marker.startpoint[0],
    #                         world.scale * marker.startpoint[1])
    #     self.p.setOpacity(1.0)

    # def plot_invariable_objects(self):
    #     """
    #     Plots invariable objects into the map.
    #
    #     Plots Santa's house.
    #     """
    #
    #     self.plot_santa_house()
    #
    # def plot_variable_objects(self):
    #     """Plots variable objects into the map.
    #
    #     Plots resources, kids' houses, deers and markers.
    #     """
    #     world = self.world
    #     self.plot_resources(world)
    #     self.plot_kids_houses(world)
    #     self.plot_deers(world)
    #     self.plot_markers(world)
    #
    # def clear_world(self):
    #     """
    #     Clears the map.
    #     """
    #     self.p.eraseRect(0, 0, 800, 800)

    def update_world(self, world):
        """
        Updates map.
        
        Args:
            world: An instance of the class 'World', describing the world.
        """
        self.world = world
        mainlog.debug("Update world called")

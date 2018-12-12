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
        
        # region plot Santa's house
        # body
        qp.setBrush(PyQt5.Qt.QColor(255, 0, 0))
        qp.drawRect(world.scale * (world.santa_house.center[0] - world.N / 40),
                    world.scale * (world.santa_house.center[1] - world.N / 40),
                    world.scale * world.N / 20,
                    world.scale * world.N / 20)
        # roof
        qp.setBrush(PyQt5.Qt.QColor(0, 0, 0))
        qp.drawLine(world.scale * (world.santa_house.center[0] - world.N / 40),
                    world.scale * (world.santa_house.center[1] - world.N / 40),
                    world.scale * (world.santa_house.center[0] + world.N / 40),
                    world.scale * (world.santa_house.center[1] + world.N / 40))
        qp.drawLine(world.scale * (world.santa_house.center[0] + world.N / 40),
                    world.scale * (world.santa_house.center[1] - world.N / 40),
                    world.scale * (world.santa_house.center[0] - world.N / 40),
                    world.scale * (world.santa_house.center[1] + world.N / 40))
        # endregion

        # region plot kids' houses
        for kid in world.kids:
            if kid.received:
                # If kid already has the toy, the house is orange.
                qp.setBrush(PyQt5.Qt.QColor(255, 165, 0))
            else:
                # If not, it's black.
                qp.setBrush(PyQt5.Qt.QColor(0, 0, 0))
            
            qp.drawRect(
                world.scale * (kid.house.center[0] - kid.house.size / 2),
                world.scale * (kid.house.center[1] - kid.house.size / 2),
                world.scale * kid.house.size,
                world.scale * kid.house.size)
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
            
        # reset pen
        pen.setColor(PyQt5.QtGui.QColor(0, 0, 0, 255))
        pen.setWidth(0)
        qp.setPen(pen)
        # endregion

        # region plot deers            
        for deer in world.deers:
            if deer.loaded:
                # If deer has loaded resource, its colour is orange.
                # Alternatively, we could also draw deers by the colour of resource
                qp.setBrush(PyQt5.Qt.QColor(255, 165, 0))
            else:
                # If not, it's black.
                qp.setBrush(PyQt5.Qt.QColor(0, 0, 0))

            qp.drawEllipse(world.scale * deer.position[0] - 5,
                           world.scale * deer.position[1] - 5,
                           10,
                           10)
            
            if deer.is_distributing:
                # Draws a number indicating the amount of loaded toys.
                qp.drawText(world.scale * deer.position[0] + 4,
                            world.scale * deer.position[1] - 4,
                            str(deer.loaded_toys()))
        # endregion

        # region draw clock
        qp.setBrush(PyQt5.Qt.QColor(255, 255, 255, 127))
        qp.drawRect(8, 8, 250, 40)
        qp.drawText(
            12, 34,
            f'Provided Time: {world.T} | Current Time: {world.gui_time:.2f}')
        # endregion

        qp.end()

    def update_world(self, world):
        """Updates the map.
        
        Args:
            world: An instance of the class 'World', describing the world.
        """
        self.world = world
        
    def generate_message(self, world):
        """Generates a message for the pop-up message box.
        
        See also the docstring of show_popup().
        
        Args:
            world: An instance of the class 'World', describing the world.
            
        Returns:
            A message of type str describing the produced toys and their
            destinations.
        """
        message = f'Santa made {len(world.toys)} toys for {len(world.kids)} ' \
                  f'kids:\n\n'
        toys = False
        for kid in world.kids:
            if kid.toy is not None: # if kid will get a toy
                toys = True
                message += (kid.name + ' will get a ' +
                            kid.toy.toy_type.toy_name + '.\n')
                
        return message if toys else "Sadly there will be no toys this christmas"
        
    def show_popup(self, world):
        """Shows a pop-up message box.
        
        This method gets called once the deers have finished collecting
        resources and the toys have been produced. It creates a pop-up message
        box and the main GUI will stop until the user clicks 'OK' in the
        pop-up.
        See also the docstring of generate_message().
        
        Args:
            world: An instance of the class 'World', describing the world.
        """
        PyQt5.QtWidgets.QMessageBox.about(self, 'Toys',
                                          self.generate_message(world))

    def game_finished(self, iter_):
        PyQt5.QtWidgets.QMessageBox.about(self, "Game over", f"Game finished after {iter_:.2f} seconds")

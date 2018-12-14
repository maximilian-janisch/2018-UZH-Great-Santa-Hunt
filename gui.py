"""
GUI
Authors: Atsuhiro Funatsu, Maximilian Janisch
"""

import random

import PyQt5.Qt
import PyQt5.QtGui
import PyQt5.QtWidgets
from PyQt5 import QtCore


class Santa_GUI(PyQt5.QtWidgets.QMainWindow):

    def __init__(self, world):
        """Initialises the class 'Santa_GUI'."""

        super().__init__()

        self.setWindowTitle('Visualisation (Santa)')
        self.resize(800, 880)

        self.world = world

        self.draw_path = False  # draw time-dependent distribution paths or not
        self.is_visualising_distribution = False  # used for drawing / not drawing distribution paths
        self.btn = PyQt5.QtWidgets.QPushButton('Show/hide live distribution paths',
                                               self)
        self.btn.clicked.connect(self.switch_live_mode)
        self.btn.resize(self.btn.minimumSizeHint())
        self.btn.move(0, 800)

        self.btn2 = PyQt5.QtWidgets.QPushButton('Show/hide static distribution paths',
                                               self)
        self.btn2.clicked.connect(self.switch_a_priori_mode)
        self.btn2.resize(self.btn.minimumSizeHint())
        self.btn2.move(200, 800)

        self.show()

    def paintEvent(self, QPaintEvent):
        # note: the name of this function is important since it overwrites
        #       paintEvent in QWidget on thus gets called on repaint
        """Draws the map."""

        world = self.world

        pen = PyQt5.QtGui.QPen()
        qp = PyQt5.QtGui.QPainter()
        qp.begin(self)

        # region plot world boundary
        qp.drawRect(0, 0, 800, 800)
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
            try:
                pen.setColor(PyQt5.QtGui.QColor(
                    world.colours[marker.location.resource.name][0],
                    world.colours[marker.location.resource.name][1],
                    world.colours[marker.location.resource.name][2],
                    51))
            except:
                pen.setColor(PyQt5.QtGui.QColor(0, 0, 0))
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

        # region draw a priori distribution paths
        if self.is_visualising_distribution:
            pen.setWidth(2)
            pen.setStyle(QtCore.Qt.CustomDashLine)
            pen.setDashPattern([1, 4, 5, 4])
            for path in self.world.distribution_paths:
                try:
                    pen.setColor(path.color)
                except AttributeError:
                    path.color = PyQt5.Qt.QColor(*random.choice(list(world.colours.values())))
                    pen.setColor(path.color)
                qp.setPen(pen)

                kids = path.kids
                if kids:
                    qp.drawLine(world.scale * world.santa_house.center[0],
                                world.scale * world.santa_house.center[1],
                                world.scale * kids[0].house.center[0],
                                world.scale * kids[0].house.center[1],
                                )
                for i in range(len(kids) - 1):

                    qp.drawLine(world.scale * kids[i].house.center[0],
                                world.scale * kids[i].house.center[1],
                                world.scale * kids[i + 1].house.center[0],
                                world.scale * kids[i + 1].house.center[1])
                else:
                    try:
                        qp.drawLine(world.scale * kids[-1].house.center[0],
                                    world.scale * kids[-1].house.center[1],
                                    world.scale * world.santa_house.center[0],
                                    world.scale * world.santa_house.center[1]
                                    )
                    except IndexError:
                        pass

            # reset pen
            pen.setColor(PyQt5.QtGui.QColor(0, 0, 0, 255))
            pen.setStyle(QtCore.Qt.SolidLine)
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

                if self.draw_path:
                    # Draws time-dependent distribution paths.
                    pen.setColor(PyQt5.QtGui.QColor(0, 0, 0, 51))
                    pen.setWidth(5)
                    qp.setPen(pen)

                    for i in range(len(deer.distr_log) - 1):
                        qp.drawLine(world.scale * deer.distr_log[i][0],
                                    world.scale * deer.distr_log[i][1],
                                    world.scale * deer.distr_log[i + 1][0],
                                    world.scale * deer.distr_log[i + 1][1])

                    # reset pen
                    pen.setColor(PyQt5.QtGui.QColor(0, 0, 0, 255))
                    pen.setWidth(0)
                    qp.setPen(pen)
        # endregion

        # region draw clock
        qp.setBrush(PyQt5.Qt.QColor(255, 255, 255, 127))
        qp.drawRect(8, 8, 320, 40)
        qp.drawText(
            12, 34,
            f'Provided Time: {world.T} | Current Time: {world.gui_time:.2f}')
        # endregion
        
        # region draw latest event
        for kid in world.kids:
            if kid.received and kid.index not in world.happy_kids_list:
                world.happy_kids_list.append(kid.index)
                world.latest_event = f'Latest event: {kid.name} received ' \
                                     f'{kid.toy.toy_type.toy_name} ' \
                                     f'(time: {world.gui_time:.2f})'
        qp.drawText(5, 865, world.latest_event)
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
        if len(world.toys) == 1 and len(world.kids) == 1:
            message = f'Santa made 1 gift for 1 kid'
        elif len(world.toys) == 1 and len(world.kids) != 1:
            message = f'Santa made 1 gift for {len(world.kids)} kids'
        elif len(world.toys) != 1 and len(world.kids) == 1:
            message = f'Santa made {len(world.toys)} gifts for 1 kid'
        else:
            message = f'Santa made {len(world.toys)} gifts for ' \
                f'{len(world.kids)} kids'

        if len(world.toys) - len(world.kids) == 1:
            message += f" (he will keep 1 gift for himself)"
        elif len(world.toys) > len(world.kids):
            message += f" (he will keep {len(world.toys) - len(world.kids)} " \
                f"gifts for himself)"

        message += ".\n\n"

        toys = False
        for kid in world.kids:
            if kid.toy is not None:  # if kid will get a toy
                toys = True
                message += (kid.name + ' will get ' +
                            kid.toy.toy_type.toy_name + '.\n')

        if len(world.toys) < len(world.kids):
            message += 'The rest doesn\'t deserve gifts.\n'

        return message if toys else "Sadly, there will be no gifts this Christmas."

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
        msg = self.generate_message(world)
        PyQt5.QtWidgets.QMessageBox.about(self, 'Gifts',
                                          msg if len(msg) < 1000 else "\n".join(msg.splitlines()[:30]) + "\n...")
        # keep message on screen

    def game_finished(self, iter_):
        PyQt5.QtWidgets.QMessageBox.about(
            self, "Game over", f"Game finished after {iter_:.2f} seconds")

    def switch_live_mode(self):
        """Reverses the value of draw_path.

        This method gets called when the user clickes the button in the GUI to
        show / hide the time-dependent distribution paths. It reverses the
        Boolean value of draw_path which is used for deciding whether the live paths
        will be drawn or not.
        """
        self.draw_path = not self.draw_path

    def switch_a_priori_mode(self):
        """
        Reverses the value of draw_path.

        This method gets called when the user clickes the button in the GUI to
        show / hide the a priori distribution paths. It reverses the
        Boolean value of draw_path which is used for deciding whether the a priori paths
        will be drawn or not.
        """
        self.is_visualising_distribution = not self.is_visualising_distribution

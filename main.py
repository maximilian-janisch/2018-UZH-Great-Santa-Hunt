"""
Main file of the Santa Hunt project
Authors: Maximilian Janisch, Robert Scherrer
"""

import sys
import PyQt5.QtWidgets
from PyQt5.QtCore import QTimer
from typing import *  # library for type hints

from logs import *
from global_variables import *
from gui import Santa_GUI
from statistics import Statistics


world = World("config.ini")  # reads Config and generates Resources, Locations, Deers

iter_ = 0


# region Main Function
def main():  # one step of the main loop
    global iter_
    if iter_ == 0:
        for deer in world.deers:  # All deers leave Santa's house
            deer.move_to_collect(world.dx, world.santa_house, world.N, world.markers)
    elif iter_ <= world.T:
        for deer in world.deers:
            deer.move_to_collect(world.dx, world.santa_house, world.N, world.markers)
            for location in world.locations:  # checks if the deer hit a natural resource
                if location.point_in_circle(deer.position) and not deer.resource:  # a searching deer hits a resource
                    deer.load_resource(location, world.Lp)  # deer loads resource

                    if location.amount == 0:  # checks if resource location is depleted
                        world.locations.remove(location)
                    else:
                        already_marked = False
                        for marker in world.markers:
                            already_marked = already_marked or (marker.location == location)
                        if not already_marked:
                            world.markers.append(deer.start_marker(location, world.santa_house.center))  # add marker
                    break  # one deer can not collect multiple Resources at once
    elif iter_ > world.T:
        # start distribution
        world.produce_toys()
        world.calculate_distribution()
        for second in range(1, world.T + 1):  # main loop
            for deer in world.deers:
                deer.move_to_distribute(world.dx, world.santa_house, world.distribution_paths)

            mainlog.debug(f"Time: {second} / Deers: {world.deers} / Paths: {world.distribution_paths}")

            # finish early if the job is done
            if all(path.is_finished() for path in world.distribution_paths):
                # yeah, all paths were followed successfully
                if all(deer.inactive for deer in world.deers):
                    # the deers are resting
                    mainlog.debug(
                        f"Distribution finished by {len(world.deers)} deers on {len(world.distribution_paths)} paths.")
                    break
        # todo: now walk

    iter_ += 1
    #  if distribution_is_done:
    #       gui_updates.stop()

    for marker in world.markers:  # marker cleanup todo: unify marker cleanup a posteriori and in real time
        if marker.is_disabled():
            world.markers.remove(marker)

# endregion


# region GUI
def animation_next():  # todo: export to some other file ?
    """
    Updates the program logic and GUI
    """
    mainlog.debug("Called animation_next")
    main()  # next step of loop
    gui.update_world(world)  # update
    gui.repaint()            # GUI

    stats.update(iter_)  # update stats
    mainlog.debug(f"Time: {iter_} / Deers: {world.deers} / Resources: {world.resources} / Markers: {world.markers}")

# endregion


# region mainloop
with Statistics(world) as stats:
    app = PyQt5.QtWidgets.QApplication(sys.argv)
    gui_updates = QTimer()
    gui_updates.timeout.connect(animation_next)
    gui_updates.start(1000)  # delay in milliseconds
    # todo: make timer stop after T seconds. Currently it doesn't stop (see main function)
    gui = Santa_GUI(world)
    app.exec_()

    stats.analyze()

# endregion

mainlog.info(f"Final result: {world.resources}")

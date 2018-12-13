"""
Main file of the Santa Hunt project
Authors: Maximilian Janisch, Robert Scherrer, Atsuhiro Funatsu
"""

import sys
import PyQt5.QtWidgets
import PyQt5.QtCore
from enum import Enum

from logs import *
from global_variables import *
from gui import Santa_GUI
from statistics import Statistics


class Process_State(Enum):
    start = 0
    collect = 1
    produce = 2
    distribute = 3
    finished = 4


world = World("config.ini")  # reads Config and generates Resources, Locations, Deers

iter_ = 0
state_ = Process_State.start


# region Main Function
def main():  # one step of the main loop
    global iter_, state_

    if state_ == Process_State.start:
        for deer in world.deers:  # All deers leave Santa's house
            deer.move_to_collect(world.dx, world.santa_house, world.N, world.markers)
        state_ = Process_State.collect

    elif state_ == Process_State.collect:
        for deer in world.deers:
            deer.move_to_collect(world.dx, world.santa_house, world.N, world.markers)
            for location in world.locations:  # checks if the deer hit a natural resource
                if location.point_in_circle(deer.position) and not deer.resource:  # a searching deer hits a resource
                    deer.load_resource(location, world.Lp)  # deer loads resource

                    if location.amount == 0:  # checks if resource location is depleted
                        world.locations.remove(location)
                        world.resources_with_emptied_locations.append(location.resource.name)
                    else:
                        already_marked = False
                        for marker in world.markers:
                            already_marked = already_marked or (marker.location == location)
                        if not already_marked:
                            world.markers.append(deer.start_marker(location, world.santa_house.center))  # add marker
                    break  # one deer can not collect multiple Resources at once

        if iter_ % 1 < (1 / world.animation_smoothness):
            mainlog.debug(f"Time: {round(iter_)} seconds / Deers: {world.deers} / Resources: {world.resources} "
                          f"/ Markers: {world.markers}")

        # criteria to end collection
        if iter_ > world.T or (all(resource_.name in world.resources_with_emptied_locations
                                   for resource_ in world.resources)):
            mainlog.debug(f"Collection finished at time {iter_}")
            state_ = Process_State.produce
            world.markers = []  # remove all markers
            stats.analyze_collection()

    elif state_ == Process_State.produce:
        # produce toys
        world.produce_toys()
        world.calculate_distribution()
        state_ = Process_State.distribute
        # add time spent to the budget we have
        world.T_dist += iter_

        gui.show_popup(world)

    elif state_ == Process_State.distribute:
        # start distribution
        time_left = world.T_dist - iter_
        time_to_go_home = max(deer.steps_to_destination(world.dx, world.santa_house.center) for deer in world.deers)
        if time_left <= time_to_go_home:
            # go home before the kids wake up
            if all(world.santa_house.point_in_square(deer_.position) for deer_ in world.deers):
                state_ = Process_State.finished
                gui_updates.stop()
                gui.game_finished(iter_)
            for deer in world.deers:
                deer.return_to_home(world.dx, world.santa_house)
        else:
            # continue distribution
            for deer in world.deers:
                deer.move_to_distribute(world.dx, world.santa_house, world.distribution_paths)

            if abs(iter_ % 1 - 0) < (1 / world.animation_smoothness):
                mainlog.debug(f"Time: {round(iter_)} / Deers: {world.deers} / Paths: {world.distribution_paths}")

            # finish early if the job is done
            if all(path.is_finished() for path in world.distribution_paths):
                # yeah, all paths were followed successfully
                if all(deer.inactive for deer in world.deers):
                    # the deers are resting
                    mainlog.debug(
                        f"Distribution finished by {len(world.deers)} deers on {len(world.distribution_paths)} paths.")
                    state_ = Process_State.finished
                    stats.close()
                    gui_updates.stop()
                    gui.game_finished(iter_)
            

    iter_ += 1 / world.animation_smoothness
    world.gui_time += 1 / world.animation_smoothness

    for marker in world.markers:
        if marker.is_disabled():
            world.markers.remove(marker)


# endregion


# region GUI
def animation_next():
    """
    Updates the program logic and GUI
    """
    main()  # next step of loop
    gui.update_world(world)  # update
    gui.repaint()  # GUI

    stats.update(iter_)  # update stats

# endregion


# region mainloop
stats = Statistics(world)
app = PyQt5.QtWidgets.QApplication(sys.argv)
gui_updates = PyQt5.QtCore.QTimer()
gui_updates.timeout.connect(animation_next)
gui_updates.start(1000 // world.animation_smoothness)  # delay in milliseconds
# todo: make timer stop after T seconds. Currently it doesn't stop (see main function)
gui = Santa_GUI(world)
app.exec_()

# endregion

mainlog.info(f"Final result: {world.resources}")

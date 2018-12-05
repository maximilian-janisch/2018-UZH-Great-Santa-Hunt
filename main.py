"""
Main file of the Santa Hunt project
Authors: Maximilian Janisch, Robert Scherrer
"""

from time import sleep
from typing import *  # library for type hints

from logs import *
from global_variables import *
from statistics import Statistics

world = World("config.ini")  # reads Config and generates Resources, Locations, Deers

with Statistics(world) as stats:
    # region MAIN: Resource Hunt
    for deer in world.deers:  # All deers leave Santa's house
        deer.move(world.dx, world.santa_house, world.N, world.markers)

    for second in range(1, world.T + 1):  # main loop
        for deer in world.deers:
            deer.move(world.dx, world.santa_house, world.N, world.markers)
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

        for marker in world.markers:  # marker cleanup todo: unify marker cleanup a posteriori and in real time
            if marker.is_disabled():
                world.markers.remove(marker)

        stats.update(second)
        mainlog.debug(f"Time: {second} / Deers: {world.deers} / Resources: {world.resources} / Markers: {world.markers}")
        sleep(0.01)  # todo: replace by 1 second delay

        mainlog.info(f"Final result of collection: {world.resources}")

    # endregion

    # region MAIN: toy distribution
    world.produce_toys()
    paths = world.calculate_distribution()
    # now walk: todo

    stats.analyze()

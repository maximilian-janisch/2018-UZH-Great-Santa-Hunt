"""
Main file of the Santa Hunt project
Authors: Maximilian Janisch, Robert Scherrer
"""

import random
from time import sleep
from typing import *  # library for type hints

from classes import *
from functions import *
from logs import *
from global_variables import *


world = World("config.ini")  # reads Config

# region Generating Resources/Locations
resources = sorted(random.sample(world.resources, world.P))  # Pseudo-randomly choose P resources
resources: List[Resource] = [Resource(i, resources[i], 0) for i in
                             range(len(resources))]  # Initializes the resources using the Resource class

locations: List[Location] = []
for i in range(world.P):  # Generates pseudo-random location for each resource, assuring that no locations overlap
    radius: float = random.uniform(world.min_radius, world.max_radius)

    new_location = Location(resources[i], random_tuple(radius, world.N - radius), radius)
    collision: bool = new_location.overlap_square(world.santa_house) \
                      or any(new_location.overlap_circle(location) for location in locations)
    while collision:
        new_location = Location(resources[i], random_tuple(radius, world.N-radius), radius)
        if new_location.overlap_square(world.santa_house) \
                or any(new_location.overlap_circle(location) for location in locations):
            # collision detection with Santa's house and previous locations
            continue
        break
    locations.append(new_location)
mainlog.debug(f"Generated {world.P} resources at the locations {locations}")
# endregion

# region Deers
deers: List[Deer] = [Deer(i, world.santa_house.center) for i in range(world.D)]  # initialize deers
mainlog.info(f"{world.D} deers have {world.T} seconds to collect the resources")
# endregion

# region Resource Hunt
markers: List[Marker] = []  # list of markers left behind by the deers

for deer in deers:  # All deers leave Santa's house
    deer.move(world.dx, world.santa_house, world.N, markers)

for second in range(1, world.T + 1):  # main loop
    for deer in deers:
        deer.move(world.dx, world.santa_house, world.N, markers)
        for location in locations:  # checks if the deer hit a natural resource
            if location.point_in_circle(deer.position) and not deer.resource:  # a searching deer hits a resource
                deer.load_resource(location, world.Lp)  # deer loads resource

                if location.amount == 0:  # checks if resource location is depleted
                    locations.remove(location)
                else:
                    already_marked = False
                    for marker in markers:
                        already_marked = already_marked or (marker.location == location)
                    if not already_marked:
                        markers.append(deer.start_marker(location, world.santa_house.center))  # add marker
                break  # one deer can not collect multiple Resources at once

    for marker in markers:  # marker cleanup
        if marker.is_disabled():
            markers.remove(marker)

    mainlog.debug(f"Time: {second} / Deers: {deers} / Resources: {resources} / Markers: {markers}")
    sleep(0.01)  # todo: replace by 1 second delay

mainlog.info(f"Final result: {resources}")

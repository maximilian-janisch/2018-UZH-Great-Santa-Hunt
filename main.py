import configparser
import random
from time import sleep
from typing import *  # library for type hints

from classes import *
from functions import *
from logs import *

# region Read Config
config = configparser.ConfigParser()
config.read("config.ini")

N = eval(config["General"]["N"])
P = eval(config["General"]["P"])

resources = eval(config["Environment"]["Resources"])

max_radius = eval(config["General"]["maximum_radius"])
min_radius = eval(config["General"]["minimum_radius"])
prec = eval(config["General"]["precision"])

max_deers = eval(config["General"]["maximum_deers"])
min_deers = eval(config["General"]["minimum_deers"])

max_time = eval(config["General"]["maximum_time"])
min_time = eval(config["General"]["minimum_time"])

dx = eval(config["Deers"]["dx"])
Lp = eval(config["Deers"]["Lp"])

epsilon = eval(config["General"]["epsilon"])  # todo: Unused variable?
mainlog.info("-"*40 + "\nLoaded all variables from config.ini")
# endregion

# region Santa's House
santa_house = House(random_tuple(prec, N / 20, N - N / 20), N / 20)
# fixme: House range should be [0, N] x [0, N], not [N / 20, N - N / 20] x ...
mainlog.debug(f"Generated Santa's house at {santa_house.center}")
# endregion

# region Generating Resources/Locations
resources = sorted(random.sample(resources, P))  # Pseudo-randomly choose P resources
resources: List[Resource] = [Resource(i, resources[i], 0) for i in
                             range(len(resources))]  # Initializes the resources using the Resource class

locations: List[Location] = []
for i in range(P):  # Generates pseudo-random location for each resource, assuring that no locations overlap
    radius: float = round(random.uniform(min_radius, max_radius), prec)

    new_location = Location(resources[i], random_tuple(prec, radius, N - radius), radius)
    collision: bool = new_location.overlap_square(santa_house) \
                      or any(new_location.overlap_circle(location) for location in locations)
    while collision:
        new_location = Location(resources[i], random_tuple(prec, radius, N-radius), radius)
        if new_location.overlap_square(santa_house) \
                or any(new_location.overlap_circle(location) for location in locations):
            # collision detection with Santa's house and previous locations
            continue
        break
    locations.append(new_location)
mainlog.debug(f"Generated {P} resources at the locations {locations}")
# endregion

# region Deers / Time
D: int = random.randint(min_deers, max_deers)  # amount of deers
T: int = random.randint(min_time, max_time)  # provided time

deers: List[Deer] = [Deer(i, santa_house.center) for i in range(D)]  # initialize deers
mainlog.info(f"{D} deers have {T} seconds to collect the resources")
# endregion

# region Resource Hunt
markers: List[Marker] = []  # list of markers left behind by the deers

for deer in deers:  # All deers leave Santa's house
    deer.move(dx, prec, santa_house, N, markers)

for second in range(1, T + 1):  # main loop
    for deer in deers:
        deer.move(dx, prec, santa_house, N, markers)
        for location in locations:  # checks if the deer hit a natural resource
            dp = deer.position
            lc = location.center
            lr = location.radius
            if location.point_in_circle(deer.position) and not deer.resource:  # a searching deer hits a natural resource
                deer.load_resource(location, Lp)  # deer loads resource

                if location.amount == 0:  # checks if resource location is depleted
                    locations.remove(location)
                else:
                    already_marked = False
                    for marker in markers:
                        already_marked = already_marked or (marker.location == location)
                    if not already_marked:
                        markers.append(deer.start_marker(location, santa_house.center))  # add marker
                break  # one deer can not collect multiple Resources at once

    for marker in markers:  # marker cleanup
        if marker.is_disabled():
            markers.remove(marker)

    mainlog.debug(f"Time: {second} / Deers: {deers} / Resources: {resources} / Markers: {markers}")
    sleep(0.01)  # 1 second delay

mainlog.info(f"Final result: {resources}")

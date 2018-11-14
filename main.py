import configparser
import random
from time import sleep
from typing import *  # library for type hints

from classes import *
from functions import *

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
# endregion

# region Generating Resources
resources = sorted(random.sample(resources, P))  # Pseudo-randomly choose P resources
resources: List[Resource] = [Resource(i, resources[i], 0) for i in
                             range(len(resources))]  # Initializes the resources using the Resource class

locations: List[Locations] = []
for i in range(P):  # Generates pseudo-random location for each resource
    locations.append(
        Locations(resources[i], random_tuple(prec, 0, N), round(random.uniform(min_radius, max_radius), prec)))
print(locations)
# endregion

# region Santa's House
santa_house = House(random_tuple(prec, 0, N), N / 20)
print(f"Santas House at {santa_house.center}")
# endregion

# region Deers / Time
D: int = random.randint(min_deers, max_deers)  # amount of deers
T: float = round(random.uniform(min_time, max_time), prec)  # provided time

deers: List[Deer] = [Deer(i, santa_house.center) for i in range(D)]  # initialize deers

# endregion

# region Resource Hunt
markers: List[Tuple[float]] = []  # list of markers left behind by the deers

for deer in deers:  # All deers leave Santa's house
    deer.move(dx, prec, santa_house, N)

while True:  # main loop
    for deer in deers:
        deer.move(dx, prec, santa_house, N)
        for location in locations:  # checks if the deer hit a natural resource
            if location.collision(deer.position) and not deer.resource:  # a searching deer hits a natural resource
                deer.resource = location.resource
                deer.loaded = min(location.amount, Lp)
                markers.append(deer.position)  # add marker

                location.amount = max(0, location.amount - Lp)
                print(location)
                if location.amount == 0:  # checks if resource location is depleted
                    locations.remove(location)
                break  # one deer can not collect to Resources at once
    print(deers)
    print(resources)
    sleep(1)  # 1 second delay



import configparser
import random

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
# endregion

# region Generating Resources
resources = sorted(random.sample(resources, P))  # Pseudo-randomly choose P resources
resources = [Resource(i, resources[i], 0) for i in
             range(len(resources))]  # Initializes the resources using the Resource class

locations = []
for i in range(P):  # Generates pseudo-random location for each resource
    locations.append(Locations(resources[i], random_tuple(prec, 0, N), round(random.uniform(min_radius, max_radius), prec)))





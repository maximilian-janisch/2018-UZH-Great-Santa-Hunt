"""
Global variables used in main.py get initialized (mainly) here
Authors: Maximilian Janisch, Atsuhiro Funatsu
"""

__all__ = ("World",)

import configparser
import os
import random
from typing import *

from classes import *
from classes2 import *
from functions import *
from logs import *


class World:
    def __init__(self, file):
        """
        Reads the configuration file
        :param file: path to the file config file
        """
        # region Read Config
        if not os.path.isfile(file):
            mainlog.warn(f"Error while reading configuration: {file} is not a valid file path")

        config = configparser.ConfigParser()
        config.read(file)
        
        self.colours = eval(config['GUI']['Resource_Colours'])

        self.N = eval(config["General"]["N"])
        self.P = eval(config["General"]["P"])
        self.K = eval(config["General"]["K"])

        self.resources = eval(config["Environment"]["Resources"])
        self.kids = eval(config["Environment"]["Kids"])
        self.toys = eval(config["Environment"]["Toys"])

        self.max_radius = eval(config["General"]["maximum_radius"])
        self.min_radius = eval(config["General"]["minimum_radius"])

        self.max_deers = eval(config["General"]["maximum_deers"])
        self.min_deers = eval(config["General"]["minimum_deers"])

        self.max_time = eval(config["General"]["maximum_time"])
        self.min_time = eval(config["General"]["minimum_time"])

        self.max_kids = eval(config["General"]["maximum_kids"])
        self.min_kids = eval(config["General"]["minimum_kids"])

        self.dx = eval(config["Deers"]["dx"])
        self.Lp = eval(config["Deers"]["Lp"])

        mainlog.info("-" * 40)
        mainlog.info(f"Loaded all variables from {file}")
        # endregion
        
        # region GUI
        self.scale = 800 / self.N
        # endregion

        self.markers: List[Marker] = []

        # region Initialize pseudo-random
        self.D = random.randint(self.min_deers, self.max_deers)  # amount of deers
        self.T = random.randint(self.min_time, self.max_time)  # provided time
        self.santa_house: House = House(random_tuple(self.N / 20, self.N * 19 / 20), self.N / 20)
        mainlog.debug(f"Generated Santa's house at {self.santa_house.center}")
        # endregion

        # region Generating Resources
        resources = sorted(random.sample(self.resources, self.P))  # Pseudo-randomly choose P resources
        self.resources: List[Resource] = [Resource(i, resources[i], 0) for i in
                                          range(len(resources))]  # Initializes the resources using the Resource class
        # endregion

        # region Generating Locations
        self.locations: List[Location] = []
        for i in range(self.P):
            # Generates pseudo-random location for each resource, assuring that no locations overlap
            radius: float = random.uniform(self.min_radius, self.max_radius)

            new_location = Location(self.resources[i], random_tuple(radius, self.N - radius), radius)
            collision: bool = new_location.overlap_square(self.santa_house) \
                              or any(new_location.overlap_circle(location) for location in self.locations)
            while collision:
                new_location = Location(self.resources[i], random_tuple(radius, self.N - radius), radius)
                if new_location.overlap_square(self.santa_house) \
                        or any(new_location.overlap_circle(location) for location in self.locations):
                    # collision detection with Santa's house and previous locations
                    continue
                break
            self.locations.append(new_location)
        mainlog.debug(f"Generated {self.P} resources at the locations {self.locations}")
        # endregion

        # region Generating kids' houses
        self.kids_houses = []
        for i in range(self.K):
            # Locations for each kid's house, assuring that nothing overlaps
            kids_house = House(random_tuple(self.N / 80, self.N * 79 / 80), self.N / 40)

            collision: bool = kids_house.overlap_square(self.santa_house) \
                              or any(location.overlap_square(kids_house) for location in self.locations) \
                              or any(house.overlap_square(kids_house) for house in self.kids_houses)

            while collision:
                kids_house = House(random_tuple(self.N / 80, self.N * 79 / 80), self.N / 40)
                if kids_house.overlap_square(self.santa_house) \
                        or any(location.overlap_square(kids_house) for location in self.locations) \
                        or any(house.overlap_square(kids_house) for house in self.kids_houses):
                    # collision detection with Santa's house, with circles and previous kids_houses
                    continue
                break
            self.kids_houses.append(kids_house)
        mainlog.debug(f"Generated {self.K} kids houses: {self.kids_houses}")
        # endregion

        # region Deers
        self.deers: List[Deer] = [Deer(i, self.santa_house.center) for i in range(self.D)]  # initialize deers
        mainlog.info(f"{self.D} deers have {self.T} seconds to collect the resources")
        # endregion

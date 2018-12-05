"""
Global variables used in main.py get initialized (mainly) here
Author: Maximilian Janisch
"""

__all__ = ("World",)

import configparser
import os
import random
from typing import *
import numpy as np

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

        self.N = eval(config["General"]["N"])
        self.P = eval(config["General"]["P"])
        self.K = eval(config["General"]["K"])

        self.resource_names = eval(config["Environment"]["Resources"])
        self.kid_names = eval(config["Environment"]["Kids"])
        self.toy_names = eval(config["Environment"]["Toys"])

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

        self.markers: List[Marker] = []

        # region Initialize pseudo-random
        self.D = random.randint(self.min_deers, self.max_deers)  # amount of deers
        self.T = random.randint(self.min_time, self.max_time)  # provided time
        self.santa_house: House = House(random_tuple(self.N / 20, self.N * 19 / 20), self.N / 20)
        mainlog.debug(f"Generated Santa's house at {self.santa_house.center}")
        # endregion

        # region Generating Resources
        resources = sorted(random.sample(self.resource_names, self.P))  # Pseudo-randomly choose P resources
        self.resources: List[Resource] = [Resource(i, resources[i], 0) for i in
                                          range(len(resources))]  # Initializes the resources using the Resource class
        # endregion

        # region Generating Toy types
        self.toy_types = []
        for i, name in enumerate(self.toy_names):
            self.toy_types.append(Toy_Type(i, self.resources, name))
        self.toy_types.sort(key=lambda Toy_Type: Toy_Type.toy_grade, reverse=True)
        # endregion

        # region Generating Locations
        self.locations: List[Location] = self.create_locations()

        # region Generating kids' houses
        self.kids_houses = self.create_kids_houses()

        # region Generating Kids
        self.kids = []
        for i, house in enumerate(self.kids_houses):
            self.kids.append(Kid(i, self.kid_names[random.randint(1,len(self.kid_names)-1)], house))            
        self.kids.sort(key=lambda Kid: Kid.kid_grade, reverse=True)
        # endregion

        # region initializing empty Toys list for later use in production
        self.toys = []
        # endregion

        # region Deers
        self.deers: List[Deer] = [Deer(i, self.santa_house.center) for i in range(self.D)]  # initialize deers
        mainlog.info(f"{self.D} deers have {self.T} seconds to collect the resources")
        # endregion
        
        self.distribution_paths = []
        
    def create_locations(self) -> List[Location]:
        """
        Generating Locations
        """
        result: List[Location] = []
        for i in range(self.P):
            # Generates pseudo-random location for each resource, assuring that no locations overlap
            radius: float = random.uniform(self.min_radius, self.max_radius)

            new_location = Location(self.resources[i], random_tuple(radius, self.N - radius), radius)
            collision: bool = new_location.overlap_square(self.santa_house) \
                              or any(new_location.overlap_circle(location) for location in result)
            while collision:
                new_location = Location(self.resources[i], random_tuple(radius, self.N - radius), radius)
                if new_location.overlap_square(self.santa_house) \
                        or any(new_location.overlap_circle(location) for location in result):
                    # collision detection with Santa's house and previous locations
                    continue
                break
            result.append(new_location)
        mainlog.debug(f"Generated {self.P} resources at the locations {result}")
        return result

    def create_kids_houses(self) -> List[House]:
        """
        Generating the kids houses
        """
        result: List[House] = []
        for i in range(self.K):
            # Locations for each kid's house, assuring that nothing overlaps
            kids_house = House(random_tuple(self.N / 80, self.N * 79 / 80), self.N / 40)

            collision: bool = kids_house.overlap_square(self.santa_house) \
                              or any(location.overlap_square(kids_house) for location in self.locations) \
                              or any(house.overlap_square(kids_house) for house in result)

            while collision:
                kids_house = House(random_tuple(self.N / 80, self.N * 79 / 80), self.N / 40)
                if kids_house.overlap_square(self.santa_house) \
                        or any(location.overlap_square(kids_house) for location in self.locations) \
                        or any(house.overlap_square(kids_house) for house in result):
                    # collision detection with Santa's house, with circles and previous kids_houses
                    continue
                break
            result.append(kids_house)

        mainlog.debug(f"Generated {self.K} kids houses: {result}")
        return result

    def calculate_distribution(self)-> None:
        """
        takes all kids in the world and assigns them to a list of distribution
        paths that the deers can follow to dirstribute the toys
        As a deer can load max 3 toys, there should be max 3 kids per path
        """
        # calculate angles and set angle in Houses.angle to angle (in degrees):
        for location in self.kids_houses:
            x = location.center[0] - self.santa_house.center[0]
            y = location.center[1] - self.santa_house.center[1]
            location.angle = np.arcsin(x/y)*180/np.pi


        # sort for the angles (not sure wheather increasing or decreasing angle,
        # but doesn't matter here)
        self.kids.sort(key=lambda Kid: Kid.house.angle, reverse=True)

        #create list of list
        #here we have a list in a list
        result = []
        lucky_kids = [] # kids that will recieve toys
        for i in self.kids:
            if i.toy:
                lucky_kids.append(i)

        result = chunkIt(lucky_kids, self.D)
        return result


    def produce_toys(self)-> None:
        """
        take all the resources collected and build the toys
        in order of the toys value (i.e. rank)
        """
        """After the resource collection, the toys will be produced according the grading"""
        # build toys
        for toy_type in self.toy_types:
            enough = True
            while enough:
                for r in self.resources:
                    demand = toy_type.resource_list.count(r)
                    supply = r.collected
                    if demand > supply:
                        # checks whether the number for collected resources is > 0
                        enough = False
                if enough:
                    self.toys.append(Toy(toy_type))
                    mainlog.debug("Produced toy {}".format(toy_type.toy_name))


        # After the production of toys they will be assigned to the kids
        number_to_distribute = min(len(self.toys), len(self.kids))
        mainlog.debug("{} Toys and {} Kids".format(len(self.toys), len(self.kids)))
        for i in range(number_to_distribute):
            self.kids[i].assign_toy(self.toys[i])
            mainlog.debug("Kid {} will get toy {}".format(self.kids[i].name, self.toys[i].toy_type.toy_name))
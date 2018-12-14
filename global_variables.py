"""
Global variables used in main.py get initialized (mainly) here
Authors: Maximilian Janisch, Robert Scherrer, Atsuhiro Funatsu
"""

__all__ = ("World",)

import configparser
import os
import random
from typing import *

from classes import *
from classes2 import *
from deer import *
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

        self.animation_smoothness = eval(config['GUI']['smoothness'])
        self.colours = eval(config['GUI']['Resource_Colours'])

        self.N = eval(config["General"]["N"])
        self.P = eval(config["General"]["P"])
        self.K = eval(config["General"]["K"])
        self.kids_house_size = eval(config["General"]["kids_house_size"])
        if self.kids_house_size == -1:
            self.kids_house_size = self.N / 40

        self.resource_names = eval(config["Environment"]["Resources"])
        self.kid_names = eval(config["Environment"]["Kids"])
        self.toy_names = eval(config["Environment"]["Toys"])

        self.max_radius = eval(config["General"]["maximum_radius"])
        self.min_radius = eval(config["General"]["minimum_radius"])

        self.max_deers = eval(config["General"]["maximum_deers"])
        self.min_deers = eval(config["General"]["minimum_deers"])

        self.max_time = eval(config["General"]["maximum_time"])
        self.min_time = eval(config["General"]["minimum_time"])

        self.max_resources = eval(config["General"]["maximum_locations_per_resource"])
        self.min_resources = eval(config["General"]["minimum_locations_per_resource"])

        self.dx = eval(config["Deers"]["dx"])/self.animation_smoothness
        self.Lp = eval(config["Deers"]["Lp"])

        mainlog.info("-" * 40)
        mainlog.info(f"Loaded all variables from {file}")
        # endregion

        # region GUI
        self.scale = 800 / self.N
        self.gui_time = 0
        self.latest_event = 'Latest event:'
        self.happy_kids_list = [] # used for 'latest event' in GUI
        # endregion

        self.markers: List[Marker] = []
        self.resources_with_emptied_locations = []

        # region Initialize pseudo-random
        self.D = random.randint(self.min_deers, self.max_deers)  # amount of deers
        self.T = random.randint(self.min_time, self.max_time)  # provided time for collection
        self.T_dist = 1000  # time for distribution
        self.santa_house: House = House(random_tuple(self.N / 20, self.N * 19 / 20), self.N / 20)
        mainlog.debug(f"Generated Santa's house at {self.santa_house.center}")
        # endregion

        # region Generating Resources
        resources = sorted(random.sample(self.resource_names, self.P))  # Pseudo-randomly choose P resources
        self.resources = []
        for i in range(len(resources)):
            self.resources.append(Resource(i, resources[i], 0))
        # endregion

        # region Generating Toy types
        self.toy_types = []
        for i, name in enumerate(self.toy_names):
            self.toy_types.append(Toy_Type(i, self.resources, name))
        self.toy_types.sort(reverse=True)
        # endregion

        # region Generating Locations
        self.locations: List[Location] = self.create_locations()

        # region Generating kids' houses
        self.kids_houses = self.create_kids_houses()

        # region Generating Kids
        self.kids = []
        for i, house in enumerate(self.kids_houses):
            self.kids.append(Kid(i, self.kid_names[random.randint(1, len(self.kid_names) - 1)], house))
        self.kids.sort(reverse=True)
        # endregion

        # region initializing empty Toys list for later use in production
        self.toys = []
        # endregion

        # region Deers
        self.deers: List[Deer] = [Deer(i, self.santa_house.center, self.animation_smoothness)
                                  for i in range(self.D)]  # initialize deers
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

            amount = random.randint(self.min_resources, self.max_resources)
            for iter__ in range(amount):
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
            kids_house = House(random_tuple(self.N / 80, self.N * 79 / 80), self.kids_house_size)

            collision: bool = kids_house.overlap_square(self.santa_house) \
                              or any(location.overlap_square(kids_house) for location in self.locations) \
                              or any(house.overlap_square(kids_house) for house in result)

            while collision:
                kids_house = House(random_tuple(self.N / 80, self.N * 79 / 80), self.kids_house_size)
                if kids_house.overlap_square(self.santa_house) \
                        or any(location.overlap_square(kids_house) for location in self.locations) \
                        or any(house.overlap_square(kids_house) for house in result):
                    # collision detection with Santa's house, with circles and previous kids_houses
                    continue
                break
            result.append(kids_house)

        mainlog.debug(f"Generated {self.K} kids houses: {result}")
        return result

    def calculate_distribution(self) -> None:
        """
        takes all kids in the world and assigns them to a list of distribution
        paths that the deers can follow to distribute the toys
        As a deer can load max 3 toys, there should be max 3 kids per path
        """
        lucky_kids = [i for i in self.kids if i.toy]  # kids that will receive toys

        lucky_kids_chunks = [[]]
        while lucky_kids:
            if len(lucky_kids_chunks[-1]) == 3:
                lucky_kids_chunks.append([])
            elif len(lucky_kids_chunks[-1]) > 0:
                kid_minimal_distance_index = 0
                for i in range(1, len(lucky_kids)):
                    kid = lucky_kids[i]
                    if euclidean_norm(
                            (kid.house.center[0] - lucky_kids_chunks[-1][-1].house.center[0],
                             kid.house.center[1] - lucky_kids_chunks[-1][-1].house.center[1]
                             )) <= euclidean_norm(
                            (lucky_kids[kid_minimal_distance_index].house.center[0] - lucky_kids_chunks[-1][-1].house.center[0],
                             lucky_kids[kid_minimal_distance_index].house.center[1] - lucky_kids_chunks[-1][-1].house.center[1]
                             )):
                        kid_minimal_distance_index = i

                lucky_kids_chunks[-1].append(lucky_kids.pop(kid_minimal_distance_index))

            else:  # lucky_kids last chunk is empty
                lucky_kids_chunks[-1].append(lucky_kids[0])
                lucky_kids.pop(0)

        for each in lucky_kids_chunks:
            self.distribution_paths.append(Distribution_Path(each))

        mainlog.debug(f"Planned {len(self.distribution_paths)} paths for {self.D} deers to distribute to {len(lucky_kids)} Kids")

    def produce_toys(self) -> None:
        """
        take all the resources collected and build the toys
        in order of the toys value (i.e. rank)

        After the resource collection, the toys will be produced according the grading
        """
        # build toys
        depleted_toy_names = []
        while len(depleted_toy_names) < len(self.toy_types):
            toy_type = random.choice(self.toy_types)

            while toy_type.toy_name in depleted_toy_names:
                toy_type = random.choice(self.toy_types)

            enough = True
            for r in self.resources:
                demand = toy_type.resource_list.count(r)
                supply = r.collected
                if demand > supply:
                    # checks whether the number for collected resources is > 0
                    enough = False
                    if toy_type.toy_name not in depleted_toy_names:
                        depleted_toy_names.append(toy_type.toy_name)
            if enough:
                self.toys.append(Toy(toy_type))
                mainlog.debug("Produced toy {}".format(toy_type.toy_name))

        # After the production of toys they will be assigned to the kids
        number_to_distribute = min(len(self.kids), len(self.toys))
        mainlog.debug("{} Toys and {} Kids".format(len(self.toys), len(self.kids)))
        for i in range(number_to_distribute):
            self.kids[i].assign_toy(self.toys[i])
            mainlog.debug("Kid {} will get toy {}".format(self.kids[i].name, self.toys[i].toy_type.toy_name))

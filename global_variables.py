"""
Global variables used in main.py get initialized (mainly) here
Author: Maximilian Janisch
"""

__all__ = ("World",)

import configparser
import os
import random

from classes import *
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

        self.resources = eval(config["Environment"]["Resources"])
        self.max_radius = eval(config["General"]["maximum_radius"])
        self.min_radius = eval(config["General"]["minimum_radius"])

        self.max_deers = eval(config["General"]["maximum_deers"])
        self.min_deers = eval(config["General"]["minimum_deers"])

        self.max_time = eval(config["General"]["maximum_time"])
        self.min_time = eval(config["General"]["minimum_time"])

        self.dx = eval(config["Deers"]["dx"])
        self.Lp = eval(config["Deers"]["Lp"])
        mainlog.info("-" * 40)
        mainlog.info("Loaded all variables from {file}")
        # endregion

        # region Initialize pseudo-random
        self.D = random.randint(self.min_deers, self.max_deers)  # amount of deers
        self.T = random.randint(self.min_time, self.max_time)  # provided time
        self.santa_house: House = House(random_tuple(self.N/20, self.N * 19/20), self.N/20)
        mainlog.debug(f"Generated Santa's house at {self.santa_house.center}")
        # endregion

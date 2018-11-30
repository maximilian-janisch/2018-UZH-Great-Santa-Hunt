"""
File for classes that are not responsible for geometry, such as Kid and Toy
Author: Reetta Välimäki, Maximilian Janisch
"""

__all__ = ("Kid", "Toy")

import random
from typing import *  # library for type hints

from logs import *


class Kid:
    def __init__(self, index: int, name: str, house):
        """Initialises the Kid class"""
        self.kid_grade = random.randint(1, 6)
        self.name = name
        self.house = house
        self.received = False
        self.index = index

    def receiving_gift(self):  # remark: this doesn't really need a function of it's own
        """Sets self.received to True"""
        self.received = True


class Toy:
    def __init__(self, toy_name: str):
        self.resource_list = random.sample(self.resources, 3)
        self.toy_name = toy_name
        self.toy_grade = random.randint(1, 6)

    def toy_production(self):
        """After the resource collection, the toys will be produced according the grading"""
        self.produced_toys = []
        for x in toys:
            if self.toy_grade == 1: # To do: need to make this into a for loop
                if set(self.resource_list).issubset(collected_resources): #To do: check the list of collected_resources
                    self.produced_toys.append(self.toy_name)
                    break
                else:
                    continue
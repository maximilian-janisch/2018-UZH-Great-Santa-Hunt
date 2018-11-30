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
        self.kid_list_sorted = kids.sort(key=kid_grade, reverse=True)

    def receiving_gift(self):  # remark: this doesn't really need a function of it's own
        """Sets self.received to True"""
        self.received = True

class Toy:
    def __init__(self, toy_name: str):
        self.resource_list = sorted(random.sample(self.resources, 3)) #random sample of resources for a toy to be produced
        self.toy_name = toy_name
        self.toy_grade = random.randint(1, 6)
        self.toy_list_sorted = toys.sort(key=toy_grade, reverse=True)

    def toy_production(self):
        """After the resource collection, the toys will be produced according the grading"""
        self.produced_toys = []
        for x in toy_list_sorted:
            for z in self.resource_list:
                if z.collected > 0: #checks whether the number for collected resources is > 0
                    continue
                else:
                    break
            self.produced_toys.append(x)

    def toy_assigning(self):
        """After the production of toys they will be assigned to the kids"""
        self.toys_kids = [produced_toys, kid_list_sorted]




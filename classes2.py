"""
File for classes that are not responsible for geometry, such as Kid and Toy
Authors: Reetta Välimäki, Maximilian Janisch
"""

__all__ = ("Kid", "Toy")

import random


from typing import *  # library for type hints
from classes import *
from logs import *


class Kid:
    def __init__(self, index: int, name: str, house: House):
        """Initialises the Kid class"""
        self.kid_grade = random.randint(1, 6)
        self.name = name
        self.house = house
        self.received = False
        self.index = index



        # fixme (fatal): unresolved reference "kids"

class Toy:
    def __init__(self, toy_name: str):
        self.resource_list = sorted(random.sample(resources, 3)) #random sample of resources for a toy to be produced
        # fixme (fatal): unresolved reference "World" (note that the world class gets initialized in main.py)

        self.toy_name = toy_name
        self.toy_grade = random.randint(1, 6) #fix
        # fixme (fatal): unresolved reference "toys"
        self.toys_kids = []
        self.produced_toys = []

    def toy_production(self):
        """After the resource collection, the toys will be produced according the grading"""
        for x in self.toy_list_sorted:
            for z in self.resource_list:
                if z.collected > 0: # checks whether the number for collected resources is > 0
                    continue
                else:
                    break
            self.produced_toys.append(x)

    def toy_assigning(self):
        """After the production of toys they will be assigned to the kids"""
        self.toys_kids = [kids, self.toy_list_sorted, Kid.kid_list_sorted] # The table for toys and kids

"""
File for classes that are not responsible for geometry, such as Kid and Toy
Authors: Reetta Välimäki, Maximilian Janisch
"""

__all__ = ("Kid", "Toy", "Toy_Type", "Distribution_Path")

import random


from typing import *  # library for type hints
from classes import *
from logs import *


class Toy_Type:
    """
    """
    def __init__(self, seq: int, resources: List[Resource], toy_name: str):
        self.resource_list = random.sample(resources, 3)  
        # fixme: we need to be able to have a longer list of resources
        # random sample of resources for a toy to be produced
        self.toy_name = toy_name
        self.toy_grade = seq
        

class Toy:
    def __init__(self, toy_type: Toy_Type):
        self.toy_type = toy_type
        # when one toy is procuced, it should "use" the resources needed
        for r in toy_type.resource_list:
            r.collected -= 1


class Kid:
    """
    A single kid 
    """
    def __init__(self, index: int, name: str, house: House):
        """
        Initialises the Kid class
        :param index: numbering of the kids
        :param name: name of the kids
        :param house: the house the kid lives in 
        """
        self.kid_grade = random.randint(1, 6)  # a kid can have been very nasty this year
        self.name = name
        self.house = house
        self.received = False  # todo: how to propagate state to color of house?
        self.index = index
        self.toy = None

    def assign_toy(self, toy: Toy)-> None:
        """
        """
        self.toy = toy


class Distribution_Path:
    """
    A path that a deer can follow to distribute the toys
    """
    
    def __init__(self, kids: List[Kid]):
        self.kids: List[Kid] = kids
#        self.position = 0
    
    def add_kid(self, additional_kid: Kid) -> None:
        if not additional_kid.toy:
            raise IndexError("Distribution_Path must not contain kids that won't get a toy.")
        self.kids.append(additional_kid)
    
    def get_size(self)-> int:
        return size (self.kids)




"""
File for classes that are not responsible for geometry, such as Kid and Toy
Authors: Reetta Välimäki, Maximilian Janisch
"""

__all__ = ("Kid", "Toy", "Toy_Type", "Distribution_Path")

import random
from typing import *  # library for type hints

from classes import *


class Toy_Type:
    """
    A single toy type
    """
    def __init__(self, seq: int, resources: List[Resource], toy_name: str):
        """
        Initialises the Toy Class
        :param seq: index
        :param resources: list of the resources that the toy type needs in order to be produced
        :param toy_name: the name of the toy, e.g. chocolate
        """
        self.resource_list = [random.choice(resources) for x in range(1, 5)]
        # random sample of resources for a toy to be produced
        self.toy_name = toy_name
        self.toy_grade = seq

    def __repr__(self):
        return f"Toy Type '{self.toy_name}'"
    
    def __int__ (self)-> int:
        return len(self.resource_list)
        
    def __eq__(self, other)-> bool:
        return int(self) == int(other)

    def __lt__(self, other)-> bool:
        return int(self) < int(other)

    def __gt__(self, other)-> bool:
        return int(self) > int(other)

    def __ne__(self, other)-> bool:
        return not self.__eq__(other)
    
    def __le__(self, other)-> bool:
        return not self.__gt__(other)

    def __ge__(self, other)-> bool:
        return not self.__lt__(other)


class Toy:
    def __init__(self, toy_type: Toy_Type):
        self.toy_type = toy_type
        # when one toy is procuced, it should "use" the resources needed
        for r in toy_type.resource_list:
            r.collected -= 1

    def __repr__(self):
        return f"Toy '{self.toy_type.toy_name}'"


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
        self.received = False
        self.index = index
        self.toy = None

    def __repr__(self):
        return f"Kid '{self.name}' living at {self.house.center}"
    
    def __int__ (self)-> int:
        return self.kid_grade

    def __eq__(self, other)-> bool:
        return int(self) == int(other)

    def __lt__(self, other)-> bool:
        return int(self) < int(other)

    def __gt__(self, other)-> bool:
        return int(self) > int(other)

    def __ne__(self, other)-> bool:
        return not self.__eq__(other)
    
    def __le__(self, other)-> bool:
        return not self.__gt__(other)

    def __ge__(self, other)-> bool:
        return not self.__lt__(other)

    def assign_toy(self, toy: Toy)-> None:
        """
        assigns the toy the kid will receive
        """
        self.toy = toy

    def give_toy(self)-> None:
        """
        give the toy to the kid
        """
        self.received = True

    def got_toy(self)-> bool:
        """
        returns true if kid has got the toy already
        """
        return self.received


class Distribution_Path:
    """
    A path that a deer can follow to distribute the toys
    """

    def __init__(self, kids: List[Kid]):
        self.kids: List[Kid] = kids
        self.picked_by_deer = False

    def __repr__(self):
        return f"Path with {self.left_to_distribute()} toys left to distribute to kids {self.kids}"

    def get_size(self)-> int:
        return len(self.kids)

    def pick(self)-> None:
        if self.picked_by_deer:
            raise IndexError("Distribution_Path.pick: only one deer allowed")
        self.picked_by_deer = True

    def is_picked(self)-> bool:
        return self.picked_by_deer

    def is_finished(self)-> bool:
        try:
            return self.kids[-1].got_toy()
        except IndexError:
            return True

    def get_next_kid(self)-> Kid:
        for k in self.kids:
            if k.got_toy():
                continue
            else:
                return k
        raise IndexError("Distribution_Path.get_next_kid, no more unhappy kids:-)")

    def get_next_house(self) -> House:
        return self.get_next_kid().house

    def left_to_distribute(self)-> int:
        result = 0
        for k in self.kids:
            if not k.got_toy():
                result += 1
        return result

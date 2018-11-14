"""
(Helper) classes that are used by other files in this project are specified here.
Author: Maximilian Janisch
"""

__all__ = ("Resource", "Locations", "House", "Deer")

from math import *
import random

from typing import Tuple  # library for type hints

from functions import *


class Resource:
    def __init__(self, index: int, name: str, collected: int):
        """
        Initializes the Resource class
        :param index: The identifier of the resource
        :param name: String which specifies the name of the resource
        :param collected: Amount of collected units
        """
        self.index = index
        self.name = name
        self.collected = collected

    def __repr__(self):
        return f"Resource #{self.index} | {self.name} | collected {self.collected}"

    def deposit(self, amount: int):
        print(f"depositing {amount} {self}")
        self.collected += amount


class Locations:
    def __init__(self, resource: Resource, center: Tuple[float], radius: float):
        """
        Initializes the Locations class
        :param resource: A Resource class
        :param center: Center of resource location
        :param radius: Radius of resource location
        """
        self.resource = resource
        self.center = center
        self.radius = radius
        self.amount = floor(pi * (radius ** 2))

    def __repr__(self):
        return f"Location of \"{self.resource}\" | center {self.center} | radius {self.radius} | amount {self.amount}"

    def collision(self, point: Tuple[float]):
        if euclid((self.center[0] - point[0], self.center[1] - point[1])) <= self.radius:
            return True
        else:
            return False


class House:
    def __init__(self, center: Tuple[float], size: int):
        """
        Initializes the House class
        :param center: center of the house
        :param size: size of the house (square form)
        """
        self.center = center
        self.size = size


class Deer:
    def __init__(self, index: int, position: Tuple[float]):
        """
        Initializes the Deer class
        :param index: index of the deer
        :param position: initial position of the deer
        """
        self.index = index
        self.position = position
        self.resource: Resource = None  # loaded resource
        self.loaded: int = 0  # amount of loaded resources
        self.inactive = False  # deer rests after depositing resources

    def __repr__(self):
        state = "Return to home" if self.resource else "Searching"
        state = "Inactive" if self.inactive else state
        return f"#{self.index} | {state} | current position {self.position} | loaded {self.loaded}"

    def move(self, dx: int, prec: int, house: House, N: int):
        """
        Moves the deer either pseudo-randomly or home to Santa
        :param dx: speed of the deer
        :param prec: precision of the angle that the deer turns
        :param house: Santa's house (in order to return and deposit)
        :param N: size of the world
        """
        if self.inactive:
            self.inactive = False
            return

        home = house.center
        if not self.resource:  # deer doesn't have a resource
            theta: float = round(random.uniform(0, 360), prec)  # pseudo-random angle
            self.position = (min(max(0.0, self.position[0] + dx * cos(theta)), N),
                             min(max(0.0, self.position[1] + dx * sin(theta)), N)
                             )

        else:  # return to home mechanism
            if euclid((self.position[0] - home[0],
                       self.position[1] - home[1])) <= 1.01 * house.size:  # deer reached Santa's house, the 1.01
                # prevent the deer from being stuck at the edge of the house

                self.resource.deposit(self.loaded)
                self.loaded = 0
                self.resource = None
                self.inactive = True
                return

            direction = (home[0] - self.position[0], home[1] - self.position[1])
            direction = (dx * direction[0] / euclid(direction),
                         dx * direction[1] / euclid(direction))
            self.position = (min(max(0.0, self.position[0] + direction[0]), float(N)),
                             min(max(0.0, self.position[1] + direction[1]), float(N))
                             )

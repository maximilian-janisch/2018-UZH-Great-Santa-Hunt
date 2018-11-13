"""
(Helper) classes that are used by other files in this project are specified here.
Author: Maximilian Janisch
"""

__all__ = ("Resource", "Locations")

from math import *


class Resource:
    def __init__(self, index: int, name: str, collected: int):
        """
        Initializes the Resource class
        :param index: The identifier of the resource
        :param name: String which specifies the name of the resource
        :param collected: Amount of collected units
        :return: None
        """
        self.index = index
        self.name = name
        self.collected = collected

    def __repr__(self):
        return "Resource #{index} | {name} | collected {collected}".format(index=self.index, name=self.name,
                                                                           collected=self.collected)


class Locations:
    def __init__(self, resource: Resource, center: tuple, radius: int):
        """
        Initializes the Locations class
        :param resource: A Resource class
        :param center: Centre of resource location
        :param radius: Radius of resource location
        :return: None
        """
        self.resource = resource
        self.center = center
        self.radius = radius
        self.amount = floor(pi * (radius ** 2))

    def __repr__(self):
        return "Location of \"{resource}\" | center {center} | radius {radius} | amount {amount}".format(
            resource=self.resource, center=self.center, radius=self.radius, amount=self.amount)

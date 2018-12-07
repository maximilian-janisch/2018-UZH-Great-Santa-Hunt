"""
Classes that are responsible mainly for geometry in this project are specified here.
Authors: Maximilian Janisch, Robert Scherrer, Reetta Välimäki
"""

__all__ = ("Circle", "Square", "Resource", "Location", "House", "Marker")

from math import *
import random
from typing import *  # library for type hints

from functions import *
from logs import *
from segment_intersection import *


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
        self.collected += amount
        mainlog.debug(f"depositing {amount} to {self}")


class Square:
    def __init__(self, center: Tuple[float, float], size: float):
        """
        Initializes the Square class
        :param center: center of the house
        :param size: edge length of the square (= 2 * "radius")
        """
        self.center = center
        self.size = size

        self.left_boundary = self.center[0] - self.size / 2
        self.right_boundary = self.center[0] + self.size / 2
        self.top_boundary = self.center[1] + self.size / 2
        self.bottom_boundary = self.center[1] - self.size / 2

    def __repr__(self):
        return f"Square with \"center {self.center} | edge length {self.size}"

    def point_in_square(self, point: Tuple[float, float]) -> bool:
        """
        Returns True if point is within the square, else False
        :param point: point to check
        :return: True or False
        """
        return max_norm((point[0] - self.center[0], point[1] - self.center[1])) <= self.size / 2

    def overlap_square(self, other_square) -> bool:
        """
        Returns True if other_square overlaps this square, else False
        :param other_square: square to check
        :return: True or False
        """
        return max_norm((self.center[0] - other_square.center[0], self.center[1] - other_square.center[1])) <= \
               (self.size + other_square.size) / 2


class Circle:
    def __init__(self, center: Tuple[float, float], radius: float):
        """
        Initializes the Circle class
        :param center: Center
        :param radius: Radius
        """
        self.center = center
        self.radius = radius

    def __repr__(self):
        return f"Circle with \"center {self.center} | radius {self.radius}\""

    def point_in_circle(self, point: Tuple[float, float]) -> bool:
        """
        Returns True if point is within the circle, else False
        :param point: point to check
        :return: True or False
        """
        return euclidean_norm((self.center[0] - point[0], self.center[1] - point[1])) <= self.radius

    def overlap_square(self, square: Square) -> bool:
        """
        Returns True if square overlaps this circle, else False
        :param square: square to check
        :return: True or False
        """
        fusspunkt = (
            limit(self.center[0], square.left_boundary, square.right_boundary),
            limit(self.center[1], square.bottom_boundary, square.top_boundary)
        )

        return self.point_in_circle(fusspunkt)

    def overlap_circle(self, other_circle) -> bool:
        """
        Returns True if this circle overlaps the other_circle, else False
        :param other_circle: circle to be check
        :return: True or False
        """
        return euclidean_norm((self.center[0] - other_circle.center[0], self.center[1] - other_circle.center[1])) <= (
                self.radius + other_circle.radius)


class Location(Circle):
    def __init__(self, resource: Resource, center: Tuple[float, float], radius: float):
        """
        Initializes the Location class
        :param resource: A Resource class
        :param center: Center of resource location
        :param radius: Radius of resource location
        """
        self.resource = resource
        self.amount = floor(pi * (radius ** 2))
        super().__init__(center, radius)

    def __repr__(self):
        return f"Location of \"{self.resource}\" | center {self.center} | radius {self.radius} | amount {self.amount}"

    def pickup_resources(self, requested_amount: int) -> int:
        """
        Returns the number of ressources picked up and reduces radius accordingly
        :param requested_amount: what should be picked up
        :return: the effective amount, max the requested amount, but only as much as there is
        """
        result = min(requested_amount, self.amount)
        self.amount -= result
        self.radius = sqrt(self.amount / pi)
        return result


class House(Square):
    def __init__(self, center: Tuple[float, float], size: float):
        """
        Initializes the House class
        :param center: center of the house
        :param size: size of the house (square form)
        :arg euler angle between the santa house an the kids house
        """
        super().__init__(center, size)
        self.angle = None



class Marker:  # todo: test behaviour
    def __init__(self, location: Location, direction: Tuple[float, float]):
        """
        Initializes the Marker class
        :param location: resource location associated to the marker
        :param direction: out of which direction the marker points to the location
        """
        self.location = location  # connected location
        self.endpoint = location.center  # where the marker will be drawn to
        self.startpoint = self.endpoint  # where the maker ends, start without length
        self.direction = direction  # tells the deers in which direction to follow

    def __repr__(self):
        return f"Marker starting at {self.startpoint} associated with {self.location}"

    def line_touch(self, old_pos: Tuple[float, float],
                   new_pos: Tuple[float, float]) -> bool:
        """
        Checks if a deer traversed this marker while going from old_pos to new_pos
        :param old_pos: Old position of the deer
        :param new_pos: New position of the deer
        :return: True if the segments (old_pos -> new_pos) and (startpoint -> location.center) intersect, else False
        """
        def almost_on_segment(point: Tuple[float, float]):
            """
            Checks whether point is __almost__ on the segment from self.startpoint to self.endpoint
            :param point: Point to check
            :return:
            """
            return euclidean_norm((point[0] - self.startpoint[0], point[1] - self.startpoint[1])) \
                   + euclidean_norm((point[0] - self.endpoint[0], point[1] - self.endpoint[1])) \
                   <= euclidean_norm((self.endpoint[0] - self.startpoint[0], self.endpoint[1] - self.startpoint[1])) \
                        + 0.2  # tolerance
        return almost_on_segment(old_pos) and almost_on_segment(new_pos)

    def disable(self):
        """
        moves the marker out of the way
        future implementations could  implement a garbage collection
        """
        self.startpoint = (-1, -1)
        self.endpoint = (-1, -1)
        self.location = None

    def is_disabled(self):
        """
        returns false after call to disable
        """
        return not self.location

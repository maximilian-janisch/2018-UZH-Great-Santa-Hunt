"""
(Helper) classes that are used by other files in this project are specified here.
Author: Maximilian Janisch
"""

__all__ = ("Resource", "Location", "House", "Deer", "Marker")

from math import *
import random

from typing import *  # library for type hints

from functions import *
from logs import *


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
        mainlog.debug(f"depositing {amount} to {self}")
        self.collected += amount


class Location:
    def __init__(self, resource: Resource, center: Tuple[float, float], radius: float):
        """
        Initializes the Location class
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

    def collision(self, point: Tuple[float, float]) -> bool:
        """
        Returns True if point is within the circle, else False
        :param point: point to check
        :return: True or False
        """
        if euclidean_norm((self.center[0] - point[0], self.center[1] - point[1])) <= self.radius:
            return True
        else:
            return False


class House:
    def __init__(self, center: Tuple[float, float], size: int):
        """
        Initializes the House class
        :param center: center of the house
        :param size: size of the house (square form)
        """
        self.center = center
        self.size = size


class Deer:
    def __init__(self, index: int, position: Tuple[float, float]):
        """
        Initializes the Deer class
        :param index: index of the deer
        :param position: initial position of the deer
        """
        self.index = index
        self.position = position
        self.old_position = position # old position for checking marker intersection
        self.resource: Resource = None  # loaded resource
        self.loaded: int = 0  # amount of loaded resources
        self.inactive = False  # deer rests after depositing resources
        self.marker = None

    def __repr__(self):
        state = "Return to home" if self.resource else "Searching"
        state = "Inactive" if self.inactive else state
        return f"#{self.index} | {state} | current position {self.position} | loaded {self.loaded}"

    def move(self, dx: int, prec: int, house: House, N: int, markers: list):
        """
        Moves the deer either pseudo-randomly or home to Santa
        :param dx: speed of the deer
        :param prec: precision of the angle that the deer turns
        :param house: Santa's house (in order to return and deposit)
        :param N: size of the world
        :param markers: list of all set markers
        """
        self.old_position = self.position
        if self.inactive:  # deer rests after depositing materials
            self.inactive = False
            return

        if self.resource:  # return to home mechanism
            self.return_to_home(dx, house)
        else:  # deer doesn't have a resource
            if self.marker and self.marker.location.amount > 0:  # deer currently follows a marker with non-depleted
                # location
                self.follow_marker(dx, self.marker)
                return
            else:
                if self.marker is not None:  # marker cleanup
                    markers.remove(self.marker)
                self.marker = None

                for marker in markers:  # checks if the deer recently passed any marker
                    if marker.line_touch(self.old_position, self.position):
                        self.marker = marker
                        break
                if self.marker:  # if yes, follow that marker
                    self.follow_marker(self.marker)
                else:  # if not, move around pseudo-randomly
                    theta: float = round(random.uniform(0, 360), prec)  # pseudo-random angle
                    self.position = (min(max(0.0, self.position[0] + dx * cos(theta)), N),
                                     min(max(0.0, self.position[1] + dx * sin(theta)), N)
                                     )

    def return_to_home(self, dx: int, house: House):
        """
        Moves the deer home to Santa along a straight line
        :param dx: speed of the deer
        :param house: Santa's house
        """
        home = house.center
        max_distance = max(self.position[0] - home[0], self.position[1] - home[1])  # Santa's house has a square form
        if max_distance <= house.size:  # deer reached Santa's house
            self.resource.deposit(self.loaded)
            self.loaded = 0
            self.resource = None
            self.inactive = True
            return

        self.follow_marker(dx, home)

    def follow_marker(self, dx: int, marker: Tuple[float, float]):  # makes the deer follow a marker
        """
        Moves the deer into the direction of a marker
        :param dx: speed of the deer
        :param marker: position of the marker
        """
        euclidean_distance = euclidean_norm((self.position[0] - marker[0], self.position[1] - marker[1]))
        direction = (marker[0] - self.position[0], marker[1] - self.position[1])
        direction = (min(dx, euclidean_distance) * direction[0] / euclidean_norm(direction),
                     min(dx, euclidean_distance) * direction[1] / euclidean_norm(direction))
        self.position = (self.position[0] + direction[0], self.position[1] + direction[1])


class Marker:
    def __init__(self, location: Location, startpoint: Tuple[float, float]):
        """
        Initializes the Marker class
        :param location: resource location associated to the marker
        :param startpoint: position to which the deer has drawn the marker
        """
        self.location = location
        self.startpoint = startpoint

    def __repr__(self):
        return f"Marker starting at {self.startpoint} associated with {self.location}"

    def line_touch(self, old_pos: Tuple[float, float], new_pos: Tuple[float, float]) -> bool:
        """
        Checks if a deer traversed this marker while going from old_pos to new_pos
        :param old_pos: Old position of the deer
        :param new_pos: New position of the deer
        :return: True if the segments (old_pos -> new_pos) and (startpoint -> location.center) intersect, else False
        """
        def counter_clockwise_orientation(A: Tuple[float, float], B: Tuple[float, float], C: Tuple[float, float]) -> bool:
            """
            Checks if th three points A, B and C are oriented in a counterclockwise fashion in the plane,
            i.e. if the slope of the line AC is more than the slope of the line AB.
            :param A: first point
            :param B: second point
            :param C: third point
            :return: True or False
            """
            slope_AB = (B[1] - A[1]) / (B[0] - A[0])
            slope_AC = (C[1] - A[1]) / (C[0] - A[0])
            return slope_AC > slope_AB

        def intersect(A: Tuple[float, float], B: Tuple[float, float], C: Tuple[float, float], D: Tuple[float, float]) -> bool:
            """
            Checks if the segments (A -> B) and (C -> D) intersect
            :return: True in case of intersection else False
            """
            return (counter_clockwise_orientation(A, C, D) != counter_clockwise_orientation(B, C, D)
                    and counter_clockwise_orientation(A, B, C) != counter_clockwise_orientation(A, B, D)
                    )

        try:
            return intersect(old_pos, new_pos, self.startpoint, self.location.center)
        except ZeroDivisionError:
            mainlog.info("Zero Division in intersection check")
            try:
                return intersect((old_pos[0] - 0.1, old_pos[1] - 0.1), (new_pos[0] - 0.1, new_pos[1] - 0.1),
                                 self.startpoint, self.location.center)
            except ZeroDivisionError as e:
                mainlog.warn(f"Unexpected second Zero Division in intersection check: {e}")
                return False

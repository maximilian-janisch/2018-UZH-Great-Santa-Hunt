"""
The deer class.
Authors: Maximilian Janisch, Robert Scherrer, Reetta Välimäki
IMPORTANT: I assume that a positive change in the x coordinate of a tuple (i. e. tuple[0]) is a movement to the RIGHT
           and that a positive change in the y coordinate of a tuple (i. e. tuple[1]) is a movement to the TOP
"""

__all__ = ("Deer", )

from math import *
import random
from typing import *  # library for type hints

from functions import *
from classes import *
from classes2 import *
from logs import *



class Deer:
    def __init__(self, index: int, position: Tuple[float, float]):
        """
        Initializes the Deer class
        :param index: index of the deer
        :param position: initial position of the deer
        """
        self.index = index
        self.position = position
        self.old_position = position  # old position for checking marker intersection
        self.resource: Resource = None  # loaded resource
        self.loaded: int = 0  # amount of loaded resources
        self.inactive = False  # deer rests after depositing resources
        self.marker = None
        self.is_painting_marker = False
        self.is_erasing_marker = False

    def __repr__(self):
        state = "Random search"
        if self.resource:
            if self.is_painting_marker:
                state = "Painting marker"
            elif self.is_erasing_marker:
                state = "Erasing marker"
            else:
                state = "Return to home"
        elif self.marker:
            state = "Follow marker"
        elif self.inactive:
            state = "Inactive"
        return f"#{self.index} | {state} | current position {self.position} | loaded {self.loaded}"

    def move_towards(self, dx: int, destination: Tuple[float, float]):
        """
        Moves the deer into the direction of a destination point by linear interpolation
        :param dx: speed of the deer
        :param destination: position to move towards
        """
        euclidean_distance = euclidean_norm((self.position[0] - destination[0], self.position[1] - destination[1]))
        direction = (destination[0] - self.position[0], destination[1] - self.position[1])

        if euclidean_norm(direction) == 0:  # avoid division by 0 error (if self is already at location)
            return
        direction = (min(dx, euclidean_distance) * direction[0] / euclidean_norm(direction),
                     min(dx, euclidean_distance) * direction[1] / euclidean_norm(direction))
        self.position = (self.position[0] + direction[0], self.position[1] + direction[1])

    def random_walk(self, dx: int, N: int):  # makes the deer move pseudo-randomly
        """
        Moves the deer around pseudo-randomly
        :param dx: speed of the deer
        :param N: edge of the world
        """
        theta: float = random.uniform(0, 360)  # pseudo-random angle
        self.position = (min(max(0.0, self.position[0] + dx * cos(theta)), N),
                         min(max(0.0, self.position[1] + dx * sin(theta)), N)
                         )

    def move(self, dx: int, house: House, N: int, markers: list):
        """
        Moves the deer according to the environment (markers, inactivity, etc.)
        :param dx: speed of the deer
        :param house: Santa's house (in order to return and deposit)
        :param N: size of the world
        :param markers: list of all set markers
        """
        self.old_position = self.position
        if self.inactive:  # deer rests after depositing materials
            self.inactive = False

            # find and attach marker
            if not self.marker:  # deer might want to stick to his current marker
                # avoid markers that have not reached santa's house
                valid_markers = [marker for marker in markers if marker.startpoint == house.center]
                if valid_markers:
                    # if there is at least one marker, pick it
                    self.marker = random.choice(valid_markers)

        elif self.resource:  # return to home mechanism
            self.return_to_home(dx, house)
        elif self.marker:  # deer doesn't have a resource but follows a marker
            self.follow_marker(dx, N)
        else:  # deer has neither a resource nor a marker
            for marker in markers:  # checks if the deer recently passed any marker
                if marker.line_touch(self.old_position, self.position):
                    self.marker = marker
                    break
            if self.marker:  # if yes, follow that marker
                self.follow_marker(dx, N)
            else:  # if not, move around pseudo-randomly
                self.random_walk(dx, N)

    def load_resource(self, location: Location, amount: int):
        """
        loads amount of resource from location
        :param location: the location with the loot
        :param amount: how many
        """
        self.resource = location.resource
        self.loaded = location.pickup_resources(amount)
        self.position = location.center  # a hack, but this way, the marker is connected to the center of the location and will not disconnect when the location shrinks
        mainlog.debug(f"picking up {self.loaded} from {location.resource}")
        if self.marker and (location.amount == 0):  # we just emptied the location
            self.is_erasing_marker = True
            mainlog.debug(f"deer #{self.index} erases {self.marker}")

    def return_to_home(self, dx: int, house: House):
        """
        Moves the deer home to Santa along a straight line
        :param dx: speed of the deer
        :param house: Santa's house
        """
        home = house.center
        if house.point_in_square(self.position):  # deer reached Santa's house
            self.resource.deposit(self.loaded)
            self.loaded = 0
            self.resource = None
            self.inactive = True

            # finalize marker and disconnect from it
            if self.is_painting_marker:
                self.marker.startpoint = home
                self.is_painting_marker = False
                mainlog.debug(f"Deer #{self.index} finalized {self.marker}")
                self.marker = None

            # finalize marker and disconnect from it
            if self.is_erasing_marker:
                mainlog.debug(f"deer #{self.index} removed {self.marker}")
                self.marker.disable()
                self.is_erasing_marker = False
                self.marker = None

        else:
            self.move_towards(dx, home)

            # paint the marker
            if self.is_painting_marker:
                self.marker.startpoint = self.position

            # erase the marker
            if self.is_erasing_marker:
                self.marker.endpoint = self.position

    def follow_marker(self, dx: int, N: int):  # makes the deer follow a marker
        """
        Moves the deer into the direction of a marker
        :param dx: speed of the deer
        :param N: Edge of the world
        """
        # check whether we overshoot the marker first (could have been erased in the meantime)
        planned_direction = (self.marker.endpoint[0] - self.position[0], self.marker.endpoint[1] - self.position[1])
        if (planned_direction[0] * self.marker.direction[0] >= 0) and (
                planned_direction[1] * self.marker.direction[1] >= 0):
            # endpoint of marker is still in front of us, go ahead
            self.move_towards(dx, self.marker.endpoint)
        else:
            # the marker's endpoint does not lie in our direction anymore
            self.marker = None
            self.random_walk(dx, N)

    def start_marker(self, location: Location, origin: Tuple[float, float]) -> Marker:
        """
        Creates a new marker to start painting on the way home.
        :param location: the location to which the marker has to lead
        :param origin: the point the marker will origin from when completed
        :return: the newly created marker
        """
        self.is_painting_marker = True
        self.marker = Marker(location, (location.center[0] - origin[0], location.center[1] - origin[1]))
        mainlog.debug(f"deer #{self.index} paints {self.marker}")
        return self.marker

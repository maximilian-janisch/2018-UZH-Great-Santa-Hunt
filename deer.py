"""
The deer class.
Authors: Maximilian Janisch, Robert Scherrer, Reetta Välimäki
IMPORTANT: I assume that a positive change in the x coordinate of a tuple (i. e. tuple[0]) is a movement to the RIGHT
           and that a positive change in the y coordinate of a tuple (i. e. tuple[1]) is a movement to the TOP
"""

__all__ = ("Deer",)

from math import *
import random
from typing import *  # library for type hints

from functions import *
from classes import *
from classes2 import *
from logs import *


class Deer:
    def __init__(self, index: int, position: Tuple[float, float], smoothness: int):
        """
        Initializes the Deer class
        :param index: index of the deer
        :param position: initial position of the deer
        :param smoothness: Integer according to the smoothness of the animation
        """
        self.index = index

        self.position = position
        self.old_position = position  # old position for checking marker intersection

        self.resource: Resource = None  # loaded resource
        self.loaded: int = 0  # amount of loaded resources
        self.inactive = 0  # deer rests after depositing resources
        self.marker = None

        self.is_painting_marker = False
        self.is_erasing_marker = False
        self.is_distributing = False
        self.path = None  # used for distribution

        self.random_target = None
        self.smoothness = smoothness
        # Note that the deer needs to know the smoothness factor in random_walk
        # in order to counteract the normalization effect of moving randomly often
        # i. e. it will change its random target less often on purpose in order
        # to get further away from Santa's house

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
        elif self.is_distributing:
            if self.path:
                state = "Distributing toy"
            else:
                state = "Return to home"
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
        if self.random_target and not euclidean_norm((self.position[0] - self.random_target[0],
                                                      self.position[1] - self.random_target[1])) <= 0.001:
            self.move_towards(dx, self.random_target)
        else:
            self.random_target = (limit(self.position[0] + dx * cos(theta) * self.smoothness, 0, N),
                                  limit(self.position[1] + dx * sin(theta) * self.smoothness, 0, N)
                                  )

    def move_to_collect(self, dx: int, santa_house: House, N: int, markers: list):
        """
        Moves the deer according to the environment (markers, inactivity, etc.)
        :param dx: speed of the deer
        :param santa_house: Santa's house (in order to return and deposit)
        :param N: size of the world
        :param markers: list of all set markers
        """
        self.old_position = self.position

        if self.inactive:  # deer rests after depositing materials
            # find and attach marker
            self.inactive = (self.inactive + 1) % self.smoothness
            if not self.marker:  # deer might want to stick to his current marker
                # avoid markers that have not reached santa's house
                valid_markers = [marker for marker in markers if marker.startpoint == santa_house.center]
                if valid_markers:
                    # if there is at least one marker, pick it
                    self.marker = random.choice(valid_markers)

        elif self.resource:  # return to home mechanism
            self.return_to_home(dx, santa_house)
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

    def move_to_distribute(self, dx: int, santa_house: House, paths: list):
        """
        Moves the deer according to the environment (markers, inactivity, etc.)
        :param dx: speed of the deer
        :param santa_house: Santa's house (in order to return and deposit)
        :param paths: list of all distribution paths
        """
        # cleanup for collecting deers
        if not self.is_distributing:
            self.is_distributing = True
            self.is_painting_marker = False
            self.is_erasing_marker = False
            if self.marker:
                self.marker.disable()
                self.marker = None

        self.old_position = self.position
        if self.inactive:  # deer rests after returning home
            # find and attach path
            # avoid paths that are already picked
            valid_paths = [path for path in paths if not (path.is_picked() or path.is_finished())]
            if valid_paths:
                # if there is at least one marker, pick it
                self.path = random.choice(valid_paths)
                self.path.pick()
                self.inactive = False
            # else stay inactive in santa's house to rest

        # still in collection mode, go home and finish job
        elif self.resource:
            self.return_to_home(dx, santa_house)

        # deer on the move in distribution mode
        elif self.path:  # if yes, follow that path
            if not self.path.is_finished():
                target_house = self.path.get_next_house()
                self.move_towards(dx, target_house.center)
                if target_house.point_in_square(self.position):
                    mainlog.debug(f"Deer #{self.index} gave toy to {self.path.get_next_kid().name}")
                    self.path.get_next_kid().give_toy()
            else:
                self.path = None
                self.return_to_home(dx, santa_house)
        else:  # if not, move around pseudo-randomly
            self.return_to_home(dx, santa_house)

    def load_resource(self, location: Location, amount: int, markers: List[Marker]):
        """
        loads amount of resource from location
        :param location: the location with the loot
        :param amount: how many
        """
        self.resource = location.resource
        self.loaded = location.pickup_resources(amount)
        self.position = location.center  # a hack, but this way, the marker is connected to the center of the location and will not disconnect when the location shrinks
        mainlog.debug(f"picking up {self.loaded} from {location.resource}")
        if (self.loaded > 0) and (location.amount == 0):  # we just emptied the location
            existing_marker = None
            for marker in markers:
                if not existing_marker:
                    if marker.location == location:
                        existing_marker = marker
            self.marker = existing_marker
            if self.marker:
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
            # unload resources
            if self.resource:
                self.resource.deposit(self.loaded)
                self.loaded = 0
                self.resource = None
            self.inactive = 1

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

    def loaded_toys(self) -> int:
        """
        returns the number of toys loaded
        """
        result = 0
        if self.path:
            result = self.path.left_to_distribute()
        return result

    def steps_to_destination(self, dx: int, destination: Tuple[float, float])-> int:
        """
        Estimates the steps needed to walk to destination
        :param dx: speed of the deer
        :param destination: position to move towards
        """
        euclidean_distance = euclidean_norm((self.position[0] - destination[0], self.position[1] - destination[1]))
        return ceil(euclidean_distance/dx)


"""
(Helper) classes that are used by other files in this project are specified here.
Authors: Maximilian Janisch, Robert Scherrer, Reetta Välimäki
IMPORTANT: I assume that a positive change in the x coordinate of a tuple (i. e. tuple[0]) is a movement to the RIGHT
           and that a positive change in the y coordinate of a tuple (i. e. tuple[1]) is a movement to the TOP
"""

__all__ = ("Circle", "Square", "Resource", "Location", "House", "Deer", "Marker")

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
        self.collected += amount
        mainlog.debug(f"depositing {amount} to {self}")


class Kid:
    def __init__(self, name: str):
        """Initialises the Kid class"""
        self.name = name

    def kid_grade(self):
        """Gives grades to the kids, 0=bad, 5=good"""
        self.kid_grade = (randint(0, 5))
        return kid_grade

    def kid_home(self):
        """Assigns a square to the kid"""

class Toy:
    def __init__(self, toy_name:str):
        self.resource_list = []
        self.toy_name = toy_name

    def toy_grade(self):
        """Gives grades to the toys, 0=bad, 5=good"""
        self.toy_grade = (randint(0, 5))
        return toy_grade

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

    def pickup_ressources(self, requested_amount: int) -> int:
        """
        Returns the number of ressources picked up and reduces radius accordingly
        :param requested_amount: what should be picked up
        :return: the effective amount, max the requested amount, but only as much as there is
        """
        result = min(requested_amount, self.amount)
        self.amount -= result
        self.radius = sqrt(self.amount / pi)  # todo: looses precision since floor(...) is used for the initial amount
        return result


class House(Square):
    def __init__(self, center: Tuple[float, float], size: float):
        """
        Initializes the House class
        :param center: center of the house
        :param size: size of the house (square form)
        """
        super().__init__(center, size)


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

    def line_touch(self, old_pos: Tuple[float, float], new_pos: Tuple[float, float]) -> bool:  # todo: test behaviour
        """
        Checks if a deer traversed this marker while going from old_pos to new_pos
        :param old_pos: Old position of the deer
        :param new_pos: New position of the deer
        :return: True if the segments (old_pos -> new_pos) and (startpoint -> location.center) intersect, else False
        """

        def counter_clockwise_orientation(A: Tuple[float, float], B: Tuple[float, float],
                                          C: Tuple[float, float]) -> bool:
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

        def intersect(A: Tuple[float, float], B: Tuple[float, float], C: Tuple[float, float],
                      D: Tuple[float, float]) -> bool:
            """
            Checks if the segments (A -> B) and (C -> D) intersect
            :return: True in case of intersection else False
            """
            return (counter_clockwise_orientation(A, C, D) != counter_clockwise_orientation(B, C, D)
                    and counter_clockwise_orientation(A, B, C) != counter_clockwise_orientation(A, B, D)
                    )

        try:
            return intersect(old_pos, new_pos, self.startpoint, self.endpoint)
        except ZeroDivisionError:
            mainlog.info("Zero Division in intersection check")
            try:
                return intersect((old_pos[0] - 0.1, old_pos[1] - 0.1), (new_pos[0] - 0.1, new_pos[1] - 0.1),
                                 self.startpoint, self.endpoint)
            except ZeroDivisionError as err:
                mainlog.warn(f"Unexpected second Zero Division in intersection check: {err}")
                return False

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
                state = "Retrun to home"
        elif self.marker:
            state = "Follow marker"
        elif self.inactive:
            state = "Inactive"
        return f"#{self.index} | {state} | current position {self.position} | loaded {self.loaded}"

    def move(self, dx: int, house: House, N: int, markers: list):
        """
        Moves the deer either pseudo-randomly or home to Santa or in the direction of a marker
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
                if len(valid_markers) > 0:
                    # if there is at least one marker, pick it
                    # fixme: should at least some deers prefer random walk even if there are markers available?
                    self.marker = valid_markers[random.randint(0, len(valid_markers) - 1)]
            return

        if self.resource:  # return to home mechanism fixme: this whole if-else-etc. block doesn't make sense
            self.return_to_home(dx, house)
        else:  # deer doesn't have a resource
            if self.marker:
                self.follow_marker(dx, N)
            else:
                # fixme: detect when marker is erased
                if self.marker is not None:  # marker cleanup
                    markers.remove(self.marker)  # fixme: Code block unreachable
                self.marker = None

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
        self.loaded = location.pickup_ressources(amount)
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
        """
        # check whether wie overshoot the marker first (could have been erased in dhe meantime)
        planned_direction = (self.marker.endpoint[0] - self.position[0], self.marker.endpoint[1] - self.position[1])
        if (planned_direction[0] * self.marker.direction[0] >= 0) and (
                planned_direction[1] * self.marker.direction[1] <= 0):
            self.move_towards = (
            dx, self.marker.endpoint)  # fixme (FATAL): move_towards shadows function move_towards()
        else:
            # the marker's endpoint does not lie in our direction anymore
            self.marker = None
            self.random_walk(dx, N)

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

    def move_towards(self, dx: int, destination: Tuple[float, float]):  # makes the deer move towards destination
        """
        Moves the deer into the direction of a destination point
        :param dx: speed of the deer
        :param destination: position to move towards
        """
        euclidean_distance = euclidean_norm((self.position[0] - destination[0], self.position[1] - destination[1]))

        direction = (destination[0] - self.position[0], destination[1] - self.position[1])
        direction = (min(dx, euclidean_distance) * direction[0] / euclidean_norm(direction),
                     min(dx, euclidean_distance) * direction[1] / euclidean_norm(direction))
        self.position = (self.position[0] + direction[0], self.position[1] + direction[1])

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

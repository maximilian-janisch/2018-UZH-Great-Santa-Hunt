"""
Statistics module.
Authors: Robert Scherrer, 
Collects data and writes output to a file
"""

__all__ = ("Statistics",)

import csv
import time
from typing import *

from geometry import *
from deer import *
from helper_functions import *
from global_variables import *


class Tracker:
    """
    Abstract base class for stat-collecting classes
    """
    def __init__(self, tracked: Any):
        self.tracked = tracked
        self.stats = []
        self.update(0)

    def update(self, _time: int) -> None:
        """
        Collects next stat for stats list
        :param _time: Time (in seconds) of status of tracked object
        """
        self.stats.append((_time,) + self.get_stats(_time))

    def get_stats(self, _time) -> tuple:
        """
        Returns stats about tracked object at _time
        :param _time: Time in seconds
        :return: Tuple containing stats about the tracked object at _time
        """
        return (self.tracked.position,)


class DeerStats(Tracker):
    """
    Collects statistics about deers
    """
    def __init__(self, deer: Deer):
        """
        Initializes class instances
        :param deer: the deer we collect data from
        """
        super().__init__(deer)


class LocationStats(Tracker):
    """
    collects statistics about locations
    """
    def __init__(self, location: Location):
        """
        Initializes class instances
        :param location: the location we collect data from
        """
        super().__init__(location)
        self.initial_radius = self.tracked.radius

    def get_stats(self, _time: int) -> tuple:
        """
        Gets information about location at _time
        :param _time: Time (in seconds) of the Location's status
        :return: Tuple with information about the location
        """
        return self.tracked.center, self.tracked.amount

    def time_to_find(self) -> int:
        """
        evaluates, in which time step the location was found
        """
        index_amount = 2
        index_time = 0
        result = -1
        orig_amount = self.stats[0][index_amount]
        for s in self.stats:
            if s[index_amount] < orig_amount:
                result = s[index_time]
                break
            
        return result


class Statistics:
    """
    Class to handle statistics for the ressource hunt
    """
    def __init__(self, my_world: World):
        """
        Initializes statistics class and opens output file.
        :param my_world: the world we collect data from
        """
        self.world = my_world
        self.deers = []
        self.locations = []
        self.time = 0

        # initialize output file        
        filename = time.strftime("%Y-%m-%d_%H-%M-%S_Hunt_Stats.csv")
        self.file = open(filename, mode="w")
        self.writer = csv.writer(self.file, delimiter=";", lineterminator="\n")

        self.writer.writerow(["Size of the World", self.world.N])
        self.writer.writerow(["Number of Deers", len(self.world.deers)])
        self.writer.writerows([[], ["Sants's House"]])
        self.writer.writerow(["Type", "x", "y", "Size"])
        self.writer.writerow(
            ["House", self.world.santa_house.center[0], self.world.santa_house.center[1], self.world.santa_house.size])
        self.writer.writerows([[], ["Locations"]])
        self.writer.writerow(["Type", "Ressource Index", "Ressource Name", "x", "y", "Radius", "Initial Amount"])
        for l in self.world.locations:
            self.locations.append(LocationStats(l))
            self.writer.writerow(
                ["Location", l.resource.index, l.resource.name, l.center[0], l.center[1], l.radius, l.amount])
        for d in self.world.deers:
            self.deers.append(DeerStats(d))

    def close(self):
        """
        Closes output file
        """
        self.file.close()

    def update(self, _time: int) -> None:
        """
        collects current dynamic data from self.world
        param time: the time step after which the update is done
        """
        self.time = _time
        for each in self.locations:
            each.update(_time)
        for each in self.deers:
            each.update(_time)

    def analyze_collection(self) -> None:
        """
        place to invent good ideas and create output out of it
        """
        # how many ressources were collected
        self.writer.writerows([[], ["How many resources were collected?"]])
        self.writer.writerow(["Type", "Index", "Name", "Amount"])
        for r in self.world.resources:
            self.writer.writerow(
                ["Location", r.index, r.name, r.collected])

        # how long did it take
        self.writer.writerows([[], ["How long did the collection last?"]])
        self.writer.writerow(["max time", "effective time"])
        self.writer.writerow([self.world.T, round(self.time)])

        # how easy were the locations found
        self.writer.writerows([[], ["How were the locations discovered?"]])
        self.writer.writerow(["Distance", "Size", "Time"])
        for l in self.locations:
            size = l.initial_radius
            distance = euclidean_norm((l.tracked.center[0] - self.world.santa_house.center[0],
                                       l.tracked.center[1] - self.world.santa_house.center[1]))
            elapsed = l.time_to_find()
            self.writer.writerow([distance, size, elapsed])


# self test section
if __name__ == "__main__":
    pass

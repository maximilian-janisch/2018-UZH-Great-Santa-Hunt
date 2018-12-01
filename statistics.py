"""
Statistics module.
Authors: Robert Scherrer, 
Collects data and writes output to a file
"""

__all__ = ("Statistics")


import csv
import time
from typing import *
from global_variables import *
from functions import *
from classes import *



class DeerStats:
    """
    collects statistics about deers
    """
    def __init__ (self, deer: Deer):
        """
        Initializes class instances
        :param deer: the deer we collect data from
        """
        self.deer = deer
        self.stats = []
        self.update(0)
    
    def update (self, time: int) -> None:
        """
        adds next position to deer's history
        """
        self.stats.append((time, self.deer.position))
        

class LocationStats:
    """
    collects statistics about locations
    """
    def __init__ (self, location: Location):
        """
        Initializes class instances
        :param location: the location we collect data from
        """
        self.location = location
        self.initial_radius = location.radius
        self.stats = []
        self.update(0)
    
    def update (self, time: int) -> None:
        """
        adds next position to locations's history
        """
        self.stats.append((time, self.location.center, self.location.amount))

    def time_to_find (self) -> int:
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
    
    def __init__ (self, my_world: World):
        """
        Initializes statistics class and opens output file.
        :param my_world: the world we collect data from
        """
        self.world = my_world
        self.deers = []
        self.locations = []
        
        # initialize output file        
        filename = time.strftime("%Y-%m-%d_%H-%M-%S_Hunt_Stats.csv")
        self.file = open(filename, mode="w")
        self.writer = csv.writer(self.file, delimiter=";", lineterminator="\n")

        self.initial_state()

    def __del__(self):
        """
        Closes output file
        """
        self.file.close()

    def initial_state (self) -> None:
        """
        Initializes statistics class and opens output file.
        """
        self.writer.writerow(["Size of the World", self.world.N])
        self.writer.writerow(["Number of Deers", len(self.world.deers)])
        self.writer.writerows([[],["Sants's House"]])
        self.writer.writerow(["Type", "x", "y", "Size"])
        self.writer.writerow(["House", self.world.santa_house.center[0], self.world.santa_house.center[1], self.world.santa_house.size])
        self.writer.writerows([[],["Locations"]])
        self.writer.writerow(["Type", "Ressource Index", "Ressource Name", "x", "y", "Radius", "Initial Amount"])
        for l in self.world.locations:
            self.locations.append(LocationStats(l))
            self.writer.writerow(["Location", l.resource.index, l.resource.name, l.center[0], l.center[1], l.radius, l.amount])
        for d in self.world.deers:
            self.deers.append(DeerStats(d))

    def update (self, time: int) -> None:
        """
        collects current dynamic data from self.world
        param time: the time step after which the update is done
        """
        for each in self.locations:
            each.update(time)
        for each in self.deers:
            each.update(time)


    def analyze (self) -> None:
        """
        place to invent good ideas and create output out of it
        """
        #how easy were the locations found
        self.writer.writerows([[],["How were the locations discovered?"]])
        self.writer.writerow(["Distance", "Size", "Time"])
        for l in self.locations:
            size = l.initial_radius
            distance = euclidean_norm((l.location.center[0]-self.world.santa_house.center[0], l.location.center[1]-self.world.santa_house.center[1]))
            time = l.time_to_find()
            self.writer.writerow([distance, size, time])


#self test section
if __name__ == "__main__":
    pass

"""
File of the Santa Hunt project which determines the efficiency of the distribution process
Author: Maximilian Janisch
"""  # todo: Doesn't do anything at the moment

from global_variables import *
from logs import *


def one_distribution(world: World):
    """
    Performs one distribution based on data from world.
    :param world: Contains data such as collected Resources, Kids, etc.
    :return: Information about how many toys were distributed
    """
    mainlog.debug(f"Starting Distribution model with size {world.N} and time {world.T}")
    iter_ = 0
    while True:
        iter_ += world.animation_smoothness
        time_left = world.T_dist - iter_
        time_to_go_home = max(deer.steps_to_destination(world.dx, world.santa_house.center) for deer in world.deers)
        if time_left <= time_to_go_home:
            break
        else:
            # continue distribution
            for deer in world.deers:
                deer.move_to_distribute(world.dx, world.santa_house, world.distribution_paths)

            # finish early if the job is done
            if all(path.is_finished() for path in world.distribution_paths):
                # yeah, all paths were followed successfully
                if all(deer.inactive for deer in world.deers):
                    # the deers are resting
                    return


N_ranges = [0.5 * i for i in range(40, 401)]
T_dist_ranges = list(range(2, 100))

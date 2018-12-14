"""
(Helper) functions that are used by other files in this project are specified here.
Author: Maximilian Janisch
"""

__all__ = ("random_tuple", "euclidean_norm", "max_norm", "limit", "chunkIt")

import random

from typing import *  # library for type hints
from math import *


def random_tuple(_min: float, _max: float) -> Tuple[float, float]:
    """
    Generates a random 2-tuple
    :param _min: Minimal number
    :param _max: Maximal number
    :return: Pseudo-random tuple
    """
    return random.uniform(_min, _max), random.uniform(_min, _max)


def euclidean_norm(_tuple: Tuple[float, float]) -> float:
    """
    Returns the euclidean norm of the point _tuple in two-dimensional euclidean space
    """
    return sqrt(_tuple[0] ** 2 + _tuple[1] ** 2)


def polar_angle(a, b: Tuple[float, float]) -> float:
    """
    Returns the polar angle of the connection between two points (in radiant)
    """
    result = 0
    dx = b[0] - a[0]
    dy = b[1] - a[1]
    if dx == 0:
        if dy > 0:
            result = pi/2
        else:
            result = -pi/2
    else:
        result = math.atan(dy/dx)
        if dx < 0:
            if dy < 0:
                result -= math.pi
            else:
                result += math.pi
    return result


def max_norm(_tuple: Tuple[float, float]) -> float:
    """
    Returns the maximum norm of the point _tuple in two-dimensional euclidean space
    """
    return max(abs(_tuple[0]), abs(_tuple[1]))


def limit(number: float, _min: float, _max: float) -> float:
    """
    Takes a number as input and finds the closest number to it in the interval [_min, _max]
    :param number: Floating point number
    :return: closest number to the interval [_min, _max]
    """
    return min(_max, max(_min, number))

def chunkIt(seq: List, num, max_size: int)-> List[List]:
    """
    takes a list and returns a list with evenly chunked sizes
    :param seq: list
    :param num: number of slices
    :param max_size: maximum size of a slice
    :return: sliced list
    """
    avg = limit (len(seq) / float(num), 1, max_size)
    out = []
    last = 0.0

    while last < len(seq):
        out.append(seq[int(last):int(last + avg)])
        last += avg

    return out




# self test section
if __name__ == "__main__":
    # test chunkIt
    l = [1,2,3,4,5,6,7,8]
    ll = chunkIt (l, 5, 3)
    if len(ll) != 5:
        print ("chunkIt: error: number of chunks not fulfilled")
    ll = chunkIt (l, 12, 3)
    if len(ll) != len(l):
        print ("chunkIt: error: more than size of initial list")
    ll = chunkIt (l, 2, 3)
    if len(ll) != 3:
        print ("chunkIt: error: chunk size too big")


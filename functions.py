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

def chunkIt(seq, num):
    """
    takes a list and returns a list with evenly chunked sizes
    :param seq: list
    :param num: number of slices
    :return: sliced list
    """
    avg = len(seq) / float(num)
    out = []
    last = 0.0

    while last < len(seq):
        out.append(seq[int(last):int(last + avg)])
        last += avg

    return out
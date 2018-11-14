"""
(Helper) functions that are used by other files in this project are specified here.
Author: Maximilian Janisch
"""

__all__ = ("random_tuple", "euclid")

import random

from typing import Tuple, List  # library for type hints
from math import *


def random_tuple(prec: int, _min: float, _max: float) -> Tuple[float]:
    """
    Generates a random 2-tuple
    :param prec: Specifies the number of decimals after the comma
    :param _min: Minimal number
    :param _max: Maximal number
    :return: Pseudo-random tuple with prec decimals after the comma
    """
    return round(random.uniform(_min, _max), prec), round(random.uniform(_min, _max), prec)


def euclid(tuple: Tuple[float, float]):
    return sqrt(tuple[0] ** 2 + tuple[1] ** 2)
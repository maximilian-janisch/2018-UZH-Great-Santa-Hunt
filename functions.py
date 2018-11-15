"""
(Helper) functions that are used by other files in this project are specified here.
Author: Maximilian Janisch
"""

__all__ = ("random_tuple", "euclidean_norm")

import random

from typing import *  # library for type hints
from math import *


def random_tuple(prec: int, _min: float, _max: float) -> Tuple[float, float]:
    """
    Generates a random 2-tuple
    :param prec: Specifies the number of decimals after the comma
    :param _min: Minimal number
    :param _max: Maximal number
    :return: Pseudo-random tuple with prec decimals after the comma
    """
    return round(random.uniform(_min, _max), prec), round(random.uniform(_min, _max), prec)


def euclidean_norm(_tuple: Tuple[float, float]) -> float:
    return sqrt(_tuple[0] ** 2 + _tuple[1] ** 2)

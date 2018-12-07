"""
This file checks whether two line segments intersect, and if they do returns the intersection point by solving
a linear equation system.
This is an edited version of https://www.cs.hmc.edu/ACM/lectures/intersections.html
"""

__all__ = ("intersect_segments",)

import math
from typing import *

from functions import euclidean_norm


def intersect_segments(pt1: Tuple[float, float], pt2: Tuple[float, float], ptA: Tuple[float, float],
                   ptB: Tuple[float, float]):
    """
    Returns the intersection of Segment from pt1 to pt2 and Segment from ptA to ptB
    :param pt1: Starting point of the first segment
    :param pt2: End point of the first segment
    :param ptA: Starting point of the second segment
    :param ptB: End point of the second segment
    :return: Tuple: (xi, yi, valid, r, s), where
                    - (xi, yi) is the intersection point
                    - r is the number such that (xi, yi) = pt1 + r*(pt2-pt1)
                    - s is the number such that (xi, yi) = pt1 + s*(ptB-ptA)

                    valid is False if there are no or infinitely many intersections points, or if the intersection point
                      lies on the two lines induced by the segments, but not on the segments themself;
                    valid is True otherwise
    """
    det_tolerance = 0.00000001

    # the first line is pt1 + r*(pt2-pt1)
    # in component form:
    x1, y1 = pt1
    x2, y2 = pt2
    dx1 = x2 - x1
    dy1 = y2 - y1

    # the second line is ptA + s*(ptB-ptA)
    x, y = ptA
    xB, yB = ptB
    dx = xB - x
    dy = yB - y

    # we need to find the (typically unique) values of r and s
    # that will satisfy
    #
    # (x1, y1) + r(dx1, dy1) = (x, y) + s(dx, dy)
    #
    # which is the same as
    #
    #    [ dx1  -dx ][ r ] = [ x-x1 ]
    #    [ dy1  -dy ][ s ] = [ y-y1 ]
    #
    # whose solution is
    #
    #    [ r ] = _1_  [  -dy   dx ] [ x-x1 ]
    #    [ s ] = DET  [ -dy1  dx1 ] [ y-y1 ]
    #
    # where DET = (-dx1 * dy + dy1 * dx)
    #
    # if DET is too small, they're parallel
    #
    DET = (-dx1 * dy + dy1 * dx)

    if math.fabs(DET) < det_tolerance:
        return 0, 0, False, 0, 0

    # the line segments are not parallel:
    DETinv = 1.0 / DET

    # find the scalar amount along the "self" segment
    r = DETinv * (-dy * (x - x1) + dx * (y - y1))

    # find the scalar amount along the input line
    s = DETinv * (-dy1 * (x - x1) + dx1 * (y - y1))

    # return the average of the two descriptions
    xi = (x1 + r * dx1 + x + s * dx) / 2.0
    yi = (y1 + r * dy1 + y + s * dy) / 2.0

    # now that we have the intersection point, we have to check if it lies on both segments, or if it just lies on the
    #   induced lines
    intersection_on_both_segments = euclidean_norm((x1 - xi, y1 - yi)) <= euclidean_norm((dx1, dy1)) \
                                      and euclidean_norm((x - xi, y - yi)) <= euclidean_norm((dx, dy))
    return xi, yi, intersection_on_both_segments, r, s

"""
The distribution
Author: Reetta Välimäki
"""

__all__ = ("Clusters")

import random

from typing import *  # library for type hints
from math import *
from sklearn.cluster import KMeans
import numpy as np
from time import *

from global_variables import *



class Cluster:
    def __init__(self, k: D):
        k = k
        """sets the houses into D number of clusters"""
        kmeans = KMeans(n_clusters=k)
        kmeans.fit(X)
        self.y_kmeans = kmeans.predict(X)  # the clusters





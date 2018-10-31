import numpy as np

from graph import random_connected_graph
from abc import ABC


class Optimizer(ABC):
    def __init__(self, problem):
        self.__problem = problem
        
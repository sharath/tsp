import numpy as np

from graph import random_connected_graph
from abc import ABC


class Optimizer(ABC):
    def __init__(self, problem, start):
        self.__problem = problem
        self.__state = start
        
    def check(self, state) -> int:
        pass
    
    def step(self) -> None:
        pass
        

class SimulatedAnnealing(Optimizer):
    def __init__(self, problem, start):
        self.super(problem, start)
        
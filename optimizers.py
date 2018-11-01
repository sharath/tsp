import numpy as np
import dill
from scipy.special import factorial
from graph import random_connected_graph, UndirectedWeightedGraph
from typing import List
from abc import ABC


class ClosedPath:
    def __init__(self, seq : List, problem : UndirectedWeightedGraph) -> None:
        assert seq is not None
        assert isinstance(seq, list)
        assert seq[0] == seq[-1]
        
        self.__seq = seq
        self.__prob = problem
        self.__cost = 0
        for i in range(1, len(seq)):
            a = seq[i-1]
            b = seq[i]
            self.__cost += problem.weight(a, b)
        
    @property
    def sequence(self) -> List:
        return self.__seq
    
    @property
    def length(self) -> int:
        return int(self.__cost)
    
    def __str__(self) -> str:
        return ' -> '.join(self.__seq)

    def __repr__(self) -> str:
        return ' -> '.join(self.__seq)

    
class BruteForceOptimizer:
    def __init__(self, problem):
        self.__problem = problem
        self.__solution = None
        self.__history = {}
        
    def __record(self) -> None:
        if '__solution' not in self.__history:
            self.__history['__solution'] = []
        self.__history['__solution'].append(self.__solution)
        
    @property
    def recording(self) -> List:
        return self.__history['__solution']
        
    def solve(self) -> ClosedPath:
        self.__solution = None
        self.__history = {}
        
        paths = {}
        while len(paths) < factorial(len(self.__problem.vertices)):
            path = rand_path(self.__problem)
            paths[str(path)] = path
    
        self.__solution = None
        val = np.inf
        for p in paths:
            if paths[p].length < val:
                self.__solution = paths[p]
                val = paths[p].length
            self.__record()
        return self.__solution


class NearestPathOptimizer:
    def __init__(self, problem):
        self.__problem = problem
        self.__soltuion = None
        self.__history = {}

    def __record(self) -> None:
        if '__solution' not in self.__history:
            self.__history['__solution'] = []
        self.__history['__solution'].append(self.__solution)
        
    @property
    def recording(self) -> List:
        return self.__history['__solution']
    
    def solve(self) -> ClosedPath:
        start = np.random.choice(self.__problem.vertices)
        frontier = [start]
        visited = []
        
        while len(frontier) > 0:
            cur = frontier.pop()
            visited.append(cur)
            if len(visited)> 1:
                t = list(visited)
                t.append(start)
                self.__solution = ClosedPath(t, self.__problem)
                self.__record()
            for n, d in sorted(self.__problem.neighbors(cur)):
                if n not in visited and n not in frontier:
                    frontier.append(n)
        visited.append(start)
        self.__solution = ClosedPath(visited, self.__problem)
        return self.__solution
        
        
class SimulatedAnnealingOptimizer:
    def __init__(self, problem):
        self.__problem = problem
        self.__soltuion = None
        self.__history = {}

    def __record(self) -> None:
        if '__solution' not in self.__history:
            self.__history['__solution'] = []
        self.__history['__solution'].append(self.__solution)
        
    @property
    def recording(self) -> List:
        return self.__history['__solution']
    
    def solve(self) -> ClosedPath:
        start = rand_path(self.__problem)
        
        
        
        
        
        return self.__solution
        
        
# performs dfs on all vertices and adds the final edge to the start vertex and returns a path object
def rand_path(problem : UndirectedWeightedGraph) -> ClosedPath:
    assert isinstance(problem, UndirectedWeightedGraph)
    
    start = np.random.choice(problem.vertices)
    frontier = [start]
    visited = []
    
    while len(frontier) > 0:
        cur = frontier.pop()
        visited.append(cur)
        for n, d in np.random.permutation(problem.neighbors(cur)):
            if n not in visited and n not in frontier:
                frontier.append(n)
                
    visited.append(start)
    return ClosedPath(visited, problem)

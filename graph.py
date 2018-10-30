import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import dill
from constants import *


class Vertex:
    def __init__(self, name : str, x : int = None, y: int = None) -> None:
        self._name = name
        if x is None or y is None:
            x = np.random.randint(d)
            y = np.random.randint(d)
        self._x = x
        self._y = y
        
        
    @property
    def name(self) -> str:
        return self._name
    
    
    @property
    def x(self) -> int:
        return self._x
    
    
    @property
    def y(self) -> int:
        return self._y
    
    
class WeightedEdge:
    def __init__(self, a : Vertex, b: Vertex, w: float = 1) -> None:
        assert isinstance(a, Vertex)
        assert isinstance(b, Vertex)
        self._a = a
        self._b = b
        self._w = w
        
        
    @property
    def a(self) -> Vertex:
        return self._a
    
    
    @property
    def b(self) -> Vertex:
        return self._b
    
    
    @property
    def w(self) -> float:
        return self._w
    

class UndirectedWeightedGraph:
    def __init__(self) -> None:
        self._G = {}
    
    
    def add_vertex(self, vertex : Vertex) -> None:
        assert isinstance(vertex, Vertex)
        assert vertex not in self._G
        
        self._G[vertex] = []
        
        
    def add_edge(self, a : Vertex, b : Vertex, w : float = 1) -> None:
        assert isinstance(a, Vertex)
        assert isinstance(b, Vertex)
        
        assert a in self._G
        assert b in self._G
        
        assert b not in self._G[a]
        assert a not in self._G[b]
        
        self._G[a].append(b)
        self._G[b].append(a)
        
        
    def neighbors(self, vertex : Vertex) -> list:
        assert vertex in self._G
        return list(self._G[vertex])
    
    
    def vertex_with_name(self, name) -> Vertex:
        for i in range(self._G):
            if i.name == name:
                return i
        raise ValueError
        
        
    def save(self, filename : str) -> None:
        with open(filename, 'wb') as fd:
            dill.dump(self, fd)
            
            
def load_graph(filename : str) -> None:
    with open(filename, 'rb') as fd:
        g = dill.load(fd)
    return g
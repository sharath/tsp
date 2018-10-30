import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import dill
from typing import List


class UndirectedWeightedGraph:
    def __init__(self) -> None:
        self.__G = {}
        
    def add_vertex(self, a : str) -> None:
        assert a not in self.__G
        self.__G[a] = []
        
    def add_edge(self, a : str, b : str, w : float = 1) -> None:
        assert a in self.__G and b in self.__G
        assert isinstance(a, str) and isinstance(b, str)
        
        edge1 = (b, w)
        edge2 = (a, w)
        
        assert edge1 not in self.__G[a]
        assert edge2 not in self.__G[b]
        
        self.__G[a].append(edge1)
        self.__G[b].append(edge2)
        
    def get_neighbors(self, a : str) -> List:
        assert a in self.__G
        return self.__G[a]
    
    def save(self, filename : str) -> None:
        assert isinstance(filename, str)
        with open(filename, 'wb') as fd:
            dill.dump(self, fd)
            
    @property
    def adjacency(self) -> List:
        return self.__G
            
def load_graph(filename : str) -> UndirectedWeightedGraph:
    assert isinstance(filename, str)
    with open(filename, 'rb') as fd:
        g = dill.load(fd)
    return g

def random_weight_connected_graph(k : int = 5, wlow : int = 1, whigh : int = 3) -> UndirectedWeightedGraph:
    if k >= len(ascii_uppercase):
        raise NotImplementedError
        
    g = UndirectedWeightedGraph()
    
    for i in range(k):
        g.add_vertex(ascii_uppercase[i])
        
    for i in range(k):
        for j in range(k):
            if i < j:
                g.add_edge(ascii_uppercase[i], ascii_uppercase[j], np.random.randint(wlow, whigh))
    return g
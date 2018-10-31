import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import dill

from matplotlib.patches import Circle, ConnectionPatch
from string import ascii_uppercase
from typing import List, Tuple
from utils import euclidean_distance
from constants import *

class Vertex:
    def __init__(self, name : str, x : int = None, y : int = None, color : Tuple = None) -> None:
        self._name = name
        
        if not x or not y:
            x, y = np.random.randint(d), np.random.randint(d)
        self._x, self._y =  x, y
        
        if not color:
            color = (np.random.uniform(0.1, 1),
                     np.random.uniform(0.1, 1),
                     np.random.uniform(0.1, 1), 0.8)
        self._color = color
        
    @property
    def name(self) -> str:
        return self._name
       
    @property
    def loc(self) -> Tuple:
        return (self._x, self._y)

    @property
    def color(self) -> Tuple:
        return self._color
    
    
class UndirectedWeightedGraph:
    def __init__(self) -> None:
        self.__G = {} # adjacency list of weights
        self.__loc = {}
        self.__vertices = {} # actual vertex objects
        
    def add_vertex(self, a : str, x : int = None, y : int =None, color : Tuple = None) -> None:
        assert a not in self.__G
        self.__G[a] = []
        self.__vertices[a] = Vertex(a, x=x, y=y, color=color)
        
    def add_edge(self, a : str, b : str, w : float = None) -> None:
        assert a in self.__G and b in self.__G
        assert isinstance(a, str) and isinstance(b, str)
        
        if not w:
            w = euclidean_distance(self.get_loc(a), self.get_loc(b))
        
        edge1 = (b, w)
        edge2 = (a, w)
        
        assert edge1 not in self.__G[a]
        assert edge2 not in self.__G[b]
        
        self.__G[a].append(edge1)
        self.__G[b].append(edge2)
        
    def get_neighbors(self, a : str) -> List:
        assert a in self.__G
        return self.__G[a]
        
    def get_col(self, name : str) -> Tuple:
        return self.__vertices[name].color
    
    def get_loc(self, name : str) -> Tuple:
        return self.__vertices[name].loc
    
    def save_viz(self, filename : str, figsize : Tuple = (10, 10), dpi : int = 50, vradius : float = 2.3, edge_col : Tuple = (0, 0, 0)) -> None:
        fig, ax = plt.subplots(figsize=(10, 10))
        ax.axis('equal')
        ax.set_xlim((int(-0.25*d), int(1.25*d)))
        ax.set_ylim((int(-0.25*d), int(1.25*d)))
        ax.set_xticks([]), ax.set_yticks([])
        for v1 in self.adjacency:
            for v2 in self.adjacency:
                ax.add_artist(ConnectionPatch(self.get_loc(v1), self.get_loc(v2), 'data'))
        for vname in self.adjacency:
            viz = Circle(self.get_loc(vname), vradius)
            viz.set_edgecolor(edge_col)
            viz.set_facecolor(self.get_col(vname))
            ax.add_artist(viz)
        fig.savefig(filename, dpi=dpi)
        plt.close()

    
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

def random_connected_graph(k=5) -> UndirectedWeightedGraph:
    if k >= len(ascii_uppercase):
        raise NotImplementedError
    
    np.random.seed(rseed)
    g = UndirectedWeightedGraph()
    
    for i in range(k):
        g.add_vertex(ascii_uppercase[i])
        
    for i in range(k):
        for j in range(k):
            if i < j:
                g.add_edge(ascii_uppercase[i], ascii_uppercase[j])
    return g
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import dill

from matplotlib.patches import Circle, ConnectionPatch
from typing import List, Tuple, Dict
from utils import euclidean_distance
from constants import *

class Vertex:
    def __init__(self, name : str, x : int = None, y : int = None, color : Tuple = None) -> None:
        self._name = name
        
        if not x or not y:
            x, y = np.random.randint(d), np.random.randint(d)
        self._x, self._y =  x, y
        
        if not color:
            color = (np.random.uniform(0.5, 1),
                     np.random.uniform(0.1, 1),
                     np.random.uniform(0.5, 1), 1)
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
        self.__G = {}        # adjacency list of weights
        self.__vertices = {} # actual vertex objects
        
    def add_vertex(self, a : str, x : int = None, y : int = None, color : Tuple = None) -> None:
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
        
    @property
    def vertices(self) -> np.array:
        return np.array([i for i in self.__G])
        
    def neighbors(self, a : str) -> np.array:
        assert a in self.__G
        return self.__G[a]
        
    def weight(self, a : str, b: str) -> np.array:
        assert a in self.__G
        for p in self.__G[a]:
            if p[0] == b:
                return p[1]
        raise ValueError
    
    def get_col(self, name : str) -> Tuple:
        return self.__vertices[name].color
    
    def get_loc(self, name : str) -> Tuple:
        return self.__vertices[name].loc
    
    def show(self, filename : str = None,
             figsize : Tuple = (10, 10),
             dpi : int = 50,
             vradius : float = 2.3,
             edge_col : Tuple = (0, 0, 0, 0.6),
             fsize=12, fcol='black', vshift : int = 0) -> plt.Figure:
        fig, ax = plt.subplots(figsize=figsize)
        ax.axis('equal')
        ax.set_xlim((int(-0.05*d), int(1.05*d)))
        ax.set_ylim((int(-0.05*d), int(1.05*d)))
        ax.set_xticks([]), ax.set_yticks([])
        sns.despine(left=True, bottom=True, right=True)
        for v1 in self.adjacency:
            for v2 in self.adjacency:
                ax.add_artist(ConnectionPatch(self.get_loc(v1), self.get_loc(v2), 'data'))
        for vname in self.adjacency:
            textposx, textposy = self.get_loc(vname)
            viz = Circle(self.get_loc(vname), vradius)
            viz.set_edgecolor(edge_col)
            viz.set_facecolor(self.get_col(vname))
            ax.annotate(vname, xy=self.get_loc(vname), fontsize=fsize, ha='center', xytext=(textposx, textposy+vshift), color=fcol)
            ax.add_artist(viz)
        if filename:
            fig.savefig(filename, dpi=dpi, bbox_inches="tight", pad_inches=0)
        plt.close()
        return fig

    
    def save(self, filename : str) -> None:
        assert isinstance(filename, str)
        with open(filename, 'wb') as fd:
            dill.dump(self, fd)
    
    @property
    def adjacency(self) -> Dict:
        return self.__G
            
def load_graph(filename : str) -> UndirectedWeightedGraph:
    assert isinstance(filename, str)
    with open(filename, 'rb') as fd:
        g = dill.load(fd)
    return g

def random_connected_graph(k=5) -> UndirectedWeightedGraph:
    np.random.seed(rseed)
    g = UndirectedWeightedGraph()
    
    for i in range(k):
        g.add_vertex(f'{i}')
        
    for i in range(k):
        for j in range(k):
            if i < j:
                g.add_edge(f'{i}', f'{j}')
    return g
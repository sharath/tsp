from typing import Tuple

def euclidean_distance(c1 : Tuple, c2 : Tuple) -> float:
    return ((c1[0] - c2[0])**2 + (c1[1] - c2[1])**2)**0.5
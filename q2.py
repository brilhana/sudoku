# Auteurs: Alexandre Brilhante, Yan Lajeunesse

import random
import sys
import time
import numpy as np

from search import *
from sudoku import *

def main():
    with open("100sudoku.txt", 'r') as f:
        for line in f:
            s = Sudoku(tuple(map(int, line[:-1])))
            start = time.time()
            print(depth_first_graph_search(s, bound=1000000), round(time.time()-start, 2))

main()
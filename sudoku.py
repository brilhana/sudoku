# Auteurs: Alexandre Brilhante, Yan Lajeunesse

import random
import sys
import numpy as np

from search import *

class Sudoku(Problem):
    def actions(self, state):
        state = grid(state)
        for i, j in zip(*np.where(state == 0)):
            line = state[i]
            column = state[:,j]
            square = state[i//3*3:i//3*3+3, j//3*3:j//3*3+3]
            for elem in range(1, 10):
                if elem not in line and elem not in column and elem not in square:
                    yield i, j, elem

    def result(self, state, action):
        i, j, elem = action
        temp = list(state)
        temp[i*9+j] = elem
        return tuple(temp)

    def goal_test(self, state):
        return 0 not in state and not count_conflict(state)

    def value(self, state):
        state = grid(state)
        temp = []
        for i, j in zip(*np.where(state == 0)):
            temp += [possibilities(state, i, j)]
        return len(temp)

class SudokuHillClimbing(Problem):
    def __init__(self, initial, goal=None):
        state = grid(initial)
        self.clean = grid(initial)
        self.zero = list(zip(*np.where(state == 0)))
        self.initial = state
        for i, j in zip(*np.where(state == 0)):
            poss = possibilities(state, i, j)
            state[i][j] = random.choice(poss)
        self.filled = tuple(state.flatten())
 
    def actions(self, state):
        state = grid(self.clean)
        for i, j in zip(*np.where(state == 0)):
            square = state[i//3*3:i//3*3+3, j//3*3:j//3*3+3]
            posX = i//3*3
            posY = j//3*3
            for x, y in zip(*np.where(square == 0)):
                x += posX
                y += posY
                if (i, j) != (x, y):
                    yield i, j, x, y

    def result(self, state, action):
        i, j, x, y = action
        temp = grid(state)
        temp[i][j], temp[x][y] = temp[x][y], temp[i][j]
        return tuple(temp)

    def goal_test(self, state):
        state = grid(state)
        for elem in range(1, 10):
            for x in state:
                if state[x].count(elem) > 1:
                    return False
                elif state[:, x].count(elem) > 1:
                    return False
        return True

    def value(self, state):
        return count_conflict(state)

def grid(state):
    return np.array(state).reshape((9, 9))

def line(state, line, elem):
    state = grid(state)
    return list(state[line]).count(elem) > 1 

def column(state, column, elem):
    state = grid(state)
    return list(state[:, column]).count(elem) > 1

def square(state, line, column, elem):
    state = grid(state)
    return list(tuple(state[line//3*3:line//3*3+3, column//3*3:column//3*3+3].flatten())).count(elem) > 1

def count_conflict(state):
    countConflicts = 0
    for x in range(9):
        for y in range(1, 10):
            if (line(state, x, y)):
                countConflicts += 1
            elif (column(state, x, y)):
                countConflicts += 1
        for i in range(9):
            for j in range(9):
                for k in range(1, 10):
                    if (square(state, i, j, k)):
                        countConflicts += 1
    return countConflicts

def possibilities(state, i, j):
    n = [x for x in range(1, 10)]
    temp = []
    state = grid(state)
    square = state[i//3*3:i//3*3+3, j//3*3:j//3*3+3]
    for elem in n:
        if elem not in square:
            temp.append(elem)
    return temp

def possibilities_grid(state, i, j):
    temp = []
    state = grid(state)
    line = state[i]
    column = state[:,j]
    square = state[i//3*3:i//3*3+3, j//3*3:j//3*3+3]
    for elem in range(1, 10):
        if (elem not in square) and (elem not in line) and (elem not in column) and state[i][j] == 0:
            temp.append(elem)
    return temp

def most_constrained(node):
    if node.parent is not None:
        i, j, elem = node.action
        return possibilities_grid(node.parent.state, i, j)
    return 0

def main():
    with open("1sudoku.txt", 'r') as f:
        for line in f:
            s = Sudoku(tuple(map(int, line[:-1])))
            #s2 = SudokuHillClimbing(tuple(map(int, line[:-1])))
            #print(depth_first_graph_search(s, 100000))
            #s3 = grid(simulated_annealing(s2))
            s34 = tuple(map(int, '530070000600195000098000060800060003400803001700020006060000280000419005000080079'))
            s34 = grid(s34)



            print(best_first_graph_search(s, most_constrained))

main()
import numpy as np


###


class GameNode():
    turn: str
    depth: int
    moves: list
    heuristic: int
    numberChildren: int
    debugIndex: int
    parent = None

    def __init__(self):
        self.moves = []
        self.turn = None
        self.parent = None
        self.heuristic = None

    def initialize(self, parentNode, turn: str, moves: list, depth: int = 0):
        self.numberChildren = 0
        #
        self.turn = turn
        self.depth = depth
        self.parent = parentNode
        self.moves = np.array(moves)
        #
        return self

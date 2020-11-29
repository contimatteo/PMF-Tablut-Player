import numpy as np


###


class GameNode():
    depth: int
    turn: str
    moves: list
    heuristic: int = None
    numberChildren: int
    parent = None

    def __init__(self):
        self.turn = None
        self.moves = []
        self.numberChildren=0

    def initialize(self, parentNode, turn: str, moves: list, depth: int = 0):
        self.depth = depth
        self.turn = turn
        self.moves = np.array(moves)
        self.parent = parentNode

        return self

import numpy as np


###


class GameNode():
    turn: str
    depth: int
    moves: list
    parent = None
    heuristic: int = None

    def __init__(self):
        self.moves = []
        self.turn = None

    def initialize(self, parentNode, turn: str, moves: list, depth: int = 0):
        self.turn = turn
        self.depth = depth
        self.parent = parentNode
        self.moves = np.array(moves)

        return self

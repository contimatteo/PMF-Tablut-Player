import numpy as np


###


class GameNode():
    depth: int
    turn: str
    moves: list
    heuristic: int = 0

    def __init__(self):
        self.turn = None
        self.moves = []

    def initialize(self, turn: str, moves: list, depth: int = 0):
        self.depth = depth
        self.turn = turn
        self.moves = np.array(moves)

        return self

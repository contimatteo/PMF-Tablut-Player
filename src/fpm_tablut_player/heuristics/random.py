import random
import networkx as nx

from fpm_tablut_player.libraries import GameState, GameTree, GameNode
from fpm_tablut_player.utils import DebugUtils
from fpm_tablut_player.heuristics import Heuristic


###


class RandomHeuristic(Heuristic):
    def assignValue(self,Node: GameNode):
        Node.heuristic = random.randint(1, 101)

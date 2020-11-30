import random
import networkx as nx

from fpm_tablut_player.libraries import GameTree, GameNode
from fpm_tablut_player.utils import DebugUtils
from fpm_tablut_player.heuristics import Heuristic


###


class RandomHeuristic(Heuristic):
    def assignValue(self, node: GameNode):
        node.heuristic = random.randint(1, 101)

import random
import networkx as nx

from fpm_tablut_player.libraries import GameTree, GameNode
from fpm_tablut_player.utils import DebugUtils


###


class MontecarloAlgorithm():
    def getMorePromisingNode(self, tree_with_heuristics: GameTree) -> GameNode:
        #
        # TODO: missing code.
        # ...
        #
        ChildrenArcs = list(nx.bfs_edges(tree_with_heuristics.graph, tree_with_heuristics.root))
        Children = []

        for u, v in ChildrenArcs:
            Children.append(v)

        selectedIndex = random.randint(1, len(Children))

        DebugUtils.info("Montecarlo best move is {}", [str(Children[selectedIndex].moves)])
        DebugUtils.space()

        return Children[selectedIndex]

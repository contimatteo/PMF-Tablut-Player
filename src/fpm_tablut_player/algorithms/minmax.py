from fpm_tablut_player.libraries import GameTree, GameNode
from fpm_tablut_player.utils import DebugUtils
from fpm_tablut_player.heuristics import Heuristic, RandomHeuristic

###


class MinMaxAlgorithm():
    max: str = "white"
    min: str = "black"
    heuristic: Heuristic

    ###

    def __init__(self, type_heuristic: str):
        if type_heuristic == "Random":
            self.heuristic = RandomHeuristic()
        else:  # default heuristic
            self.heuristic = RandomHeuristic()

    def __elaborateNodeValues(self, tree_with_heuristics: GameTree):
        node = tree_with_heuristics.root
        L = [node]
        while len(L) > 0:
            x = L[-1]
            if x == node and x.heuristic is not None:
                L.pop()
            elif x.heuristic is not None:
                if x.parent.heuristic is None:
                    x.parent.heuristic = x.heuristic
                elif x.parent.turn == self.min and x.heuristic < x.parent.heuristic:
                    x.parent.heuristic = x.heuristic
                elif x.parent.turn == self.max and x.heuristic > x.parent.heuristic:
                    x.parent.heuristic = x.heuristic

                L.pop()
            else:
                children = GameTree.getChildren(tree_with_heuristics.graph, x, True)
                if len(children) > 0:
                    L = L + children
                else:  # foglia senza euristica
                    self.heuristic.assignValue(x)

    ###

    def getMorePromisingNode(self, tree_with_heuristics: GameTree) -> GameNode:
        self.__elaborateNodeValues(tree_with_heuristics)

        root = tree_with_heuristics.root
        children = GameTree.getChildren(tree_with_heuristics.graph, root, False)

        bestNode = None
        heuristicValue = None

        # DebugUtils.info("MinMaxAlogorithm", [])
        for node in children:
            # DebugUtils.info("       next possible move {} value {}",
            #                 [str(node.moves), node.heuristic])
            if heuristicValue is None:
                heuristicValue = node.heuristic
                bestNode = node
            elif root.turn == self.max and node.heuristic > heuristicValue:
                heuristicValue = node.heuristic
                bestNode = node
            elif root.turn == self.min and node.heuristic < heuristicValue:
                heuristicValue = node.heuristic
                bestNode = node

        # DebugUtils.info("       Best move is {}", [str(bestNode.moves)])
        # DebugUtils.space()

        return bestNode

from fpm_tablut_player.libraries import GameTree, GameNode
from fpm_tablut_player.utils import DebugUtils


###


class MinMaxAlgorithm():
    max: str = "white" 
    min: str = "black" 

    ###

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

    ###

    def getMorePromisingNode(self, tree_with_heuristics: GameTree) -> GameNode:
        self.__elaborateNodeValues(tree_with_heuristics)

        root = tree_with_heuristics.root
        children = GameTree.getChildren(tree_with_heuristics.graph, root, False)

        bestNode = None
        heuristicValue = None

        # print("root heuristic value ",root.heuristic," turn ",root.turn)

        for node in children:
            # print("next possible move ",str(node.moves), "value ",node.heuristic)
            if heuristicValue is None:
                heuristicValue = node.heuristic
                bestNode = node
            elif root.turn == self.max and node.heuristic > heuristicValue:
                heuristicValue = node.heuristic
                bestNode = node
            elif root.turn == self.min and node.heuristic < heuristicValue:
                heuristicValue = node.heuristic
                bestNode = node

        DebugUtils.info("MinMax best move is {}", [str(bestNode.moves)])
        DebugUtils.space()

        return bestNode

import random
import networkx as nx

from fpm_tablut_player.libraries import GameState, GameTree, GameNode
from fpm_tablut_player.utils import DebugUtils

###


class RandomHeuristic():
    searchTree: GameTree

    def loadTree(self, tree: GameTree):
        self.searchTree = tree

    def getLeaves(self) -> [GameNode]:
        leaves = []
        node = None
        graph = self.searchTree.graph
        controlsNode = [self.searchTree.root]

        while len(controlsNode) > 0:
            # print("ELEMENT TO CONTROL ARE: ",len(controlsNode))
            node = controlsNode.pop(0)
            children = list(nx.bfs_edges(graph, node))
            # print("we have ",len(children),"children")
            if len(children) == 0:
                leaves.append(node)
            else:
                for u, v in children:
                    controlsNode.append(v)

        return leaves

    def assignValues(self) -> GameTree:
        # print("TREE HAS ",len(self.searchTree.graph)," NODES")
        # print("\n\nSTART COMPUTING EURISTIC");
        leaves = self.getLeaves()

        # print("LEAVES COMPUTED");
        for leaf in leaves:
            leaf.heuristic = random.randint(1, 101)

        # print("NUMERO DI FOGLIE: ",len(leaves));
        for leaf in leaves:
            DebugUtils.info("heuristic selected for  {} is {}", [leaf.moves, leaf.heuristic])
        DebugUtils.space()
        
        return self.searchTree

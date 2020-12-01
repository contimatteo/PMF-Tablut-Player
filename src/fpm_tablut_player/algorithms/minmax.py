from fpm_tablut_player.libraries import GameTree, GameNode, GameState
from fpm_tablut_player.utils import DebugUtils
from fpm_tablut_player.heuristics import Heuristic, RandomHeuristic
import networkx as nx
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

    def __elaborateNodeValues(self, tree_with_heuristics: GameTree, initialState: GameState):
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
                else: #foglia senza euristica
                    self.heuristic.assignValue(x, initialState)

    ###

    def getMorePromisingNode(self, tree_with_heuristics: GameTree, initialState: GameState) -> GameNode:
        
        root = tree_with_heuristics.root
        children = GameTree.getChildren(tree_with_heuristics.graph, root, False)

        self.__elaborateNodeValues(tree_with_heuristics, initialState)

        bestNode = None
        heuristicValue = None
        #DebugUtils.info(" This root has {} children",[len(children)])
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
        DebugUtils.info("       Best move is {}", [str(bestNode.moves)])
        DebugUtils.space()

        return bestNode


# root=GameNode().initialize(None,"white", [],0)
# child1=GameNode().initialize(root,"black", [],1)
# child2=GameNode().initialize(root,"black", [],1)

# child11=GameNode().initialize(child1,"white", [],2)
# child12=GameNode().initialize(child1,"white", [],2)
# child11.heuristic=2
# child12.heuristic=5

# child21=GameNode().initialize(child2,"white", [],2)
# child22=GameNode().initialize(child2,"white", [],2)
# child21.heuristic=1
# child22.heuristic=0

# root.debugIndex=0
# child1.debugIndex=1

# child2.debugIndex=2
# child11.debugIndex=3
# child12.debugIndex=4
# child21.debugIndex=5
# child22.debugIndex=6


# child1.moves=[{"from":(0,0),"to":(0,1)}]
# child2.moves=[{"from":(0,0),"to":(0,2)}]

# child11.moves=[{"from":(0,0),"to":(0,1)},{"from":(0,1),"to":(1,1)}]
# child12.moves=[{"from":(0,0),"to":(0,1)},{"from":(0,1),"to":(2,1)}]


# child21.moves=[{"from":(0,0),"to":(0,2)},{"from":(0,2),"to":(1,2)}]
# child22.moves=[{"from":(0,0),"to":(0,2)},{"from":(0,2),"to":(2,2)}]



# G=nx.DiGraph()
# G.add_node(root)
# G.add_edge(root,child1)
# G.add_edge(root,child2)

# G.add_edge(child1,child11)
# G.add_edge(child1,child12)

# G.add_edge(child2,child21)
# G.add_edge(child2,child22)

# tree=GameTree()
# tree.graph=G
# tree.root=root
# minMax=MinMaxAlgorithm("Random")

# #print("root has ",len(tree.getChildren(tree.graph,root,True)))
# best=minMax.getMorePromisingNode(tree,None)


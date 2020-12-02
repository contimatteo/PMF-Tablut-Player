from fpm_tablut_player.libraries import GameTree, GameNode, GameState;
from fpm_tablut_player.utils import DebugUtils
from fpm_tablut_player.heuristics import Heuristic, RandomHeuristic
#import networkx as nx

class AlphaBetaCutAlgorithm():
    max: str ="white"
    min: str ="black"
    heuristic: Heuristic


    def __init__(self,type_heuristic: str):
        if type_heuristic == "Random":
            self.heuristic = RandomHeuristic()
        else: #default heuristic
            self.heuristic = RandomHeuristic()

    def __elaborateNodeValues(self,tree_with_heuristics: GameTree, initialState: GameState):
        node = tree_with_heuristics.root
        L=[node]
        #Log=[0]
        while len(L)>0:
            x=L[-1]
        
            if x == node and x.heuristic is not None:
                #DebugUtils.info("last node I have finished",[])
                L.pop()
                #Log.pop()
            elif x.heuristic is not None:
                #DebugUtils.info("current node has a value",[])
                alpha=None
                beta =None


                if x.parent.turn == self.min: # parent is min node
                    #DebugUtils.info("     parent is a min node => status",[])
                    beta = x.parent.heuristic

                    if (beta is None) or (x.heuristic < beta):
                        beta = x.heuristic
                        #beta o la prima volta che vine ne inizializzato o trova un volore migliore


                    if x.parent.parent is not None:
                        alpha = x.parent.parent.heuristic

                    #DebugUtils.info("     alpha: {} beta: {}",[alpha,beta])
                    x.parent.heuristic = beta
                    if alpha is not None and alpha >= beta:
                        #DebugUtils.info("parent is min => cancello a partire da {}",[(x.debugIndex+1)])
                        DebugUtils.info("L {} CHILDREN {}",[len(L),x.parent.numberChildren])
                        while x.parent.numberChildren > 0 :#remove all x.parent children
                            L.pop()
                            #Log.pop()
                            x.parent.numberChildren = x.parent.numberChildren -1
                    else:
                        x.parent.numberChildren = x.parent.numberChildren -1
                    L.pop()
                    #Log.pop()
                ##################################################################  
                else: # parent is a max node
                    #DebugUtils.info("     parent is a max node",[])
                    alpha = x.parent.heuristic

                    if (alpha is None) or (x.heuristic > alpha):
                        alpha = x.heuristic
                        #alpha o la prima volta che vine ne inizializzato o trova un volore migliore


                    if x.parent.parent is not None:
                        beta = x.parent.parent.heuristic

                    #DebugUtils.info("     alpha: {} beta: {}",[alpha,beta])
                    x.parent.heuristic = alpha

                    if beta is not None and alpha >= beta:
                        #DebugUtils.info("parent is max => cancello a partire da {}",[x.debugIndex])
                        while x.parent.numberChildren > 0 :#remove all x.parent children
                            L.pop()
                            x.parent.numberChildren = x.parent.numberChildren -1
                    else:
                        x.parent.numberChildren = x.parent.numberChildren -1
                    L.pop()
                    #Log.pop()

            ##################################################################
            else:
                #DebugUtils.info("non terminal node => adding children",[])
                children=GameTree.getChildren(tree_with_heuristics.graph,x,True)
                x.numberChildren=len(children)

                if len(children) > 0:
                    L=L+children
                    #for child in children:
                    #    Log=Log +[child.debugIndex]
                else: #leaf without heurisitc
                    self.heuristic.assignValue(x, initialState)
                    
    def getMorePromisingNode(self, tree_with_heuristics: GameTree, initialState: GameState) -> GameNode:
        root = tree_with_heuristics.root
        children = GameTree.getChildren(tree_with_heuristics.graph,root,False)

        if len(children) == 0:
            return None

        #DebugUtils.info("AlphaBetaCutAlogorithm", [])
        self.__elaborateNodeValues(tree_with_heuristics, initialState)

        heuristicValue = None
        bestNode = None

        for node in children:
            #DebugUtils.info("       next possible move {} value {}",[str(node.moves), node.heuristic])
            if node.heuristic is not None:
                if heuristicValue == None :
                    heuristicValue = node.heuristic
                    bestNode = node
                elif root.turn == self.max and node.heuristic > heuristicValue:
                    heuristicValue = node.heuristic
                    bestNode = node
                elif root.turn == self.min and node.heuristic < heuristicValue:
                    heuristicValue = node.heuristic
                    bestNode = node
        
        #DebugUtils.info("AlphaBetaCut best move is {} with value {}", [str(bestNode.moves),bestNode.heuristic])
        #DebugUtils.space()
        return bestNode

#root=GameNode().initialize(None,"white", [],0)
#child1=GameNode().initialize(root,"black", [],1)
#child2=GameNode().initialize(root,"black", [],1)
#
#child11=GameNode().initialize(child1,"white", [],2)
#child12=GameNode().initialize(child1,"white", [],2)
#child11.heuristic=2
#child1.moves=[{"from":"tua sorella","to":"tua madre"}]
#child12.heuristic=5
#
#child21=GameNode().initialize(child2,"white", [],2)
#child22=GameNode().initialize(child2,"white", [],2)
#child21.heuristic=1
#child22.heuristic=0
#
#root.debugIndex=0
#child1.debugIndex=1
#child2.debugIndex=2
#child11.debugIndex=3
#child12.debugIndex=4
#child21.debugIndex=5
#child22.debugIndex=6
#
#
#G=nx.DiGraph()
#G.add_node(root)
#G.add_edge(root,child1)
#G.add_edge(root,child2)
#
#G.add_edge(child1,child11)
#G.add_edge(child1,child12)
#
#G.add_edge(child2,child21)
#G.add_edge(child2,child22)
#
#tree=GameTree()
#tree.graph=G
#tree.root=root
#alphabeta=AlphaBetaCutAlgorithm()
#
#print("root has ",len(tree.getChildren(tree.graph,root,True)))
#best=alphabeta.getMorePromisingState(tree)
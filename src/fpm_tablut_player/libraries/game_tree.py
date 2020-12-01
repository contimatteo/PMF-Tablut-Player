# import numpy as np
import networkx as nx

# import fpm_tablut_player.configs as CONFIGS
from fpm_tablut_player.libraries.game_node import GameNode


###


class GameTree():
    root: GameNode
    graph: nx.DiGraph

    def __init__(self):
        self.graph = nx.DiGraph()
        self.root = None

    ###

    def initialize(self, rootNode: GameNode):
        self.root = rootNode
        return self

    def addNode(self, parent: GameNode,nodes: [GameNode]):
        for node in nodes:
            self.graph.add_edge(parent, node, weight=0)

    def bfs(self, withRootNode: bool = False) -> [GameNode]:
        root = self.root

        if withRootNode:
            return [root] + GameTree.getChildren(self.graph, root)

        return GameTree.getChildren(self.graph, root)

        # edges = nx.bfs_edges(self.graph, root)
        # if withRootNode:
        #    return [root] + [v for u, v in edges]
        #
        # return [v for u, v in edges]

    ###

    @staticmethod
    def getChildren(graph: nx.DiGraph, node: GameNode, inverse: bool = False) -> [GameNode]:
        #edges = list(nx.bfs_edges(graph, node))
        edges = list(graph.edges(node))
        if inverse:
            L = []
            for u, v in edges:
                L = [v]+L
            return L

        return [v for u, v in edges]

import numpy as np
import networkx as nx

import fpm_tablut_player.configs as CONFIGS
from fpm_tablut_player.libraries.game_node import GameNode


###


class GameTree():
    root: GameNode
    graph: nx.Graph

    def __init__(self):
        self.graph = nx.Graph()
        self.root = None

    ###

    def initialize(self, rootNode: GameNode):
        self.root = rootNode
        return self

    def addNode(self, nodes: [GameNode]):
        for node in nodes:
            self.graph.add_edge(self.root, node, weight=0)

    def bfs(self, withRootNode: bool = False) -> [GameNode]:
        root = self.root
        edges = nx.bfs_edges(self.graph, root)

        if withRootNode:
            return [root] + [v for u, v in edges]

        return [v for u, v in edges]

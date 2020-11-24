from fpm_tablut_player.libraries import GameState, GameTree

###


class RandomHeuristic():
    searchTree: GameTree

    def loadTree(self, tree: GameTree):
        self.searchTree = tree

    def assignValues(self) -> GameTree:
        # ...
        # missing
        # ...
        return self.searchTree

from fpm_tablut_player.network import SocketManager as SocketManagerClass
from fpm_tablut_player.utils import DebugUtils
from fpm_tablut_player.schemas import GameState, GameMove
from fpm_tablut_player.libraries import RandomHeuristic, MontecarloAlgorithm


###


class Game():
    SocketManager: SocketManagerClass
    gameState: GameState

    def __init__(self):
        self.SocketManager = SocketManagerClass()

    def __is_finished(self):
        return self.SocketManager.socket is None

    def __loadGameState(self, stateFromServer: dict):
        self.gameState = GameState(stateFromServer)

    def __computeNextGameMove(self):
        tree_without_heuristics = self.gameState.generateSearchTree()

        # heuristic
        heuristic = RandomHeuristic()
        # algorithm
        algorithm = MontecarloAlgorithm()
        # next move
        next_move = GameMove()

        # load the tree in the Heuristic class.
        heuristic.loadTree(tree_without_heuristics)
        # add heuristic values.
        tree_with_heuristics = heuristic.assignValues()

        # compute the game state that we want to reach.
        gameStateToReach = algorithm.extract(tree_with_heuristics)

        # comute the move for going from: {self.gameState} -> to: {gameStateToReach}.
        next_move.compute(self.gameState, gameStateToReach)

        #
        return next_move

    ###

    def start(self):
        DebugUtils.space()
        initial_state = self.SocketManager.initialize()

        DebugUtils.info("initial state = {}", [initial_state])
        DebugUtils.space()

        while not self.__is_finished():
            self.SocketManager.listen(self)

        ###
        # 1. Capire quando il gioco finisce
        # 2. Funzione per capire se una mossa è valida
        # 3. Finchè non finisce il gicoo
        # 1. leggere lo stato del gioco (dal server)
        # 2. salvarcelo in una nostra struttura (`GameState`)
        # 3. calcolare tutte le mosse valide fino al livello `k` (=1)
        # 4. calcolo dell'eurisitca per ogni nodo (anche al punto prima volendo)
        # 5. algortimo di ricerca (montecarlo, ...)
        # 6. trovata la prossima mossa, mandarla al server
        ###

    def play(self, stateFromServer: dict):
        self.__loadGameState(stateFromServer)

        next_move = self.__computeNextGameMove()

        self.SocketManager.send_json(next_move)

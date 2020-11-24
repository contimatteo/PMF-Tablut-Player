import networkx as nx

from fpm_tablut_player.algorithms import MontecarloAlgorithm
from fpm_tablut_player.heuristics import RandomHeuristic
from fpm_tablut_player.network import SocketManager as SocketManagerClass
from fpm_tablut_player.libraries import GameState, GameMove, GameTree, GameNode
from fpm_tablut_player.utils import DebugUtils

import fpm_tablut_player.configs as CONFIGS


###


class Game():
    SocketManager: SocketManagerClass
    gameState: GameState
    searchTree: GameTree
    turn: str

    def __init__(self):
        self.turn = None
        self.SocketManager = SocketManagerClass()

    def __is_finished(self) -> bool:
        return self.SocketManager.socket is None

    def __loadGameState(self, stateFromServer: dict):
        self.gameState = GameState()
        self.gameState.createFromServerState(stateFromServer)

    def __is_my_turn(self) -> bool:
        return str(self.turn) == str(CONFIGS.APP_ROLE)

    def __generateSearchTree(self) -> GameTree:
        currentTurn = CONFIGS.APP_ROLE
        rootNode = GameNode().initialize(currentTurn, [], 0)

        # create the tree
        self.searchTree = GameTree().initialize(rootNode)
        # prepare the queue for visiting the nodes.
        nodesToVisit: [GameNode] = [rootNode]

        #
        for currentRootNode in nodesToVisit:
            currentGameState: GameState = GameState().createfromNode(self.gameState, currentRootNode)
            # check the `max-depth` limit configutation.
            if currentRootNode.depth > CONFIGS.K:
                continue
            #
            for move in currentGameState.getPossibleMoves(currentRootNode.turn):
                depth = currentRootNode.depth + 1
                nextTurn = Game.togglTurn(currentTurn)
                movesToSave = currentRootNode.moves + [move]
                #
                newNode = GameNode().initialize(nextTurn, movesToSave, depth)
                #
                self.searchTree.addNode([newNode])
                #
                nodesToVisit.append(newNode)

    def __computeNextGameMove(self) -> GameMove:
        self.__generateSearchTree()

        # heuristic
        heuristic = RandomHeuristic()
        # load the tree in the Heuristic class.
        heuristic.loadTree(self.searchTree)

        # add heuristic values.
        self.searchTree = heuristic.assignValues()

        # algorithm
        algorithm = MontecarloAlgorithm()
        # compute the game state that we want to reach.
        nodeToReach: GameNode = algorithm.getMorePromisingState(self.searchTree)
        # convert the `nodeToReach` to a state
        gameStateToReach: GameState = GameState().createfromNode(self.gameState, nodeToReach)

        # comute the move for going from: {self.gameState} -> to: {gameStateToReach}.
        next_move: GameMove = GameMove().fromStartToEnd(self.gameState, gameStateToReach)
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
        # parse turn "value" from the server
        self.turn = str(stateFromServer["turn"]).lower()

        # check if is my turn.
        if not self.__is_my_turn():
            return
        else:
            DebugUtils.info("stateFromServer -> {}", [str(stateFromServer)])

        #
        self.__loadGameState(stateFromServer)

        #
        next_move = self.__computeNextGameMove()
        obj_to_send = next_move.export()

        #
        self.SocketManager.send_json(obj_to_send)

    ###

    @staticmethod
    def togglTurn(turn: str):
        if turn == 'white':
            return 'black'

        return 'white'

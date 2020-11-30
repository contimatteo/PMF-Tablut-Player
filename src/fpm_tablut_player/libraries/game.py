# import networkx as nx

from fpm_tablut_player.algorithms import MinMaxAlgorithm
from fpm_tablut_player.heuristics import RandomHeuristic
from fpm_tablut_player.network import SocketManager as SocketManagerClass
from fpm_tablut_player.libraries import GameState, GameMove, GameTree, GameNode
from fpm_tablut_player.utils import DebugUtils, GameUtils

import fpm_tablut_player.configs as CONFIGS


###


class Game():
    turn: str
    gameState: GameState
    searchTree: GameTree
    SocketManager: SocketManagerClass

    ###

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
        rootNode = GameNode().initialize(None, currentTurn, [], 0)

        # create the tree
        self.searchTree = GameTree().initialize(rootNode)
        # prepare the queue for visiting the nodes.
        nodesToVisit: [GameNode] = [rootNode]

        #
        for currentRootNode in nodesToVisit:
            currentGameState = GameState().createfromGameNode(self.gameState, currentRootNode)
            # check the `max-depth` limit configutation.
            #
            # TODO: [@contimatteo] use a Timer to stop the search.
            #
            if currentRootNode.depth >= CONFIGS.K:
                continue
            #
            for move in currentGameState.getPossibleMoves(currentRootNode.turn):
                depth = currentRootNode.depth + 1
                nextTurn = GameUtils.togglTurn(currentTurn)
                movesToSave = list(currentRootNode.moves) + [move]
                #
                newNode = GameNode().initialize(currentRootNode, nextTurn, movesToSave, depth)
                #
                nodesToVisit.append(newNode)
                self.searchTree.addNode([newNode])

    def __computeNextGameMove(self) -> GameMove:
        self.__generateSearchTree()

        # load the tree in the Heuristic class.
        # heuristic = RandomHeuristic().loadTree(self.searchTree)

        # add heuristic values.
        #self.searchTree = heuristic.assignValues()

        # algorithm
        algorithm = MinMaxAlgorithm("Random")
        # compute the game state that we want to reach.
        nodeToReach: GameNode = algorithm.getMorePromisingNode(self.searchTree)

        # convert the `nodeToReach` to a state
        gameStateToReach = GameState().createfromGameNode(self.gameState, nodeToReach)

        # comute the move for going from: {self.gameState} -> to: {gameStateToReach}.
        next_move = GameMove().fromStartToEnd(self.gameState, gameStateToReach)
        #
        return next_move

    ###

    def start(self):
        DebugUtils.space()
        initial_state = self.SocketManager.initialize()

        DebugUtils.info("initial state = {}", [initial_state])
        DebugUtils.space()

        # try to play (if I'm the white player ...).
        self.play(initial_state)

        while not self.__is_finished():
            self.SocketManager.listen(self)

    def play(self, stateFromServer: dict):
        # parse turn "value" from the server
        self.turn = GameUtils.turnToString(stateFromServer["turn"])

        # check if is my turn.
        if not self.__is_my_turn():
            return
        else:
            DebugUtils.info("stateFromServer -> {}", [str(stateFromServer)])

        # convert the state received from the server to a {GameState} instance.
        self.__loadGameState(stateFromServer)

        # extract the "best" move for my player.
        next_move = self.__computeNextGameMove()

        # send the move to the server.
        self.SocketManager.send_json(next_move.export())

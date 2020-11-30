import fpm_tablut_player.configs as CONFIGS
from fpm_tablut_player.algorithms import MinMaxAlgorithm
from fpm_tablut_player.network import SocketManager as SocketManagerClass
from fpm_tablut_player.libraries import GameState, GameMove, GameTree, GameNode
from fpm_tablut_player.utils import DebugUtils, GameUtils, Timer


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

        # create the tree.
        self.searchTree = GameTree().initialize(rootNode)
        # prepare the queue for visiting the nodes.
        nodesToVisit: [GameNode] = [rootNode]

        # start the timer.
        timer: Timer = Timer().start()

        #
        for currentRootNode in nodesToVisit:
            # check if the time for generating the tree is not expired.
            if timer.get_time_left(CONFIGS.GAME_TREE_GENERATION_TIMEOUT) <= 0:
                timer.stop()
                break
            # create a {GameState} instance satrting from a {GameNode}.
            currentGameState = GameState().createfromGameNode(self.gameState, currentRootNode)
            # try to the generate childrens of current node.
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
        # self.searchTree = heuristic.assignValues()

        # algorithm
        algorithm = MinMaxAlgorithm("Random")
        # extract the best node.
        nodeToReach: GameNode = algorithm.getMorePromisingNode(self.searchTree)

        # extract the move from the best node {nodeToReach}.
        return GameMove().fromGameNode(nodeToReach)

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
        # convert this move to the server accepting format.
        game_move_to_server_rappresentation = next_move.export()

        # send the move to the server.
        self.SocketManager.send_json(game_move_to_server_rappresentation)

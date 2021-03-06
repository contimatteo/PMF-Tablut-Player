# from multiprocessing.dummy import Pool as ThreadPool
from multiprocessing import Process, Queue, Pool, Manager
import numpy as np
import copy

import fpm_tablut_player.configs as CONFIGS
from fpm_tablut_player.algorithms import MinMaxAlgorithm, AlphaBetaCutAlgorithm
from fpm_tablut_player.network import SocketManager as SocketManagerClass
from fpm_tablut_player.libraries import GameState, GameMove, GameTree, GameNode
from fpm_tablut_player.utils import DebugUtils, GameUtils, Timer


###

THREADS_COUNT: int = int(CONFIGS._PARALLEL_THREADS_NUMBER)

###


class GameMultithread():
    turn: str
    gameState: GameState
    searchTree: [GameTree]
    SocketManager: SocketManagerClass

    ###

    def __init__(self):
        self.turn = None
        self.searchTree = np.repeat(None, THREADS_COUNT)
        self.SocketManager = SocketManagerClass()

    def __is_finished(self) -> bool:
        return self.SocketManager.socket is None

    def __loadGameState(self, stateFromServer: dict):
        self.gameState = GameState()
        self.gameState.createFromServerState(stateFromServer)
        DebugUtils.info("BLACKS: {} WHITES: {} KING: {}", [
                        self.gameState.BlackNumber, self.gameState.WhiteNumber, self.gameState.King])

    def __is_my_turn(self) -> bool:
        return str(self.turn) == str(CONFIGS.APP_ROLE)

    def __multithreadSearchOfBestMove(self) -> GameMove:
        parallel_jobs = []
        bestNodesToReach: [GameNode] = []

        # #################################################################### #
        # ###################### Start Multithread Mode ###################### #

        multiprocessingManager = Manager()
        asyncResultNodesQueue = multiprocessingManager.Queue()

        params = []
        for index in range(THREADS_COUNT):
            queue = asyncResultNodesQueue
            gameState = copy.deepcopy(self.gameState)
            params.append((index, queue, gameState))

        pool = Pool(THREADS_COUNT)
        pool.map(GameProcess.computeNextGameMoveInParallel, params)
        pool.close()
        pool.join()

        # group the results in a list.
        for index in range(THREADS_COUNT):
            # gameNode: GameNode = asyncResultNodesQueue.get()
            gameNode: GameNode = asyncResultNodesQueue.get_nowait()
            bestNodesToReach.append(gameNode)

        # filter the 'None' values.
        bestNodesToReach = [node for node in bestNodesToReach if node is not None]

        # ####################### End Multithread Mode ####################### #
        # #################################################################### #

        # find the best node inside the {bestNodesToReach} list.
        bestNodeToReach: GameNode = bestNodesToReach[0]
        for currentNode in bestNodesToReach:
            if self.turn == "white":
                if currentNode.heuristic > bestNodeToReach.heuristic:
                    bestNodeToReach = currentNode
            else:
                if currentNode.heuristic < bestNodeToReach.heuristic:
                    bestNodeToReach = currentNode

        # extract the move from the best node {nodeToReach}.
        return GameMove().fromGameNode(bestNodeToReach)

    def __showGame(self, board):
        B = list(board)
        row_str = ""

        OKBLUE = '\033[94m'
        OKCYAN = '\033[96m'
        OKGREEN = '\033[92m'
        WARNING = '\033[93m'
        FAIL = '\033[91m'
        ENDC = '\033[0m'

        DebugUtils.space()
        for i in range(9):
            DebugUtils.info(
                "{}----- ----- ----- ----- ----- ----- ----- ----- -----{}", [OKGREEN, ENDC])
            row_str = ""
            for j in range(9):
                row_str += ""+OKGREEN+"| "+ENDC
                if B[i][j] == "WHITE":
                    row_str += "W"
                elif B[i][j] == "BLACK":
                    row_str += ""+WARNING+"B"+ENDC
                elif B[i][j] == "THRONE":
                    row_str += ""+OKBLUE+"T"+ENDC
                elif B[i][j] == "KING":
                    row_str += ""+FAIL+"K"+ENDC
                else:
                    row_str += " "
                row_str += ""+OKGREEN+" | "+ENDC
            DebugUtils.info(row_str, [])
            DebugUtils.info(
                "{}----- ----- ----- ----- ----- ----- ----- ----- -----{}", [OKGREEN, ENDC])
        DebugUtils.space()

    ###

    def start(self):
        DebugUtils.space()
        initial_state = self.SocketManager.initialize()

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
            # DebugUtils.info("stateFromServer -> {}", [str(stateFromServer)])
            self.__showGame(stateFromServer["board"])

        # convert the state received from the server to a {GameState} instance.
        self.__loadGameState(stateFromServer)

        # extract the "best" move for my player.
        next_move = self.__multithreadSearchOfBestMove()

        # convert this move to the server accepting format.
        game_move_to_server_rappresentation = next_move.export()
        # send the move to the server.
        self.SocketManager.send_json(game_move_to_server_rappresentation)


###

class GameProcess():

    @staticmethod
    def computeNextGameMoveInParallel(params: tuple):
        thread_index = params[0]
        asyncResultNodesQueue: Queue = params[1]
        gameState: GameState = params[2]

        # generate the search tree.
        searchTree = GameProcess.generateSearchTreeInParallel(params)

        # start the timer.
        timer = Timer().start()
        # algorithm
        # algorithm = MinMaxAlgorithm()
        algorithm = AlphaBetaCutAlgorithm()

        # extract the best node.
        nodeToReach: GameNode = algorithm.getMorePromisingNode(searchTree, gameState)

        #
        DebugUtils.info("[{}] >> (AlphaBetaCutAlgorithm) ended in {} seconds",
                        [thread_index, timer.get_elapsed_time()])
        # DebugUtils.info("       BEST MOVE {}",[nodeToReach.moves])
        # stop the timer.
        timer.stop()

        # return nodeToReach
        asyncResultNodesQueue.put(nodeToReach)

    @staticmethod
    def generateSearchTreeInParallel(params: tuple) -> GameTree:
        thread_index = params[0]
        gameState: GameState = params[2]

        #
        currentTurn = GameUtils.turnToString(CONFIGS.APP_ROLE)
        nodes_generated_counter = 0

        # create the root node
        rootNode = GameNode().initialize(None, currentTurn, [], 0)

        # create the tree.
        searchTree = GameTree().initialize(rootNode)
        # prepare the queue for visiting the nodes.
        nodesToVisit: [GameNode] = [rootNode]

        # start the timer.
        timer: Timer = Timer().start()

        # start visiting the tree with a BFS search.
        while nodesToVisit:
            currentGameState: GameState = None
            currentRootNode: GameNode = nodesToVisit.pop(0)
            #
            # check if the time for generating the tree is not expired.
            time_left = timer.get_time_left(CONFIGS.GAME_TREE_GENERATION_TIMEOUT)
            if time_left <= 0:
                DebugUtils.info("[{}] >> (TreeGeneration) timeout emitted", [thread_index])
                DebugUtils.info("[{}] >> (TreeGeneration) depth = {}", [
                    thread_index, currentRootNode.depth])
                break
            if currentRootNode.depth > int(CONFIGS._GAME_TREE_MAX_DEPTH):
                DebugUtils.info("[{}] >> (TreeGeneration) max-depth reached", [thread_index])
                DebugUtils.info("[{}] >> (TreeGeneration) depth = {}", [
                    thread_index, currentRootNode.depth])
                break
            #
            # try to create a {GameState} instance starting from a GameNode moves.
            currentGameState: GameState = None
            try:
                currentGameState = GameState().createFromMoves(gameState, currentRootNode.moves)
            except Exception as _:
                continue
            # get possible moves
            moves = currentGameState.getPossibleMoves(currentRootNode.turn)
            #
            # if {currentNode} is the root node, then filter the available moves at first level.
            if currentRootNode.depth == 0:
                moves = np.array_split(moves, THREADS_COUNT)[thread_index]
            #
            # try to the generate childrens of current node.
            for move in moves:
                nodes_generated_counter += 1
                #
                depth = currentRootNode.depth + 1
                nextTurn = GameUtils.togglTurn(currentRootNode.turn)
                movesToSave = list(currentRootNode.moves) + [move]
                #
                newNode = GameNode().initialize(currentRootNode, nextTurn, movesToSave, depth)
                #
                nodesToVisit.append(newNode)
                searchTree.addNode(currentRootNode, [newNode])

        #
        DebugUtils.info("[{}] >> (TreeGeneration) ended in {} seconds",
                        [thread_index, timer.get_elapsed_time()])
        DebugUtils.info("[{}] >> (TreeGeneration) number of generated nodes = {}",
                        [thread_index, nodes_generated_counter])
        # stop the timer.
        timer.stop()

        return searchTree

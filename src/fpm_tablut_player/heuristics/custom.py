import random

from fpm_tablut_player.libraries import GameTree, GameNode, GameState
from fpm_tablut_player.utils import DebugUtils, GameUtils


###

ESCAPE_CELLS: list = GameUtils.getEscapeCells()

###


class CustomHeuristic():

    @staticmethod
    def __iskingAlive(currentState: GameState) -> bool:
        return currentState.state.King is not None

    @staticmethod
    def __isKingOnEscapeArea(currentState: GameState) -> bool:
        found = False
        for escape in ESCAPE_CELLS:
            if escape == currentState.King:
                found = True
                break
        return found

    @staticmethod
    def __kingIsNearTheEscape(currentState: GameState):
        pass

    @staticmethod
    def __getPlayablePawns(currentState: GameState) -> int:
        if currentState.turn == "black":
            return currentState.state.BlackNumber
        return currentState.state.WhiteNumber

    @staticmethod
    def __blackPawnNearTheKing(currentState: GameState):
        #
        # TODO: missing ...
        #
        pass

    @staticmethod
    def __getNumberOfKills(currentState: GameState) -> int:
        #
        # TODO: missing ...
        #
        pass

    @staticmethod
    def __computeForBlack(currentState: GameState):
        #
        # TODO: missing ...
        #
        pass

    @staticmethod
    def __computeForWhite(currentState: GameState):
        #
        # TODO: missing ...
        #
        pass

    ###

    @staticmethod
    def assignValue(initialState: GameState, node: GameNode):
        currentState = GameState().createFromMoves(initialState, node.moves)

        # ########################################
        # TODO: [@contimatteo] remove this logic #
        node.heuristic = random.randint(1, 101)  #
        # ########################################

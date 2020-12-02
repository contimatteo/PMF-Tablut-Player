import random
import traceback

import fpm_tablut_player.configs as CONFIGS
from fpm_tablut_player.libraries import GameNode, GameState
from fpm_tablut_player.utils import DebugUtils, GameUtils


###

ESCAPE_CELLS: list = GameUtils.getEscapeCells()
CAMP_CELLS: list = GameUtils.getCampCells()
THRONE_CELL: tuple = (GameUtils.getThroneCells())[0]

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
    def __computeNearstPositionForEscape(currentState: GameState, escape: tuple, point: tuple) -> dict:
        distance = 0
        nearestPoint = None
        info = {}

        if escape[0] == point[0]:
            direction = "positive"
            if point[1] > escape[1]:
                direction = "negative"
            offset = abs(point[1]-escape[1])-1
            for i in range(offset):
                if direction == "positive":
                    if currentState.state[(escape[0], point[1]+(i+1))] == "EMPTY":
                        distance += 1
                        nearestPoint = (escape[0], point[1]+(i+1))
                    else:
                        break
                else:
                    if currentState.state[(escape[0], point[1]-(i+1))] == "EMPTY":
                        distance += 1
                        nearestPoint = (escape[0], point[1]-(i+1))
                    else:
                        break

        elif escape[1] == point[1]:
            direction = "positive"
            if point[0] > escape[0]:
                direction = "negative"
            offset = abs(point[0]-escape[0])-1
            for i in range(offset):
                if direction == "positive":
                    if currentState.state[(point[0]+(i+1), escape[1])] == "EMPTY":
                        distance += 1
                        nearestPoint = (point[0]+(i+1), escape[1])
                    else:
                        break
                else:
                    if currentState.state[(point[0]-(i+1), escape[1])] == "EMPTY":
                        distance += 1
                        nearestPoint = (point[0]-(i+1), escape[1])
                    else:
                        break
        info["escape"] = escape
        info["distance"] = distance
        info["nearestPoint"] = nearestPoint

        info["adjacent"] = False

        if nearestPoint is not None and escape[0] == point[0] and (escape[1] == nearestPoint[1]+1 or escape[1] == nearestPoint[1]-1):
            info["adjacent"] = True
        elif nearestPoint is not None and escape[1] == point[1] and (escape[0] == nearestPoint[0]+1 or escape[0] == nearestPoint[0]-1):
            info["adjacent"] = True
        return info

    @staticmethod
    def __kingNearTheEscapes(currentState: GameState) -> list:

        king = currentState.King
        escapeInfoList = []

        for escape in ESCAPE_CELLS:
            if escape[0] == king[0] or escape[1] == king[1]:
                info = CustomHeuristic.__computeNearstPositionForEscape(currentState, escape, king)
                escapeInfoList.append(info)

        return escapeInfoList

    @staticmethod
    def __getPlayablePawns(currentState: GameState) -> int:
        if currentState.turn == "black":
            return currentState.BlackNumber
        return currentState.WhiteNumber

    @staticmethod
    def __computeNeighbour(currentState: GameState, neighbourood: dict, coordinate: tuple):
        if currentState.state[coordinate] == "WHITE":
            neighbourood["white"] += 1
        elif currentState.state[coordinate] == "BLACK":
            neighbourood["black"] += 1
        elif coordinate in ESCAPE_CELLS:
            neighbourood["escape"] += 1
        elif coordinate in CAMP_CELLS or coordinate == THRONE_CELL:
            neighbourood["obstacle"] += 1

    @staticmethod
    def __PawnsNearTheKing(currentState: GameState):

        neighbourood = {}
        neighbourood["white"] = 0
        neighbourood["black"] = 0
        neighbourood["obstacle"] = 0  # throne or camp
        neighbourood["escape"] = 0

        king = currentState.King

        CustomHeuristic.__computeNeighbour(currentState, neighbourood, (king[0], king[1]+1))
        CustomHeuristic.__computeNeighbour(currentState, neighbourood, (king[0], king[1]-1))
        CustomHeuristic.__computeNeighbour(currentState, neighbourood, (king[0]+1, king[1]))
        CustomHeuristic.__computeNeighbour(currentState, neighbourood, (king[0]-1, king[1]))
        return neighbourood

    @staticmethod
    def __getNumberOfKills(currentState: GameState) -> int:
        return len(currentState.FinalDeaths)

    @staticmethod
    def __computeForBlack(currentState: GameState):
        #
        # TODO: missing ...
        #
        pass

    @staticmethod
    def __showGame(board):
        B = list(board)
        row_str = ""

        OKBLUE = '\033[94m'
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

    @staticmethod
    def __computeForWhite(currentState: GameState):

        DebugUtils.info("HEURISTIC DATA FOR {}", [currentState.turn.upper()])
        DebugUtils.space()
        DebugUtils.space()

        DebugUtils.info("PLAYABLE PAWNS: {}", [CustomHeuristic.__getPlayablePawns(currentState)])
        DebugUtils.info("KILL: {}", [CustomHeuristic.__getNumberOfKills(currentState)])
        DebugUtils.space()

        kingNeighbour = CustomHeuristic.__PawnsNearTheKing(currentState)

        DebugUtils.info("KING DATA {}:", [currentState.King])
        DebugUtils.info("   => NEIGHBOUROOD:", [])
        DebugUtils.space()
        DebugUtils.info("       => BLACK: {}", [kingNeighbour["black"]])
        DebugUtils.info("       => WHITE: {}", [kingNeighbour["white"]])
        DebugUtils.info("       => ESCAPE: {}", [kingNeighbour["escape"]])
        DebugUtils.info("       => OBSTACLE: {}", [kingNeighbour["obstacle"]])

        DebugUtils.space()
        DebugUtils.info("   => CLOSING ESCAPE INFO :", [])

        closeEscapesInfoList = CustomHeuristic.__kingNearTheEscapes(currentState)

        for escapeInfo in closeEscapesInfoList:
            DebugUtils.space()
            DebugUtils.info("       => ESCAPE {}", [escapeInfo["escape"]])
            DebugUtils.info("           => DISTANCE {}", [escapeInfo["distance"]])
            DebugUtils.info("           => NEAREST SHIFT {}", [escapeInfo["nearestPoint"]])
            DebugUtils.info("           => NEAREST SHIFT IS ADJACENT {}", [escapeInfo["adjacent"]])

    ###

    # @staticmethod
    # def assignValue(initialState: GameState, node: GameNode):
    #     value: int = 0
    #     currentState = None
    #     my_player_role = GameUtils.turnToString(CONFIGS.APP_ROLE)
    #
    #     try:
    #         currentState = GameState().createFromMoves(initialState, node.moves)
    #     except Exception as error:
    #         if error.__class__.__name__ == "WhiteWinsException":
    #             if my_player_role == "white":
    #                 value = 1000000
    #             else:
    #                 value = -1000000
    #         elif error.__class__.__name__ == "BlackWinsException":
    #             if my_player_role == "white":
    #                 value = -1000000
    #             else:
    #                 value = 1000000
    #         else:
    #             value = 0
    #
    #     # ########################################
    #     # TODO: [@contimatteo] remove this logic #
    #     value = random.randint(1, 101)
    #     # ########################################
    #
    #     node.heuristic = value

    @staticmethod
    def assignValue(initialState: GameState, node: GameNode, deb: int):
        traceback.print_stack()
        DebugUtils.space()
        DebugUtils.space()
        DebugUtils.space()
        DebugUtils.space()
        DebugUtils.info("DEBUG: {}", [deb])
        board = [["EMPTY", "EMPTY", "EMPTY", "EMPTY", "BLACK", "BLACK", "EMPTY", "EMPTY", "EMPTY"],
                 ["EMPTY", "EMPTY", "EMPTY", "EMPTY", "EMPTY", "EMPTY", "EMPTY", "EMPTY", "EMPTY"],
                 ["EMPTY", "EMPTY", "EMPTY", "BLACK", "WHITE", "BLACK", "EMPTY", "EMPTY", "EMPTY"],
                 ["BLACK", "EMPTY", "EMPTY", "EMPTY", "WHITE", "EMPTY", "EMPTY", "EMPTY", "BLACK"],
                 ["BLACK", "BLACK", "WHITE", "WHITE", "THRONE", "WHITE", "WHITE", "BLACK", "BLACK"],
                 ["BLACK", "EMPTY", "EMPTY", "EMPTY", "WHITE", "KING", "EMPTY", "EMPTY", "BLACK"],
                 ["EMPTY", "EMPTY", "EMPTY", "EMPTY", "WHITE", "EMPTY", "EMPTY", "EMPTY", "EMPTY"],
                 ["EMPTY", "EMPTY", "EMPTY", "EMPTY", "BLACK", "EMPTY", "EMPTY", "EMPTY", "EMPTY"],
                 ["EMPTY", "EMPTY", "EMPTY", "BLACK", "BLACK", "BLACK", "EMPTY", "EMPTY", "EMPTY"],
                 ]

        initialServerState = {"board": board, "turn": "WHITE"}
        moves = [{'from': (4, 6), 'to': (2, 6)}]

        initialGameState = GameState().createFromServerState(initialServerState)
        #moves = initialGameState.getPossibleMoves("white")

        # for move in moves:
        #    print(move)

        #print("MOVES ",len(moves),"\n\n")
        currentState = GameState().createFromMoves(initialGameState, moves)
        CustomHeuristic.__showGame(currentState.state)
        currentState.turn = "white"
        CustomHeuristic.__computeForWhite(currentState)
        DebugUtils.space()
        DebugUtils.space()
        DebugUtils.info("-------_____-------------______", [])

        #currentState = GameState().createFromMoves(initialState, node.moves)

        # if node.turn == "white":
        #    CustomHeuristic.__computeForWhite(currentState)
        # else:
        #    CustomHeuristic.__computeForBlack(currentState)

        # ########################################
        # TODO: [@contimatteo] remove this logic #
        #node.heuristic = random.randint(1, 101)  #
        # ########################################


###

if __name__ == "__main__":
    CustomHeuristic.assignValue(None, None, 1)

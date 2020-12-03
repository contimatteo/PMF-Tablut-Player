import random
import traceback

import fpm_tablut_player.configs as CONFIGS
from fpm_tablut_player.libraries import GameNode, GameState
from fpm_tablut_player.utils import DebugUtils, GameUtils


###

ESCAPE_CELLS: list = GameUtils.getEscapeCells()
CAMP_CELLS: list = GameUtils.getCampCells()
THRONE_CELL: tuple = (GameUtils.getThroneCells())[0]
MAX_HEURISITC_VALUE: int = 10000
MIN_HEURISITC_VALUE: int = -10000

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
    def __computeNearstPositionForPoint(currentState: GameState, mainPoint: tuple, point: tuple) -> dict:
        distance = 0
        nearestPoint = None
        info = {}

        if mainPoint[0] == point[0]:
            direction = "positive"
            if point[1] > mainPoint[1]:
                direction = "negative"
            offset = abs(point[1]-mainPoint[1])-1
            if offset == 0:
                nearestPoint = point
            else:
                for i in range(offset):
                    if direction == "positive":
                        if currentState.state[(mainPoint[0], point[1]+(i+1))] == "EMPTY":
                            distance += 1
                            nearestPoint = (mainPoint[0], point[1]+(i+1))
                        else:
                            break
                    else:
                        if currentState.state[(mainPoint[0], point[1]-(i+1))] == "EMPTY":
                            distance += 1
                            nearestPoint = (mainPoint[0], point[1]-(i+1))
                        else:
                            break

        elif mainPoint[1] == point[1]:
            direction = "positive"
            if point[0] > mainPoint[0]:
                direction = "negative"
            offset = abs(point[0]-mainPoint[0])-1
            if offset == 0:
                nearestPoint = point
            else:
                for i in range(offset):
                    if direction == "positive":
                        if currentState.state[(point[0]+(i+1), mainPoint[1])] == "EMPTY":
                            distance += 1
                            nearestPoint = (point[0]+(i+1), mainPoint[1])
                        else:
                            break
                    else:
                        if currentState.state[(point[0]-(i+1), mainPoint[1])] == "EMPTY":
                            distance += 1
                            nearestPoint = (point[0]-(i+1), mainPoint[1])
                        else:
                            break
        info["mainPoint"] = mainPoint
        info["distance"] = distance
        info["nearestPoint"] = nearestPoint

        info["adjacent"] = False

        if nearestPoint is not None and mainPoint[0] == point[0] and (mainPoint[1] == nearestPoint[1]+1 or mainPoint[1] == nearestPoint[1]-1):
            info["adjacent"] = True
        elif nearestPoint is not None and mainPoint[1] == point[1] and (mainPoint[0] == nearestPoint[0]+1 or mainPoint[0] == nearestPoint[0]-1):
            info["adjacent"] = True
        return info

    @staticmethod
    def __kingNearTheEscapes(currentState: GameState) -> list:

        king = currentState.King
        escapeInfoList = []

        for escape in ESCAPE_CELLS:
            if currentState.state[escape] == "EMPTY" and (escape[0] == king[0] or escape[1] == king[1]):
                info = CustomHeuristic.__computeNearstPositionForPoint(currentState, escape, king)
                escapeInfoList.append(info)

        return escapeInfoList

    @staticmethod
    def __BlacksCloseToTheKing(currentState: GameState):
        numberOfBlack = 0
        distanceSum = 0
        for black in currentState.BlackList:
            if currentState.King[0] == black[0] or currentState.King[1] == black[1]:
                info = CustomHeuristic.__computeNearstPositionForPoint(
                    currentState, black, currentState.King)
                if info["adjacent"] == True:
                    numberOfBlack += 1
                else:
                    distanceSum += info["distance"]
        return {"closedBlack": numberOfBlack, "sumDistances": distanceSum}

    @staticmethod
    def __getPlayablePawns(currentState: GameState) -> int:
        if currentState.turn == "black":
            return currentState.BlackNumber
        return currentState.WhiteNumber

    @staticmethod
    def __getPlayableEnemyPawns(currentState: GameState) -> int:
        if currentState.turn == "black":
            return currentState.WhiteNumber
        return currentState.BlackNumber

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
    def __computeForBlack(currentState: GameState) -> int:
        heuristicValue = 0

        closedEscapeValue = 0
        closeEscapesInfoList = CustomHeuristic.__kingNearTheEscapes(currentState)
        DebugUtils.info("ESCAPES:\n{}\n", [closeEscapesInfoList])
        for escapeInfo in closeEscapesInfoList:
            DebugUtils.info("THERE IS A CLOSE ESCAPE", [])
            if escapeInfo["adjacent"] == True:
                heuristicValue = MAX_HEURISITC_VALUE
                break
            else:
                closedEscapeValue += (9-escapeInfo["distance"])

        if heuristicValue >= MAX_HEURISITC_VALUE:
            numberOfBlack = CustomHeuristic.__getPlayableEnemyPawns(currentState)
            numberOfWhite = CustomHeuristic.__getPlayablePawns(currentState)
            numberOfkill = CustomHeuristic.__getNumberOfKills(currentState)
            kingObstacles = CustomHeuristic.__PawnsNearTheKing(currentState)["obstacle"]
            blacksClosedToKingInfo = CustomHeuristic.__BlacksCloseToTheKing(currentState)

            kingDangerFactor = blacksClosedToKingInfo["closedBlack"] * \
                blacksClosedToKingInfo["sumDistances"]

            heuristicValue = numberOfBlack-numberOfWhite+numberOfkill - \
                closedEscapeValue+kingDangerFactor+kingObstacles
        return heuristicValue

    @staticmethod
    def __computeForWhite(currentState: GameState) -> int:

        # DebugUtils.info("HEURISTIC DATA FOR {}", [currentState.turn.upper()])
        # DebugUtils.space()
        # DebugUtils.space()
        #
        # DebugUtils.info("PLAYABLE PAWNS: {}", [CustomHeuristic.__getPlayablePawns(currentState)])
        # DebugUtils.info("KILL: {}", [CustomHeuristic.__getNumberOfKills(currentState)])
        # DebugUtils.space()
        #
        # kingNeighbour = CustomHeuristic.__PawnsNearTheKing(currentState)
        # blacksClosed = CustomHeuristic.__BlacksCloseToTheKing(currentState)
        #
        # DebugUtils.info("KING DATA {}:", [currentState.King])
        # DebugUtils.info("   => CLOSED BLACKS: {}",[blacksClosed])
        # DebugUtils.info("   => NEIGHBOUROOD:", [])
        # DebugUtils.space()
        # DebugUtils.info("       => BLACK: {}", [kingNeighbour["black"]])
        # DebugUtils.info("       => WHITE: {}", [kingNeighbour["white"]])
        # DebugUtils.info("       => ESCAPE: {}", [kingNeighbour["escape"]])
        # DebugUtils.info("       => OBSTACLE: {}", [kingNeighbour["obstacle"]])
        #
        # DebugUtils.space()
        # DebugUtils.info("   => CLOSING ESCAPE INFO :", [])
        #
        # closeEscapesInfoList = CustomHeuristic.__kingNearTheEscapes(currentState)
        #
        # for escapeInfo in closeEscapesInfoList:
        #     DebugUtils.space()
        #     DebugUtils.info("       => ESCAPE {}", [escapeInfo["mainPoint"]])
        #     DebugUtils.info("           => DISTANCE {}", [escapeInfo["distance"]])
        #     DebugUtils.info("           => NEAREST SHIFT {}", [escapeInfo["nearestPoint"]])
        #     DebugUtils.info("           => NEAREST SHIFT IS ADJACENT {}", [escapeInfo["adjacent"]])

        heuristicValue = 0

        closedEscapeValue = 0
        closeEscapesInfoList = CustomHeuristic.__kingNearTheEscapes(currentState)
        for escapeInfo in closeEscapesInfoList:
            DebugUtils.info("ESCAPE: {}", [str(escapeInfo)])
            if escapeInfo["adjacent"] == True:
                #DebugUtils.info("KING PROSSIMO AD USCIRE",[])
                heuristicValue = MAX_HEURISITC_VALUE
                break
            elif escapeInfo["distance"] > 0:
                closedEscapeValue += (9-escapeInfo["distance"])

        if heuristicValue < MAX_HEURISITC_VALUE:
            numberOfBlack = CustomHeuristic.__getPlayableEnemyPawns(currentState)
            numberOfWhite = CustomHeuristic.__getPlayablePawns(currentState)
            numberOfkill = CustomHeuristic.__getNumberOfKills(currentState)
            kingObstacles = CustomHeuristic.__PawnsNearTheKing(currentState)["obstacle"]
            blacksClosedToKingInfo = CustomHeuristic.__BlacksCloseToTheKing(currentState)

            kingDangerFactor = blacksClosedToKingInfo["closedBlack"] * \
                blacksClosedToKingInfo["sumDistances"]
            DebugUtils.info("WHITE: {}", [numberOfWhite])
            DebugUtils.info("BLACK: {}", [numberOfBlack])
            DebugUtils.info("KILL: {}", [numberOfkill])
            DebugUtils.info("CLOSED ESCAPE VALUE: {}", [closedEscapeValue])
            DebugUtils.info("KING IN DANGER FACTOR: {}", [kingDangerFactor])
            DebugUtils.info("KING OBSTACLES {}", [kingObstacles])
            heuristicValue = numberOfWhite-numberOfBlack+numberOfkill + \
                closedEscapeValue-kingDangerFactor-kingObstacles

        DebugUtils.info("HEURISTIC VALUE: {}", [heuristicValue])
        return heuristicValue

    ###

    @staticmethod
    def assignValue(initialState: GameState, node: GameNode):
        value: int = None
        currentState = None
        my_player_role = GameUtils.turnToString(CONFIGS.APP_ROLE)

        # #################################################################################
        # TODO: [@francesco] remove this ...
        node.moves = [{'from': (4, 6), 'to': (2, 6)}]
        board = [
            ["EMPTY", "EMPTY", "EMPTY", "EMPTY", "BLACK", "BLACK", "EMPTY", "EMPTY", "EMPTY"],
            ["EMPTY", "EMPTY", "EMPTY", "EMPTY", "EMPTY", "EMPTY", "BLACK", "EMPTY", "EMPTY"],
            ["EMPTY", "EMPTY", "EMPTY", "BLACK", "WHITE", "EMPTY", "EMPTY", "WHITE", "EMPTY"],
            ["BLACK", "EMPTY", "EMPTY", "EMPTY", "WHITE", "EMPTY", "EMPTY", "KING", "BLACK"],
            ["BLACK", "BLACK", "EMPTY", "WHITE", "THRONE", "EMPTY", "WHITE", "BLACK", "BLACK"],
            ["BLACK", "EMPTY", "EMPTY", "EMPTY", "WHITE", "EMPTY", "EMPTY", "EMPTY", "BLACK"],
            ["EMPTY", "EMPTY", "EMPTY", "EMPTY", "WHITE", "BLACK", "EMPTY", "EMPTY", "EMPTY"],
            ["EMPTY", "EMPTY", "EMPTY", "EMPTY", "EMPTY", "EMPTY", "EMPTY", "EMPTY", "EMPTY"],
            ["EMPTY", "EMPTY", "EMPTY", "BLACK", "BLACK", "EMPTY", "WHITE", "EMPTY", "EMPTY"],
        ]
        initialServerState = {"board": board, "turn": "WHITE"}
        initialState = GameState().createFromServerState(initialServerState)
        # #################################################################################

        try:
            #
            currentState = GameState().createFromMoves(initialState, node.moves)

            # #################################################################################
            # TODO: [@francesco] remove this ...
            CustomHeuristic.__showGame(currentState.state)
            currentState.turn = "white"
            # #################################################################################

            #
            value = CustomHeuristic.__computeForWhite(currentState)
        except Exception as error:
            if error.__class__.__name__ == "WhiteWinsException":
                if my_player_role == "white":
                    value = MAX_HEURISITC_VALUE
                else:
                    value = MIN_HEURISITC_VALUE
            elif error.__class__.__name__ == "BlackWinsException":
                if my_player_role == "white":
                    value = MIN_HEURISITC_VALUE
                else:
                    value = MAX_HEURISITC_VALUE
            else:
                value = 0

        #
        node.heuristic = value

###

    # @staticmethod
    # def assignValue(initialState: GameState, node: GameNode, deb: int = 0):
    #     traceback.print_stack()
    #     DebugUtils.space()
    #     DebugUtils.space()
    #     DebugUtils.space()
    #     DebugUtils.space()
    #     DebugUtils.info("DEBUG: {}", [deb])
    #     board = [["EMPTY", "EMPTY", "EMPTY", "EMPTY", "BLACK", "BLACK", "EMPTY", "EMPTY", "EMPTY"],
    #              ["EMPTY", "EMPTY", "EMPTY", "EMPTY", "EMPTY", "EMPTY", "EMPTY", "EMPTY", "EMPTY"],
    #              ["EMPTY", "EMPTY", "EMPTY", "BLACK", "WHITE", "BLACK", "EMPTY", "EMPTY", "EMPTY"],
    #              ["BLACK", "EMPTY", "EMPTY", "EMPTY", "WHITE", "EMPTY", "EMPTY", "EMPTY", "BLACK"],
    #              ["BLACK", "BLACK", "WHITE", "WHITE", "THRONE", "WHITE", "WHITE", "BLACK", "BLACK"],
    #              ["BLACK", "EMPTY", "EMPTY", "EMPTY", "WHITE", "KING", "EMPTY", "EMPTY", "BLACK"],
    #              ["EMPTY", "EMPTY", "EMPTY", "EMPTY", "WHITE", "EMPTY", "EMPTY", "EMPTY", "EMPTY"],
    #              ["EMPTY", "EMPTY", "EMPTY", "EMPTY", "BLACK", "EMPTY", "EMPTY", "EMPTY", "EMPTY"],
    #              ["EMPTY", "EMPTY", "EMPTY", "BLACK", "BLACK", "BLACK", "EMPTY", "EMPTY", "EMPTY"],
    #              ]

    #     initialServerState = {"board": board, "turn": "WHITE"}
    #     moves = [{'from': (4, 6), 'to': (2, 6)}]

    #     initialGameState = GameState().createFromServerState(initialServerState)
    #     #moves = initialGameState.getPossibleMoves("white")

    #     # for move in moves:
    #     #    print(move)

    #     #print("MOVES ",len(moves),"\n\n")
    #     currentState = GameState().createFromMoves(initialGameState, moves)
    #     CustomHeuristic.__showGame(currentState.state)
    #     currentState.turn = "white"
    #     CustomHeuristic.__computeForWhite(currentState)
    #     DebugUtils.space()
    #     DebugUtils.space()
    #     DebugUtils.info("-------_____-------------______", [])

    #     #currentState = GameState().createFromMoves(initialState, node.moves)

    #     # if node.turn == "white":
    #     #    CustomHeuristic.__computeForWhite(currentState)
    #     # else:
    #     #    CustomHeuristic.__computeForBlack(currentState)

    #     # ########################################
    #     # TODO: [@contimatteo] remove this logic #
    #     #node.heuristic = random.randint(1, 101)  #
    #     # ########################################


###

if __name__ == "__main__":
    CustomHeuristic.assignValue(None, None)

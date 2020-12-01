import random

from fpm_tablut_player.libraries import GameTree, GameNode, GameState
from fpm_tablut_player.utils import DebugUtils
from fpm_tablut_player.heuristics import Heuristic


###


class CustomHeuristic(Heuristic):
    State: GameState
    Escapes: list

    def __init__(self):
        self.Escapes=[(1,0),(2,0),(6,0),(7,0),
                     (0,1),(0,2),(0,6),(0,7),
                     (1,8),(2,8),(6,8),(7,8),
                     (8,1),(8,2),(8,6),(8,7)]


    def iskingAlive(self) ->bool:
        return self.State.King is not None

    def isKingOnEscapeArea(self) ->bool:
        found=False
        for escape in self.Escapes:
            if escape == self.State.King:
                found=True
                break
        return found

    #def kingIsNearTheEscape(self):

    def getPlayablePawns(self,turn: str) ->int:
        if turn == "black":
            return self.State.BlackNumber
        return self.State.WhiteNumber
    
    #def blackPawnNearTheKing(self):
    #def getNumberOfKills(self) ->int:


    def assignValue(self, node: GameNode, initialState: GameState):
        self.state=GameState().createfromGameNode(initialState, node)
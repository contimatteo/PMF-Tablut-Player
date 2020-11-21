###


class GameMove:
    def __init__(self):
        self.fromCell = ""
        self.toCell = ""

    def __export(self):
        return {
            "from": self.fromCell,
            "to": self.fromCell
        }

    def compute(self, currentState: GameState, stateToReach: GameState):
        ### ...
        ### missing code
        ### ...

        self.fromCell = "a1"
        self.toCell = "a2"

        return self.__export()

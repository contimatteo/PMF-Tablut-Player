from fpm_tablut_player.network import SocketManager as SocketManagerClass
from fpm_tablut_player.utils import DebugUtils


###


class Game():
    SocketManager: SocketManagerClass

    def __init__(self):
        self.SocketManager = SocketManagerClass()

    def start(self):
        DebugUtils.space()
        initial_state = self.SocketManager.initialize()

        DebugUtils.info("initial state = {}", [initial_state])

        DebugUtils.space()
        self.SocketManager.listen()

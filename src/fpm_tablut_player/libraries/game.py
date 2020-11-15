from fpm_tablut_player.network import SocketManager as SocketManagerClass

###

class Game():
    SocketManager: SocketManagerClass

    def __init__(self):
        super(Game, self).__init__()
        #
        self.SocketManager = SocketManagerClass()

    def initialize(self):
        self.SocketManager.connect()

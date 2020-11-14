###

class _ProcessConfig(dict):
    HOST: str
    PORT: int

CLIENT = _ProcessConfig()
SERVER = _ProcessConfig()

###

APP_DEBUG = False

CLIENT.HOST = '127.0.0.1'
CLIENT.PORT = 5000

PLAYER_NAME = "FPM"
PLAYER_ROLE = None
PLAYER_ROLE_BLACK_ID = "black"
PLAYER_ROLE_WHITE_ID = "white"

SERVER.HOST = None
SERVER.PORT = None

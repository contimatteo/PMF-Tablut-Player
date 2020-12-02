###

_PLAYER_NAME: str = "FPM"
_PLAYER_ROLE_BLACK_ID: str = "black"
_PLAYER_ROLE_WHITE_ID: str = "white"

_SOCKET_WHITE_PLAYER_PORT: int = 5800
_SOCKET_BLACK_PLAYER_PORT: int = 5801

_APP_COMPUTATION_TIME_NEEDED_PERCENTAGE: float = 11/12

_GAME_TREE_MAX_DEPTH: int = 3

_PARALLEL_THREADS_NUMBER: int = 1

###

APP_DEBUG: bool = True
APP_ROLE: str = None

SERVER_HOST: str = '127.0.0.1'
SERVER_PORT: int = None
SERVER_ROLE: str = None

GAME_MOVE_TIMEOUT: float = 60.0
GAME_TREE_GENERATION_TIMEOUT: float = None

K: int = 1

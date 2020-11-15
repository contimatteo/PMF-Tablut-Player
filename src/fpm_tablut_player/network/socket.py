import socket
import fpm_tablut_player.configs as CONFIGS
from fpm_tablut_player.utils import DebugUtils,NetworkUtils

###

class SocketHelper:
    @staticmethod
    def read_int():
        return None

###

class SocketManager:
    socket: socket.socket

    def __connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        self.socket.connect((CONFIGS.SERVER_HOST, CONFIGS.SERVER_PORT))

    def connect(self):
        DebugUtils.space()
        #
        try:
            self.__connect()
            DebugUtils.info("connection with server estabilished.", [])
            self.send(CONFIGS._PLAYER_NAME)
            DebugUtils.info("name sent successfully.", [])
        except ConnectionRefusedError as e:
            DebugUtils.error("ConnectionRefusedError -> {}", [str(e)])
        except Exception as e:
            DebugUtils.error("Exception -> {}", [str(e)])
        finally:
            self.disconnect()
        #
        DebugUtils.space()

    def disconnect(self):
        self.socket.close()

    def send(self, string: str):
        bytes_sent = self.socket.send(NetworkUtils.integer_request(len(string)))
        if not NetworkUtils.is_value_sent(bytes_sent, 4):
            raise Exception('Socket: error generated while sending the string length.')

        bytes_sent = self.socket.send(NetworkUtils.string_request(string))
        if not NetworkUtils.is_value_sent(bytes_sent, len(string)):
            raise Exception('Socket: error generated while sending the string.')

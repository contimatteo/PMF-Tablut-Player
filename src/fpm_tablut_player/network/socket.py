import socket
import json
import fpm_tablut_player.configs as CONFIGS

from fpm_tablut_player.utils import DebugUtils, NetworkUtils


###


INTEGER_MESSAGE_SIZE = 4


###


class SocketManager:
    socket: socket.socket

    ###

    def __connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        self.socket.connect((CONFIGS.SERVER_HOST, CONFIGS.SERVER_PORT))

    def __disconnect(self):
        self.socket.close()

    def __is_connected(self):
        return self.socket or self.socket.fileno() != -1

    def __send_raw(self, string: str):
        bytes_sent = self.socket.send(NetworkUtils.integer_request(len(string)))
        if not NetworkUtils.is_value_sent(bytes_sent, INTEGER_MESSAGE_SIZE):
            raise Exception('Socket: error generated while sending the string length.')

        bytes_sent = self.socket.send(NetworkUtils.string_request(string))
        if not NetworkUtils.is_value_sent(bytes_sent, len(string)):
            raise Exception('Socket: error generated while sending the string.')

    def __read_raw(self):
        message = b''
        while len(message) < INTEGER_MESSAGE_SIZE:
            fragment = self.socket.recv(min(INTEGER_MESSAGE_SIZE - len(message), 2048))
            if fragment == b'':
                raise RuntimeError("socket connection broken")
            if not fragment:
                break
            message += fragment
        #
        message_length = NetworkUtils.integer_response(message)
        raw_string = self.socket.recv(message_length, socket.MSG_WAITALL)
        return NetworkUtils.string_response(raw_string)

    def __handler(self, callback: callable):
        try:
            return callback()
        except ConnectionRefusedError as e:
            DebugUtils.error("ConnectionRefusedError -> {}", [str(e)])
        except Exception as e:
            DebugUtils.error("Exception -> {}", [str(e)])

    def __initialize(self):
        self.__connect()
        DebugUtils.info("connection with server estabilished.", [])
        self.__send_raw(CONFIGS._PLAYER_NAME)
        DebugUtils.info("name sent successfully.", [])
        #
        initial_state = self.read_json()
        return initial_state

    def __listen(self, gameInstance):
        DebugUtils.info("Socket: listening ...", [])
        #
        while self.__is_connected():
            message = self.read_json()
            DebugUtils.info("message -> {}", [str(message)])
            gameInstance.play(message)
        #
        DebugUtils.info("Socket: disconnecting ...", [])
        self.__disconnect()

    ###

    def initialize(self):
        return self.__handler(self.__initialize)

    def listen(self, gameInstance):
        def listen(_): return self.__listen(gameInstance)
        return self.__handler(listen)

    def send_json(self, obj: dict):
        message = json.dumps(obj)
        return self.__send_raw(message)

    def read_json(self):
        message = self.__read_raw()
        return json.loads(message)

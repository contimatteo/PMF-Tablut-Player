import fpm_tablut_player.configs as CONFIGS

###

class DebugUtils:

    @staticmethod
    def space():
        if CONFIGS.APP_DEBUG:
            print(" $ ")

    @staticmethod
    def info(message: str, arguments: list):
        if CONFIGS.APP_DEBUG:
            messageFormatted = message.format(*arguments)
            print(" $ [INFO]  {}".format(messageFormatted))

    @staticmethod
    def error(message: str, arguments: list):
        if CONFIGS.APP_DEBUG:
            messageFormatted = message.format(*arguments)
            print(" $ [ERROR] {}".format(messageFormatted))

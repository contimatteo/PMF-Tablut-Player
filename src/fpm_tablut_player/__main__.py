#!/usr/bin/env python3

import sys
import argparse

import fpm_tablut_player.configs as CONFIGS
from fpm_tablut_player.libraries import Game
from fpm_tablut_player.utils import DebugUtils


###


def __parse_args():
    parser = argparse.ArgumentParser(description='Fpm AI Tablut Player')
    parser.add_argument(
        '--role',
        dest='role',
        choices={CONFIGS._PLAYER_ROLE_BLACK_ID, CONFIGS._PLAYER_ROLE_WHITE_ID},
        help='player role'
    )
    parser.add_argument(
        '--timeout',
        dest='timeout',
        action='store',
        help='move timeout',
        default=CONFIGS.GAME_MOVE_TIMEOUT
    )
    parser.add_argument(
        '--server',
        dest='server',
        action='store',
        help='server ip address',
        default=CONFIGS.SERVER_HOST
    )

    arguments = parser.parse_args()

    if not arguments.role:
        parser.print_help()
        sys.exit()

    if arguments.server:
        CONFIGS.SERVER_HOST = str(arguments.server)
    if arguments.timeout:
        timeout = float(arguments.timeout)
        threshold = float(CONFIGS._GAME_TIMEOUT_SAFEZONE)
        if timeout > 10 and timeout > threshold:
            CONFIGS.GAME_MOVE_TIMEOUT = timeout - 10
        else:
            raise Exception("Timeout argument must be at least {:}".format(threshold))

    CONFIGS.GAME_TREE_GENERATION_TIMEOUT = float(CONFIGS.GAME_MOVE_TIMEOUT)
    CONFIGS.GAME_TREE_GENERATION_TIMEOUT -= float(CONFIGS._GAME_TIMEOUT_SAFEZONE)

    CONFIGS.APP_ROLE = str(arguments.role)

    if CONFIGS.APP_ROLE == CONFIGS._PLAYER_ROLE_BLACK_ID:
        CONFIGS.SERVER_PORT = CONFIGS._SOCKET_BLACK_PLAYER_PORT
    else:
        CONFIGS.SERVER_PORT = CONFIGS._SOCKET_WHITE_PLAYER_PORT

    DebugUtils.space()
    DebugUtils.info("ROLE         =  {}", [CONFIGS.APP_ROLE])
    DebugUtils.info("SERVER_PORT  =  {}", [CONFIGS.SERVER_PORT])
    DebugUtils.space()


###


def entry_point():
    print()
    __parse_args()
    #
    game = Game()
    game.start()
    #
    print()
    sys.exit()


###


if __name__ == "__main__":
    entry_point()

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
        CONFIGS.GAME_MOVE_TIMEOUT = int(arguments.timeout)

    CONFIGS.APP_ROLE = str(arguments.role)

    if CONFIGS.APP_ROLE == CONFIGS._PLAYER_ROLE_BLACK_ID:
        CONFIGS.APP_PORT = CONFIGS._SOCKET_BLACK_PLAYER_PORT
        CONFIGS.SERVER_PORT = CONFIGS._SOCKET_WHITE_PLAYER_PORT
    else:
        CONFIGS.APP_PORT = CONFIGS._SOCKET_WHITE_PLAYER_PORT
        CONFIGS.SERVER_PORT = CONFIGS._SOCKET_BLACK_PLAYER_PORT

    DebugUtils.space()
    DebugUtils.info("ROLE         =  {}", [CONFIGS.APP_ROLE])
    DebugUtils.info("APP_PORT     =  {}", [CONFIGS.APP_PORT])
    DebugUtils.info("SERVER_PORT  =  {}", [CONFIGS.SERVER_PORT])
    DebugUtils.space()

###

def entry_point():
    print()
    __parse_args()
    #
    game = Game()
    game.initialize()
    # 
    print()
    sys.exit()

###

if __name__ == "__main__":
    entry_point()

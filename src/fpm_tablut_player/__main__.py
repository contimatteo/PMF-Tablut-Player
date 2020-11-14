#!/usr/bin/env python3

import sys
import fpm_tablut_player.configs as CONFIG

###

def __parse_args():
    # TODO: missing
    # ...
    return None

def __play():
    # TODO: missing
    # ...
    return None

###

def entry():
    __parse_args()
    print()
    print(" $ CONFIG.APP_DEBUG             =  {}".format(CONFIG.APP_DEBUG))
    print(" $ CONFIG.CLIENT.HOST           =  {}".format(CONFIG.CLIENT.HOST))
    print(" $ CONFIG.CLIENT.PORT           =  {}".format(CONFIG.CLIENT.PORT))
    print(" $ CONFIG.PLAYER_NAME           =  {}".format(CONFIG.PLAYER_NAME))
    print(" $ CONFIG.PLAYER_ROLE           =  {}".format(CONFIG.PLAYER_ROLE))
    print(" $ CONFIG.PLAYER_ROLE_BLACK_ID  =  {}".format(CONFIG.PLAYER_ROLE_BLACK_ID))
    print(" $ CONFIG.PLAYER_ROLE_WHITE_ID  =  {}".format(CONFIG.PLAYER_ROLE_WHITE_ID))
    print(" $ CONFIG.SERVER.HOST           =  {}".format(CONFIG.SERVER.HOST))
    print(" $ CONFIG.SERVER.PORT           =  {}".format(CONFIG.SERVER.PORT))
    print()
    sys.exit()

###

if __name__ == "__main__":
    entry()

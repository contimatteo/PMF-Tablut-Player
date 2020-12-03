#!/bin/bash

SRC_PATH="./"
ENVIRONMENT_PATH="venv"

source "$SRC_PATH"/"$ENVIRONMENT_PATH"/bin/activate

fpm_tablut_player --role $1 --timeout $2 --server $3

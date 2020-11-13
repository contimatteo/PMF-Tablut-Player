#usr/bin/bash

git submodule update --init --recursive --remote

pip install .
pip install -r requirements.txt
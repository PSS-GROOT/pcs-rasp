#!/usr/bin/env bash

if [ "$(uname)" == "Darwin" ]; then
    # Do something under Mac OS X platform
    source venv/bin/activate
elif [ "$(expr substr $(uname -s) 1 5)" == "Linux" ]; then
    # Do something under GNU/Linux platform
    source venv/bin/activate
elif [ "$(expr substr $(uname -s) 1 10)" == "MINGW32_NT" ]; then
    # Do something under 32 bits Windows NT platform
    source venv/scripts/activate
elif [ "$(expr substr $(uname -s) 1 10)" == "MINGW64_NT" ]; then
    # Do something under 64 bits Windows NT platform
    source venv/scripts/activate
fi

# source tc/scripts/activate
python main.py $1
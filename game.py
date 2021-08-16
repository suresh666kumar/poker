#!/usr/bin/python3

import os
import sys
import time
import glob

arg = sys.argv[1]
files=glob.glob("poker_now_log_*.csv")
fn = files[0]    # sys.argv[2]

def get_game(ts):
    found = False
    game_rows = []

    for line in reversed(list(open(fn, "r"))):
        # "-- starting hand #165  (No Limit Texas Hold'em) (dealer: ""Sure @ UaAtW8RyNI"") --",2021-01-24T03:31:01.028Z,161145906103501

        if "Player stacks:" in line:
            started = True
        if "starting hand #" in line:
            if found:
                break;
            else:
                game_rows = []

        game_rows.append(line)
        if ts in line:
            found = True


    for line in game_rows:
        print (line[:-1])
    print ("\n")

if "@" in arg:
    for line in list(open(arg[1:], "r")):
        get_game(line)
else:
    get_game(arg)

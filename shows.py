#!/usr/bin/python3

import os
import sys
import time
import glob

from mycommon import ranks, get_hand, get_hand_index2, get_ts

player = sys.argv[1]
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

    return game_rows


def get_winner_hand(rows):
    hand = "???"
    for row in rows:
        #"""Solo @ RzCBjWQlAv"" collected 320 from pot",2021-08-08T00:56:45.767Z,162838420576701
        if "collected" in row:
            winner = row[3:row.find("@")]

    for row in rows:
        if "shows" in row:
            if winner in row:
                hand = get_hand(row)

    return hand

def get_loser_hand(rows):
    hand = "???"
    for row in rows:
        #"""Solo @ RzCBjWQlAv"" collected 320 from pot",2021-08-08T00:56:45.767Z,162838420576701
        if "collected" in row:
            winner = row[3:row.find("@")]

    for row in rows:
        if "shows" in row:
            if winner in row:
                hand = "???"
            else:
                hand = get_hand(row)

    return hand

for line in list(open(fn, "r")):

    if "shows" in line:
        if player in line:

            game_rows = get_game(line)

            comm = ""
            result = ""
            my_hole = ""
            against = ""
            #other_hole = []
            for row in game_rows:
                if "collected" in row:
                    if player in row:
                        result = "Won "
                    else:
                        result = "Lost"

                #"""Solo @ RzCBjWQlAv"" shows a 9♦, 8♥.",2021-08-08T01:15:07.354Z,162838530735401
                if "shows" in row:
                    hole = get_hand(row)
                    #hole = row[row.find("shows a")+7:row.find('.')]
                    if player in row:
                        my_hole = hole
                    #else:
                    #    other_hole.append(hole)

                #"Flop:  [8♣, 9♣, 8♦]",2021-08-07T23:23:20.773Z,162837860077300

                if "Flop:" in row:
                    comm = row[7:row.find('",')]
                    #print ("comm=" + comm)
                elif "Turn:" in row:
                    comm = row[7:row.find('",')]
                elif "River:" in row:
                    comm = row[8:row.find('",')]

            ndx = get_hand_index2(my_hole)
            ndx2 = 999
            if result == "Lost":
                against = get_winner_hand(game_rows)
            else:
                against = get_loser_hand(game_rows)
            if (against != "???"):
                ndx2 = get_hand_index2(against)

            sys.stdout.write (result + " | " + my_hole + " | " + str(ndx) + " | " + comm)
            sys.stdout.write (" | " + against + " | " + str(ndx2) )

            #for i in range(len(other_hole)):
            #    if i == 0:
            #        sys.stdout.write (" | ")
            #    else:
            #        sys.stdout.write (", ")
            #    ndx = get_hand_index2(other_hole[i])
            #    sys.stdout.write (other_hole[i] + " (" + str(ndx) + ") ")
            print(" | " + get_ts(line))




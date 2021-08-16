#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

import os
import sys
import time

from mycommon import ranks, get_player_index, players, get_hand_index

fn = sys.argv[1]

mylist = []
started = False
amount = 0
max_rank = 169
top = max_rank *.7
min_bet=0
include_blinds=True
bb = ""
sb = ""

if len(sys.argv) > 2:
    top = int(sys.argv[2])

if len(sys.argv) > 3:
    min_bet= int(sys.argv[3])


for line in reversed(list(open(fn, "r"))):
    if "starting hand #" in line:
        started = True
        mylist = []
    elif "Flop:" in line:
        started = False

    #"""Muru @ ckx3tizlZr"" calls 60",2021-02-21T05:06:08.547Z,161388396854800
    #"""Anand @ 5S52ALDt6Y"" calls 60",2021-02-21T05:06:07.642Z,161388396764300
    #"""Sure @ UaAtW8RyNI"" raises to 60",2021-02-21T05:06:03.169Z,161388396317000
    #"""Muru @ ckx3tizlZr"" posts a big blind of 20",2021-02-21T05:05:43.724Z,161388394372506
    #"""Anand @ 5S52ALDt6Y"" posts a small blind of 10",2021-02-21T05:05:43.724Z,161388394372505

    if line.startswith('"""'):
        player = line[line.find('"""')+3:line.find(' @')]
        #player_index = get_player_index(player)

        if "big blind" in line:
            bb = line
        elif "small blind" in line:
            sb = line

        if started and "calls" in line:
            start = line.find('calls')+6
            if "all in" in line:
                end = line.find(' ', start)
            else:
                end = line.find('"', start)
            amount = int(line[start:end])

            if player in bb:
                blind = "BB"
            elif player in sb:
                blind = "SB"
            else:
                blind = ""

            #if blind == "BB" and amount <= min_bet:
            if (blind == "BB" or blind == "SB") and amount == 20:
                amount = 0
                #print "\t" + player + " " + str(amount) + "\t" + bb

            if amount > 0:
                mylist.append({"player":player, "amount":amount, "blind":blind})
                #print "\t" + str(started) + "\t" + player + " amount=" + str(amount) + "\t" + bb + "\t" + line


    if "shows a " in line:
        for e in mylist:
            if e['player'] in line and e['amount'] > 0:
                rank = get_hand_index(line)
                if rank > top:
                    search_str2 = "shows a "
                    start = line.find(search_str2)
                    if start > 0:
                        hand = line[start+ len(search_str2):line.find(".")]

                    sys.stdout.write(player + "\t$" + str(e['amount']) + "\t " + e['blind'] + "\t" + hand + "\t#" + str(rank) + "\n")



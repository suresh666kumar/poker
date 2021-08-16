#!/usr/bin/python

import os
import sys
import time
import calendar
from datetime import datetime, timedelta

max_players = 15
players = []
stacks = []

fn = sys.argv[1]

def get_player_index(player):
    if player not in players:
        players.append(player)
    return players.index(player)

for line in reversed(list(open(fn, "r"))):
    if "Player stacks:" in line:
        tmp = line[line.find(":")+1 : line.find(",")]
        ar = tmp.split("|", 10)

        stack = []
        for i in range(max_players):
            stack.append(-1)
        #print line

        for i in range(len(ar)):
            e = ar[i]
            player = e[e.find('""')+2:e.find('@')-1]
            ###     #1 ""tamil @ osztnXmETR"" (4616)
            amount = e[e.find("(")+1:e.find(")")]

            ndx = get_player_index(player)
            stack[ndx+1] = amount
            time = int(line[-16:-1])/100000
            stack[0] = time

            #print (" " + str(time) + " '" + str(ndx) + "' " + amount + " " + e)
        #print stack
        stacks.append(stack)

sys.stdout.write ('Time')
for i in range(len(players)):
    sys.stdout.write (',' + players[i])
print ('')

starttime=-1
for j in range(0,len(stacks),5):
    stack = stacks[j]
    for i in range(len(players)+1):
        if starttime == -1:
            starttime = stack[0]

        if i == 0:
            sys.stdout.write ( str((stack[0] - starttime)/60) + ',')
        else:
            if stack[i] == -1:
                sys.stdout.write (',')
            else:
                sys.stdout.write (str(stack[i]) + ',')
    print ('')

#print(datetime.fromtimestamp(159877143968101/100000).strftime("%X"))

#1598771439 68 101
#1598846884

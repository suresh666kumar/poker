#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

import os
import sys
import time
import json

from mycommon import ranks, get_player_index, players, get_hand, get_hand_index, get_card1, get_card2, get_hand_index2, get_ts

fn = sys.argv[1]

MAX_PLAYERS=10
mylist = []
comm = ""
aShow=[]
aWhen=[]
aPreBet=[]
pot=0
winner=""
collectedWith=""
ts=""
state = 0
states=['P', 'F', 'T', 'R', 'S', 'E']

for i in range(MAX_PLAYERS):
    aShow.append("")
    aWhen.append("")
    aPreBet.append(0)

def init():
    for i in range(0,MAX_PLAYERS-1):
        aShow[i] = ""
        aWhen[i] = ""
        aPreBet[i] = 0

def get_hand_details():
    details=[]

    for i in range(0,len(players)):
        #print (players[i] + "hand=" + aShow[i] + " pre=" +  str(aPreBet[i]) + " when=" + aWhen[i] )
        show = aShow[i]
        if len(show) > 0:
            rank = "00" + str(get_hand_index2(show))
            detail = "#" + rank[-3:] + " " + show + "(" + str(aPreBet[i])+"/" +  aWhen[i] + ")"
            #print "detail=" + detail
        else:
            detail = ""
        details.append(detail)
    return details

init()
for line in reversed(list(open(fn, "r"))):
    #print line
    if "starting hand" in line:
        if pot > 0:
            details = get_hand_details()
            mylist.append({"board":comm, "with":collectedWith, 'winner':winner, "pot":pot, "details":details, "ts":ts})

        state = 0
        pot = 0
        winner = ""
        comm = ""   # reset community card
        collectedWith=""
        init()

    elif "ending hand" in line:
        state += 1
    elif "joined" in line:
        #"The player ""Sun-ita @ nVTMSlOnCS"" joined the game with a stack of 1000.",2021-08-14T23:42:30.790Z,162898455079002
        player = line[line.find('""')+2:line.find('"" ')]
        player_index = get_player_index(player)

    elif "shows a " in line:
        #"""DNegreanu @ st8V54HQHT"" shows a 2♣, 3♥.",2021-08-15T00:47:18.250Z,162898843825000
        player = line[line.find('"""')+3:line.find('"" ')]

        player_index = get_player_index(player)
        #rank = get_hand_index(line)
        hand = get_hand(line)

        #print "index=" + str(player_index) + " hand=" + hand + " len=" + str(len(aShow))
        aShow[player_index] = hand

    if "Flop:" in line:
        state += 1
        comm = line[7:line.find('",')]
    elif "Turn:" in line:
        state += 1
        comm = line[7:line.find('",')]
    elif "River:" in line:
        state += 1
        comm = line[8:line.find('",')]

    #"""Solo @ RzCBjWQlAv"" collected 3402 from pot with Flush, Ad High (combination: A♦, K♦, 9♦, 8♦, 4♦)",2021-08-15T03:08:12.009Z,162899689200900
    if "collected" in line:
        player = line[3:line.find('"" ')]
        search_str = "collected "
        start = line.find(search_str) + len(search_str);
        end   = line.find(" ", start+1)
        pot = int( line[start:end] )
        ts = get_ts(line)

        if "with" in line:
            collectedWith = line[line.find("with")+5 : line.find("(")]
            #print ("collectedWith=" + collectedWith)

        ndx = get_player_index(player)
        winner = players[ndx]

    elif line.startswith('"""'):

        player = line[line.find('"""')+3:line.find('"" ')]
        player_index = get_player_index(player)

        if not "shows" in line:
            aWhen[player_index] = states[state]

        #"""Shan @ IoFp87uwrl"" raises to 840 and go all in",2021-08-22T00:03:06.084Z,162959058608400

        #"""Solo @ P0EKPjReio"" checks",2021-03-14T07:08:33.354Z,161570571335500
        #"""Anand @ 5S52ALDt6Y"" folds",2021-03-14T07:06:52.555Z,161570561255500
        #"""Shan @ IoFp87uwrl"" raises to 200",2021-03-14T07:06:45.113Z,161570560511800
        #"""Solo @ P0EKPjReio"" calls 20",2021-03-14T07:06:28.422Z,161570558842300
        #"""ray @ 8-2EMBD5GQ"" posts a big blind of 20",2021-03-14T07:06:24.799Z,161570558480410
        #"""Anand @ 5S52ALDt6Y"" posts a small blind of 10",2021-03-14T07:06:24.799Z,161570558480409

        #"""Shan @ IoFp87uwrl"" bets 200",2021-08-22T07:10:48.380Z,162961624838000
        if state == 0:
            if "calls" in line:
                start = line.find('calls')+6
            elif "bets" in line:
                start = line.find('bets')+5
            elif "raises" in line:
                start = line.find('raises')+10
            elif "blind" in line:
                start = line.find(' of')+4
            else:
                start = 0

            if start:
                if "go all in" in line:
                    end = line.find(" and")-4
                else:
                    end = line.find('",')
                bet = line[start:end]
                aPreBet[player_index] = max(aPreBet[player_index] , bet)
            else:
                bet =  ""

sys.stdout.write ("Timestamp | Winner | Pot | With  | Board ")
for player in players:
    sys.stdout.write( " | " + player )
sys.stdout.write("\n")

sep = " | "
for i in range(len(mylist)):
    e = mylist[i]
    sys.stdout.write (e["ts"] + sep + e["winner"] + sep +  str(e["pot"]) + sep + e["with"]+ sep + e["board"]  )
    for detail in e["details"]:
        if len(detail) > 0:
            sys.stdout.write( sep + detail )
        else:
            sys.stdout.write( sep )
    sys.stdout.write("\n")

#print "players=" + str(len(players))

jsonString = json.dumps(mylist)
jsonFile = open("data.json", "w")
jsonFile.write(jsonString)
jsonFile.close()



#actions = ["calls", "raises"]
#if any(x in line for x in actions):

#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

import os
import sys
import time

from mycommon import ranks, get_player_index, players, get_hand, get_hand_index, get_card1, get_card2, get_hand_index2

fn = sys.argv[1]

mylist = []
comm = ""
aShow=[9]
pot=0
winner=""
collectedWith=""

for i in range(9):
    aShow.append("")

for line in reversed(list(open(fn, "r"))):
    if "starting hand" in line:
        if pot > 0:
            mylist.append({"board":comm, "with":collectedWith, 'winner':winner, "pot":pot, "hand":aShow })

        pot=0
        winner=""
        comm = ""   # reset community card
        aShow=[]
        for i in range(9):
            aShow.append("")

    if "joined" in line:
        #"The player ""Sun-ita @ nVTMSlOnCS"" joined the game with a stack of 1000.",2021-08-14T23:42:30.790Z,162898455079002
        player = line[line.find('""')+2:line.find('"" ')]
        player_index = get_player_index(player)

    if "shows a " in line:
        #"""DNegreanu @ st8V54HQHT"" shows a 2♣, 3♥.",2021-08-15T00:47:18.250Z,162898843825000
        player = line[line.find('"""')+3:line.find('"" ')]

        player_index = get_player_index(player)
        #rank = get_hand_index(line)
        hand = get_hand(line)
        aShow[player_index] = hand

        #print ("player="+player + " index="+ str(player_index) + " hand=" + hand)


    #"""Solo @ RzCBjWQlAv"" collected 3402 from pot with Flush, Ad High (combination: A♦, K♦, 9♦, 8♦, 4♦)",2021-08-15T03:08:12.009Z,162899689200900
    if "collected" in line:
        player = line[3:line.find('"" ')]
        search_str = "collected "
        start = line.find(search_str) + len(search_str);
        end   = line.find(" ", start+1)
        pot = int( line[start:end] )

        if "with" in line:
            collectedWith = line[line.find("with")+5 : line.find("(")]
            #print ("collectedWith=" + collectedWith)

        ndx = get_player_index(player)

        rank_index = 999
        search_str2 = "shows a "
        lastShow=""
        #for show in aShow:
        #    if players[ndx] in show:
        #        lastShow = show
        start = lastShow.find(search_str2)
        if start > 0:
            hand = lastShow[start+ len(search_str2):lastShow.find(".")]
            comma = hand.find(",")

            card1  = hand[0:comma-3]
            suite1 = ord(hand[comma-1])

            card2  = hand[comma+2:-3]
            suite2 = ord(hand[len(hand)-1:len(hand)])

            if card1 == "10":
                card1 = "T";
            if card2 == "10":
                card2 = "T";

            if card1 == card2:
                suited = ''
            else:
                if (suite1 == suite2):
                    suited = 's'
                else:
                    suited = 'o'

            myhand = card1+card2+suited

            if myhand in ranks:
                rank_index = ranks.index(card1+card2+suited)+1  # +1 beacuse start index is 0
            else:
                rank_index = ranks.index(card2+card1+suited)+1

        else:
            hand = "???"

        winner = players[ndx]

    if "Flop:" in line:
        comm = line[7:line.find('",')]
    elif "Turn:" in line:
        comm = line[7:line.find('",')]
    elif "River:" in line:
        comm = line[8:line.find('",')]
    #elif "shows a " in line:
    #    aShow.append(line)


sys.stdout.write ("Winner | Pot | With  | Board ")
for player in players:
    sys.stdout.write( " | " + player )
sys.stdout.write("\n")

sep = " | "
for i in range(len(mylist)):
    e = mylist[i]
    sys.stdout.write (e["winner"] + sep +  str(e["pot"]) + sep + e["with"]+ sep + e["board"]  )
    for show in e["hand"]:
        if len(show) > 0:
            rank = "00" + str(get_hand_index2(show))
            sys.stdout.write( " | #" + rank[-3:] + " " + show )
        else:
            sys.stdout.write( " | ")
    sys.stdout.write("\n")


    #print ( str(e['rank']) + sep + str(e['pot']) + sep + e['player'] + sep + e['hand'] + sep + win + sep + e['river'] +sep + ts)

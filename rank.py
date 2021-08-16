#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

import os
import sys
import time

from mycommon import ranks, get_player_index, players

fn = sys.argv[1]

mylist = []
top_half = []
bottom_half = []

for i in range(20):
    top_half.append(0)
    bottom_half.append(0)


comm = ""
aShow=[]

if sys.argv[2] == 'csv':
    top = 169
elif len(sys.argv) > 2:
    top = int(sys.argv[2])

for line in reversed(list(open(fn, "r"))):
    """
    ~""Anand @ 5S52ALDt6Y"" collected 240 from pot with Pair, 9's (combination: 9♥, 9♠, K♠, J♥, 10♦)",2020-10-11T06:03:10.191Z,160239619019301
    ~""Anand @ 5S52ALDt6Y"" shows a 9♥, 10♦.",2020-10-11T06:03:10.191Z,160239619019300

    ~""Muru @ hEzAamWfh1"" collected 200 from pot",2020-10-18T00:44:02.652Z,160298184265301
    ~""Uncalled bet of 100 returned to ""Muru @ hEzAamWfh1~"",2020-10-18T00:44:02.652Z,160298184265300
    """

    if "collected" in line:
        player = line[3:line.find('"" ')]
        search_str = "collected "
        start = line.find(search_str) + len(search_str);
        end   = line.find(" ", start+1)
        pot = int( line[start:end] )

        ndx = get_player_index(player)

        rank_index = 999
        search_str2 = "shows a "
        lastShow=""
        for show in aShow:
            if players[ndx] in show:
                lastShow = show
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

            if rank_index < top:
                top_half[ndx] += 1
            elif rank_index > 169 - top and rank_index < 169:
                bottom_half[ndx] += 1

        else:
            hand = "???"

#        print "rank" + str(rank_index) + " lastShow=" + lastShow + " hand=" + hand + " river=" + comm+ "\t"  + line
        mylist.append({"rank":rank_index, 'player':players[ndx], "pot":pot, "hand":hand, "river":comm, "line":line })
        aShow = []

        #print player + " " + str(rank_index) + " " + str(pot)
        #sys.stdout.write  (("00" + str(rank_index))[-3:] + "\t" + line)
        #print "hand='" + hand +  "' card1='" + card1 + "' card2='" + card2 + "\t" + ("00" + str(rank_index))[-3:]
        #print "hand='" + hand +  "' card1='" + card1 + "' suite1='" + str(suite1) + "' card2='" + card2 + "' suite2='" + str(suite2) + "'"
        #for c in hand:  print str(c) + "\t" + str(ord(c))

    # "River: 4♣, 6♣, A♥, 10♠ [9♥]",2021-01-03T01:34:20.230Z,160963766023600

    if "Flop:" in line:
        comm = line[7:line.find('",')]
    elif "Turn:" in line:
        comm = line[7:line.find('",')]
    elif "River:" in line:
        comm = line[8:line.find('",')]
    elif "starting hand" in line:
        comm = ""   # reset community card
        aShow = []
    elif "shows a " in line:
        aShow.append(line)

def byRank(e):
    return e['rank']

def byPot(e):
    return e['pot']

if sys.argv[2] == 'csv':
    sep = " | "
    mylist.sort(key=byRank)
    for i in range(len(mylist)):
        e = mylist[i]
        #if e['rank'] > -1:
        line = e['line']
        if "with" in line:
            win = line[line.find("with") + 4 : line.find("(")]
        else:
            win = "Uncalled"
        ts = line[-16:-1]
        print ( str(e['rank']) + sep + str(e['pot']) + sep + e['player'] + sep + e['hand'] + sep + win + sep + e['river'] +sep + ts)
else:
    if len(sys.argv) > 2:
        top = int(sys.argv[2])
        if top > len(mylist) or top == 0:
            top = len(mylist)
    else:
        top = len(mylist)

    print "Top "+ str(top) +" win"
    mylist.sort(reverse=True, key=byPot)
    for i in range(top):
        e = mylist[i]
        pot = ("    " + str(e['pot']))[-5:]
        rank = ("  " + str(e['rank']))[-3:]
        sys.stdout.write ( "#" + str(i+1) + " $" + pot + " (#" + rank +")  " + e['line'])


    mylist.sort(key=byRank)
    print
    print "Top "+ str(top) +" Rank"
    count = 0
    for i in range(len(mylist)):
        e = mylist[i]
        if e['rank'] > 0:
            rank = ("00" + str(e['rank']))[-3:]
            sys.stdout.write ("#" + rank + "  " + e['line'])
            count += 1
            if e['rank'] > top:
                break


    if len(sys.argv) > 2:
        mylist.sort(reverse=True, key=byRank)
        print
        print "Bottom "+ str(top) +" Rank"

        count = 0
        for i in range(len(mylist)):
            e = mylist[i]
            if e['rank'] <= 169:
                rank = ("00" + str(e['rank']))[-3:]
                sys.stdout.write ("#" + rank + "  " + e['line'])
                count += 1
                if e['rank'] < top:
                    break

    for i in range(len(players)):
        sys.stdout.write("\t")
        name=players[i] + "__";
        sys.stdout.write (name[0:4] + " ")
    print


    sys.stdout.write ("top")
    for i in range(len(players)):
        sys.stdout.write("\t" + str(top_half[i]))
    sys.stdout.write ("\nbottom")
    for i in range(len(players)):
        sys.stdout.write("\t" + str(bottom_half[i]))
    print

#f.close

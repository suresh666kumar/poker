#!/usr/bin/python

import os
import sys
import time

fn = sys.argv[1]

ranks=["AA","KK","QQ","AKs","JJ","AQs","KQs","AJs","KJs","TT","AKo","ATs","QJs","KTs","QTs","JTs","99","AQo","A9s","KQo","88","K9s","T9s","A8s","Q9s","J9s","AJo","A5s","77","A7s","KJo","A4s","A3s","A6s","QJo","66","K8s","T8s","A2s","98s","J8s","ATo","Q8s","K7s","KTo","55","JTo","87s","QTo","44","33","22","K6s","97s","K5s","76s","T7s","K4s","K3s","K2s","Q7s","86s","65s","J7s","54s","Q6s","75s","96s","Q5s","64s","Q4s","Q3s","T9o","T6s","Q2s","A9o","53s","85s","J6s","J9o","K9o","J5s","Q9o","43s","74s","J4s","J3s","95s","J2s","63s","A8o","52s","T5s","84s","T4s","T3s","42s","T2s","98o","T8o","A5o","A7o","73s","A4o","32s","94s","93s","J8o","A3o","62s","92s","K8o","A6o","87o","Q8o","83s","A2o","82s","97o","72s","76o","K7o","65o","T7o","K6o","86o","54o","K5o","J7o","75o","Q7o","K4o","K3o","96o","K2o","64o","Q6o","53o","85o","T6o","Q5o","43o","Q4o","Q3o","74o","Q2o","J6o","63o","J5o","95o","52o","J4o","J3o","42o","J2o","84o","T5o","T4o","32o","T3o","73o","T2o","62o","94o","93o","92o","83o","82o","72o"]
mylist = []
players =[]
top_half = []
bottom_half = []

for i in range(20):
    top_half.append(0)
    bottom_half.append(0)

def get_player_index(player):
    if player not in players:
        players.append(player)
    return players.index(player)


f = open(fn, "r")
for line in f:
    if "collected" in line:
        player = line[3:line.find(' ')]
        search_str = "collected "
        start = line.find(search_str) + len(search_str);
        end   = line.find(" ", start+1)
        pot = int( line[start:end] )

        ndx = get_player_index(player)

        rank_index = -1
        start = line.find("hand:")
        if start > 0:
            hand = line[start+6:line.find(")")]
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

            if rank_index < 85:  # 169/2
                top_half[ndx] += 1
            else:
                bottom_half[ndx] += 1

        mylist.append({"rank":rank_index, 'player':player, "pot":pot, "line":line })

        #print player + " " + str(rank_index) + " " + str(pot)
        #sys.stdout.write  (("00" + str(rank_index))[-3:] + "\t" + line)
        #print "hand='" + hand +  "' card1='" + card1 + "' card2='" + card2 + "\t" + ("00" + str(rank_index))[-3:]
        #print "hand='" + hand +  "' card1='" + card1 + "' suite1='" + str(suite1) + "' card2='" + card2 + "' suite2='" + str(suite2) + "'"
        #for c in hand:  print str(c) + "\t" + str(ord(c))


def byRank(e):
    return e['rank']

def byPot(e):
    return e['pot']

if sys.argv[2] == 'csv':
    sep = " && "
    mylist.sort(key=byRank)
    for i in range(len(mylist)):
        e = mylist[i]
        if e['rank'] > -1:
            line = e['line']
            hand = line[line.find("with") + 4 : line.find(")")+1]
            ts = line[-16:-1]
            print ( str(e['rank']) + sep + str(e['pot']) + sep + e['player'] + sep + hand + sep + ts)
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
    #for i in range(top):
    count = 0
    for i in range(len(mylist)):
        e = mylist[i]
        if e['rank'] > 0:
            rank = ("00" + str(e['rank']))[-3:]
            sys.stdout.write ("#" + rank + "  " + e['line'])
            count += 1
            if count > top:
                break


    if len(sys.argv) > 2:
        mylist.sort(reverse=True, key=byRank)
        print
        print "Bottom "+ str(top) +" Rank"
        for i in range(top):
            e = mylist[i]
            rank = ("00" + str(e['rank']))[-3:]
            sys.stdout.write ("#" + rank + "  " + e['line'])


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

f.close

#!/usr/bin/python3
# -*- coding: iso-8859-15 -*-

import os
import sys
import time

from mycommon import get_hand_index, is_pair, is_broadway, get_player_index, players, player_ids

max_players = 15
max_rank = 169
print_broadway = False
fn = sys.argv[1]


rflush=[]
sflush=[]
four=[]
full=[]
flush=[]
straight=[]
three=[]
twopair=[]
pair=[]
high=[]
called=[]
uncalled=[]
buyin=[]
checks=[]
calls=[]
bets=[]
raises=[]
folds=[]
allin=[]
pre_fold=[]
pre_raise=[]
total_hands=[]
broadway=[]
top20=[]
bottom20=[]
pocket_pair=[]
empty="          "
hand_vpip=[]
vpip=[]

def add_vpip(player_index):
    if started and hand_vpip[player_index] == 0:
        hand_vpip[player_index] = 1

def print_stat(label,ar):
    total=0
    sys.stdout.write (label)
    for i in range(len(players)):
        #if ar[i] > 0:
        #   sys.stdout.write (" " + players[i] + ":" + str(ar[i]) + ', ')
        tmp = empty+str(ar[i])
        sys.stdout.write ( tmp[-5:] )
        total += ar[i];
        tmp = empty+str(total)
    print ( tmp[-6:] )


for i in range(max_players):
    rflush.append(0)
    sflush.append(0)
    four.append(0)
    full.append(0)
    flush.append(0)
    straight.append(0)
    three.append(0)
    twopair.append(0)
    pair.append(0)
    high.append(0)
    uncalled.append(0)
    called.append(0)
    buyin.append(0)
    checks.append(0)
    calls.append(0)
    bets.append(0)
    raises.append(0)
    folds.append(0)
    allin.append(0)
    pre_fold.append(0)
    pre_raise.append(0)
    total_hands.append(0)
    broadway.append(0)
    top20.append(0)
    bottom20.append(0)
    pocket_pair.append(0)
    hand_vpip.append(0)
    vpip.append(0)

started = False
total = 0
dealer_index = 0
for line in reversed(list(open(fn, "r"))):
    if "starting hand #" in line:
        #"-- starting hand #192  (No Limit Texas Hold'em) (dealer: ""Solo @ P0EKPjReio"") --",2021-03-14T02:36:29.128Z,161568938912900
        #"-- starting hand #272  (No Limit Texas Hold'em) (dead button) --",2021-03-14T04:06:52.247Z,161569481224901
        started = True
        #if "dealer" in line:
        #    dealer = line[line.find('dealer: ')+10:line.find('"" ')]
        #    dealer_index = get_player_index(dealer)
            #print (line)
            #print ("dealer=" + dealer + " index=" + str(dealer_index))
    elif "Flop:" in line:
        started = False
        for i in range(max_players):
            vpip[i] += hand_vpip[i]
            hand_vpip[i] = 0

    if "Player stacks:" in line:
        for i in range(len(players)):
            if player_ids[i] in line:
                total_hands[i] += 1
        total += 1

    #if "approved" in line:
    #    player = line[line.find(' ""')+3:line.find('"" ')]
    #    player_index = get_player_index(player)
    #    amount = int(line[line.find("of ")+3:line.find(".\"") ])
        #print "'" + player + "' " + str(len(players)) + line
    #    buyin[player_index] += amount

    #if line.startswith('"The player'):
    #    player = line[line.find(' ""')+3:line.find('"" ')]
    #    player_index = get_player_index(player)
    #    start = line.find("of ");
    #    if start > -1:
    #        amount = int(line[start+3:line.find(".\"", start) ])
    #        #print player + " " + str(amount)
    #        if "quits" in line:
    #            buyin[player_index] -= amount
    #        elif "approved" in line:
    #            buyin[player_index] += amount

    if "shows a " in line:
        #"""Sunita @ 8YQgQYlyP-"" shows a 8♦, 5♣.",2021-02-21T04:06:03.969Z,161388036397000
        player = line[line.find('"""')+3:line.find('"" ')]
        player_index = get_player_index(player)
        rank = get_hand_index(line)
        if rank < max_rank*0.2:
            top20[player_index] += 1
        elif rank > max_rank*0.8:
            bottom20[player_index] += 1
        if is_pair(line):
            pocket_pair[player_index] += 1
        if is_broadway(line):
            broadway[player_index] += 1
            if print_broadway:
                print(line)

    player_index = -1
    if "collected" in line:
        player = line[3:line.find('"" ')]
        #if player not in players:
        #    players.append(player)
        #player_index = players.index(player)
        player_index = get_player_index(player)

        if "with" in line:
            called[player_index] += 1
            if "Royal Flush" in line:
                rflush[player_index] += 1
            elif "Straight Flush" in line:
                sflush[player_index] += 1
            elif "Four" in line:
                four[player_index] += 1
            elif "Flush" in line:
                flush[player_index]  += 1
            elif "Full House" in line:
                full[player_index] += 1
            elif "Straight" in line:
                straight[player_index] += 1
            elif "Three of a Kind" in line:
                three[player_index] += 1
            elif "Two Pair" in line:
                twopair[player_index] += 1
            elif "with Pair" in line:
                pair[player_index] += 1
            elif "High" in line:
                    high[player_index] += 1
            else:
                print ("Unknown: " + line)
        else:
            uncalled[player_index] += 1


    elif line.startswith('"""'):
        #"""Muru @ ckx3tizlZr"" calls 1210 and go all in",2021-04-25T03:00:16.543Z,161931961654400
        #"""Shan @ IoFp87uwrl"" raises to 1210 and go all in",2021-04-25T03:00:11.699Z,161931961170000

        #"""Solo @ P0EKPjReio"" checks",2021-03-14T07:08:33.354Z,161570571335500
        #"""Anand @ 5S52ALDt6Y"" folds",2021-03-14T07:06:52.555Z,161570561255500
        #"""Shan @ IoFp87uwrl"" raises to 200",2021-03-14T07:06:45.113Z,161570560511800
        #"""Solo @ P0EKPjReio"" calls 20",2021-03-14T07:06:28.422Z,161570558842300
        #"""ray @ 8-2EMBD5GQ"" posts a big blind of 20",2021-03-14T07:06:24.799Z,161570558480410
        #"""Anand @ 5S52ALDt6Y"" posts a small blind of 10",2021-03-14T07:06:24.799Z,161570558480409

        player = line[line.find('"""')+3:line.find('"" ')]
        player_index = get_player_index(player)

        if "big blind" in line:
            bb_player_index = player_index


        if "all in" in line:
            allin[player_index] += 1
            add_vpip(player_index)
        elif "checks" in line:
            checks[player_index] += 1
        elif "calls" in line:
            calls[player_index] += 1
            add_vpip(player_index)
        elif "bets" in line:
            bets[player_index] += 1
            add_vpip(player_index)
        elif "raises" in line:
            raises[player_index] += 1
            if started:
                pre_raise[player_index] += 1
            add_vpip(player_index)
        elif "folds" in line:
            folds[player_index] += 1
            if started:
                pre_fold[player_index] += 1


pre_fold_pct=[]
pfr_pct=[]
vpip_pct=[]
total_pct=[]
#for i in range(len(players)):
#    print (players[i][0:4] + "\t" + str(buyin[i]))

sys.stdout.write("               ")
for i in range(len(players)):
    name=players[i] + "__";
    sys.stdout.write (name[0:4] + " ")
    if (total_hands[i] > 0):
        pct = int((pre_fold[i]) * 100 / total_hands[i])
    else:
        pct = 0;
    pre_fold_pct.append( pct )

    if (total_hands[i] > 0):
        pct = int(pre_raise[i] * 100 / total_hands[i])
    else:
        pct = 0;
    pfr_pct.append( pct )

    if (total_hands[i] > 0):
        pct = int(vpip[i] * 100 / total_hands[i])
    else:
        pct = 0;
    vpip_pct.append( pct )

    if (total_hands[i] > 0):
        pct = int((total_hands[i] - pre_fold[i]) * 100 / total_hands[i])
    else:
        pct = 0;
    total_pct.append( pct )


print ("Total")

print ()
print_stat("pocket_pair   ", pocket_pair)
print_stat("broadway      ", broadway)
print_stat("top 20%       ", top20)
#print_stat("bottom 20     ", bottom20)
print ()
print_stat("StraightFlush ", sflush)
print_stat("Four          ", four)
print_stat("Full House    ", full)
print_stat("Flush         ", flush)
print_stat("Straight      ", straight)
print_stat("Three         ", three)
print_stat("Two Pair      ", twopair)
print_stat("Pair          ", pair)
print_stat("High          ", high)
print_stat("Win w/ Show   ", called)
print_stat("Win No Show   ", uncalled)
print ()
#print_stat("checks        ", checks)
#print_stat("calls         ", calls)
#print_stat("bets          ", bets)
#print_stat("raises        ", raises)
#print_stat("folds         ", folds)
print_stat("all in        ", allin)
print ()
print_stat("preflop raise ", pre_raise)
print_stat("pfr %         ", pfr_pct)
print_stat("vpip          ", vpip)
print_stat("vpip %        ", vpip_pct)
print_stat("preflop_fold  ", pre_fold)
print_stat("preflop_fold %", pre_fold_pct)
print_stat("hands played %", total_pct)
print ()
print_stat("hands total   ", total_hands)


uncalled_total = 0
for unc in uncalled:
    uncalled_total += unc
print ()
print ("Total number of hands " +  str(total) + " (Uncalled " + str(round(uncalled_total*100/total,1)) + "%)")

#grep shows poker_now_log_ldvuJmepdMFOMwXN0wAfm6TyI.csv | grep -E ' A.* A'

#grep Flop  poker_now_log_*.csv  | egrep ", A|: A|\[A" | wc -l
#grep River poker_now_log_*.csv  | egrep ", A|: A|\[A" | wc -l

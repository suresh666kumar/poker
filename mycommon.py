#!/usr/bin/python3
# -*- coding: iso-8859-15 -*-

max_rank = 169
ranks=["AA","KK","QQ","AKs","JJ","AQs","KQs","AJs","KJs","TT","AKo","ATs","QJs","KTs","QTs","JTs","99","AQo","A9s","KQo","88","K9s","T9s","A8s","Q9s","J9s","AJo","A5s","77","A7s","KJo","A4s","A3s","A6s","QJo","66","K8s","T8s","A2s","98s","J8s","ATo","Q8s","K7s","KTo","55","JTo","87s","QTo","44","33","22","K6s","97s","K5s","76s","T7s","K4s","K3s","K2s","Q7s","86s","65s","J7s","54s","Q6s","75s","96s","Q5s","64s","Q4s","Q3s","T9o","T6s","Q2s","A9o","53s","85s","J6s","J9o","K9o","J5s","Q9o","43s","74s","J4s","J3s","95s","J2s","63s","A8o","52s","T5s","84s","T4s","T3s","42s","T2s","98o","T8o","A5o","A7o","73s","A4o","32s","94s","93s","J8o","A3o","62s","92s","K8o","A6o","87o","Q8o","83s","A2o","82s","97o","72s","76o","K7o","65o","T7o","K6o","86o","54o","K5o","J7o","75o","Q7o","K4o","K3o","96o","K2o","64o","Q6o","53o","85o","T6o","Q5o","43o","Q4o","Q3o","74o","Q2o","J6o","63o","J5o","95o","52o","J4o","J3o","42o","J2o","84o","T5o","T4o","32o","T3o","73o","T2o","62o","94o","93o","92o","83o","82o","72o"]


def get_hand(line):
    hand=""
    search_str2 = "shows a "
    start = line.find(search_str2)
    if start > 0:
        hand = line[start+ len(search_str2):line.find(".")]
    return hand

def get_ts(line):
    return line[-16:-1]

def is_pair(line):
    hand = get_hand(line)
    comma = hand.find(",")

    card1  = hand[0:comma-1]
    card2  = hand[comma+2:-1]
    #print ("hand=" + hand + " comma=" + str(comma) + " c1=" + card1 + " c2="+ card2)
    return (card1 == card2)

def is_top5(card):
    ret=0
    if card == "10" or card == "J" or card == "Q" or card == "K" or card == "A":
        ret = 1
    return ret

def is_broadway(line):
    hand = get_hand(line)
    comma = hand.find(",")

    card1  = hand[0:comma-1]
    card2  = hand[comma+2:-1]
    #print ("hand=" + hand + " comma=" + str(comma) + " c1=" + card1 + " c2="+ card2)
    return (is_top5(card1) and is_top5(card2) and (is_pair(line) == False))

def is_suited(line):
    hand = get_hand(line)
    suite1 = ord(hand[comma-1])
    suite2 = ord(hand[len(hand)-1:len(hand)])
    return (suite1 == suite1)


def card_val(card):
    if card == 'A':
        return 1;
    elif card == 'J':
        return 11;
    elif card == 'Q':
        return 12;
    elif card == 'K':
        return 13;
    else:
        return ord(card);


def is_connected(line):
    hand = get_hand(line)
    comma = hand.find(",")

    card1  = hand[0:comma-1]
    card2  = hand[comma+2:-1]
    return (abs(card_val(card1) - card_val(card2)) == 1)


def get_hand_index2(hand):
    rank_index = 0
    comma = hand.find(",")

    if (len(hand) == 0) or comma == -1:
        return rank_index

    card1  = hand[0:comma-1]
    suite1 = ord(hand[comma-1])
    card1 = card1[0]

    card2  = hand[comma+2:-1]
    suite2 = ord(hand[len(hand)-1:len(hand)])
    card2 = card2[0]

    if card1 == "1":    # hack, sometime card1 is more than 2 chars (not 10)
        card1 = "T";
    if card2 == "1":
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
        if card2 != "0":
            rank_index = ranks.index(card2+card1+suited)+1
    return rank_index

def get_hand_index(line):
    hand = get_hand(line)
    return get_hand_index2(hand)

players = []
player_ids =[]

def get_player_index(player):
    at = player.find("@")
    player_name = player[0:at]
    player_id = player[at+2:]

    if player_id not in player_ids:
        player_ids.append(player_id)
        players.append(player_name)
        #print ("player_id=" + player_id + " player_name=" + player_name)
    return player_ids.index(player_id)


spade_offset    = 0xa1
heart_offset    = 0xb1
diamond_offset  = 0x81
clubs_offset    = 0x91

def get_unicode_card(card):
    card1  = card[0:-1]
    suite1 = card[-3:]
    card1 = card1[0]

    if card1 == 'A':
        num = 1
    elif card1 == 'J':
        num = 11
    #unicode has knight between J & K
    elif card1 == 'Q':
        num = 12+1
    elif card1 == 'K':
        num = 13+1
    else:
        num = int(card1)

    if suite1 == '♠':
        c4 = spade_offset
        c3=chr(0x82)
    elif suite1 == '♥':
        c4 = heart_offset
        c3=chr(0x82)
    elif suite1 == '♦':
        c4 = diamond_offset
        c3=chr(0x83)
    elif suite1 == '♣':
        c4 = clubs_offset
        c3=chr(0x83)

    cx = "\xf0\x9f" + c3 + chr(c4+num-1)
    return cx

def get_card1(hand):
    comma = hand.find(",")
    card1  = hand[0:comma]
    return get_unicode_card(card1)

def get_card2(hand):
    comma = hand.find(",")
    card2  = hand[comma+2:]
    return get_unicode_card(card2)


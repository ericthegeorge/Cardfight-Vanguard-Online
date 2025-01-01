import mysql.connector
import os
import random

SUPER_PACK_CHANCE = 0.5
C = 0
R = 1
RR = 2
RRR = 3
SP = 4 

password = os.getenv("DB_PASSWORD")

# consolidated pack rarity stats

# base original rarities
# 12 packs per box
# 7 cards per pack
    # therefore 7*12 = 84 cards per box
# 5 C per pack
    # therefore 5*12 = 60 C cards per box
# 1 R per pack
    # therefore 1*21 = 12 R cards per box
# 6 RR per box
# 4 RRR per box
# 1 SP per box
# Sum total = 60 + 12 + 6 + 4 + 1 = 83

# reconfigured rarities for 'greater enjoyment'
# 7 cards per pack
# 12 packs per box
# 3 C per pack
    # therefore 3*12 = 36 C cards per box
# 2 R per pack
    # therefore 2*12 = 24 R cards per box
# 1 small flex card per pack, either R or higher
    # 50% R, 42% RR, 8% RRR
    # therefore roughly 6 R cards per box
    # therefore roughly 5 RR cards per box
    # therefore roughly 1 RRR card per box
# 1 big flex card per pack, either RR or higher
    # 66% RR, 33% RRR, 1%SP
    # therefore roughly 8 RR cards per box
    # therefore roughly 3 RRR cards per box
    # therefore roughly 1 SP card per box
# Sum total = 36 + (24 + 6) + (5 + 8) + (1 + 3) + 1
#           = 36 +    30    +    13    +   4    + 1 = 

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password=password,
    database="Cardfight Vanguard Online - Local Database"
)

cursor = conn.cursor()

def open_pack():
    pack_rarities = []
    super_pack_rarity = random.uniform(0, 100)
    if(super_pack_rarity < SUPER_PACK_CHANCE):
        print("SUPER PACK GET!")
        # all cards are R or higher, and the last card is a RRR or higher
        for i in range (0, 6):
            rarity = random.uniform(0,100)
            card_rarity = -1
            match rarity:
                case x if x < 45:
                    card_rarity = R
                case x if x < 85:
                    card_rarity = RR
                case x if x < 99.5:
                    card_rarity = RRR
                case _:
                    card_rarity = SP
            pack_rarities.append(card_rarity)
        rarity = random.uniform(0, 100)
        card_rarity = -1
        if rarity < 75:
            card_rarity = RRR
        else:
            card_rarity = SP
        pack_rarities.append(card_rarity)
        return pack_rarities
    else:
        # first four cards 90 % chance to be common
        for i in range (0, 4):
            rarity = random.uniform(0,100)
            card_rarity = -1
            match rarity:
                case x if x < 60:
                    card_rarity = C
                case x if x < 90:
                    card_rarity = R
                case x if x < 95:
                    card_rarity = RR
                case _:
                    card_rarity = RRR
            pack_rarities.append(card_rarity)
        # next two cards 50 % chance to be common
        for i in range (4,6):
            rarity = random.uniform(0, 100)
            card_rarity = -1
            match rarity:
                case x if x < 35:
                    card_rarity = C
                case x if x < 75:
                    card_rarity = R
                case x if x < 95:
                    card_rarity = RR
                case _:
                    card_rarity = RRR
            pack_rarities.append(card_rarity)
        # at least one 'good' card in a pack
        rarity = random.uniform(0, 100)
        if (pack_rarities.count(C) == 6):
            card_rarity = -1
            match rarity:
                case x if x < 45 :
                    card_rarity = R
                case x if x < 85:
                    card_rarity = RR
                case x if x < 99.5:
                    card_rarity = RRR
                case _:
                    card_rarity = SP
            pack_rarities.append(card_rarity)
        return pack_rarities

def rarity_to_char(rarity):
    if rarity == C:
        return 'C'
    if rarity == R:
        return 'R'
    if rarity == RR:
        return 'RR'
    if rarity == RRR:
        return 'RRR'
    if rarity == SP:
        return 'SP'

def get_card(rarity):
    query = "SELECT * FROM cards WHERE rarity = %s AND number LIKE %s ORDER BY RAND() LIMIT 1;"

    cursor.execute(query, (rarity, "BT01%"))
    
    card = cursor.fetchone()
    return card

for i in range (0, 10):
    card_rarities = open_pack()
    for card_rarity in card_rarities:
        char_rarity = rarity_to_char(card_rarity)
        the_card = get_card(char_rarity)
        print(the_card[1], the_card[17])
# testing probabilities
# total_C = 0
# total_R = 0
# total_RR = 0
# total_RRR = 0
# total_SP = 0
# for i in range (0, 1000):
#     cards = open_pack()
#     total_C += cards.count(C) 
#     total_R += cards.count(R) 
#     total_RR += cards.count(RR) 
#     total_RRR += cards.count(RRR) 
#     total_SP += cards.count(SP)
#     print(f"Iteration number {i} is done!\n")
    
# prob_C = total_C / 70
# prob_R = total_R / 70
# prob_RR = total_RR / 70
# prob_RRR = total_RRR / 70
# prob_SP = total_SP / 70

# print(f"Probability of Common (C): {prob_C:.2f}%\tProbability of Rare (R): {prob_R:.2f}%\tProbability of Double Rare (RR): {prob_RR:.2f}%\tProbability of Triple Rare (RRR): {prob_RRR:.2f}%\tProbability of Special Parallel (SP): {prob_SP:.2f}%\t")

# print(f"Collected {total_RRR} Triple Rare's (RRR)\n")



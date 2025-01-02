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
# SP = RRR

# EACH PACK -> 7 CARDS
# EACH BOX -> 12 PACKS
# EACH BOX -> 84
# 84:
# 42 C : 24 R : 12 RR : 6 RRR
    #  66 ->   78  -> 84
# Average probabilities per rarity:
    # C: 50%     -> 7/14 -> 3.5/7
    # R: 28.57%  -> 4/14 ->   2/7
    # RR: 14.29% -> 2/14 ->   1/7
    # RRR: 7.14% -> 1/14 -> 0.5/7
    
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
                case _:
                    card_rarity = RRR
            pack_rarities.append(card_rarity)
        rarity = random.uniform(0, 100)
        card_rarity = RRR
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
                case x if x < 95:
                    card_rarity = R
                case x if x < 99:
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
        card_rarity = -1
        match rarity:
            case x if x < 40 :
                card_rarity = R
            case x if x < 85:
                card_rarity = RR
            case _:
                card_rarity = RRR
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
        return 'RRR'
    raise ValueError(f"Invalid rarity value: {rarity}")
    
def char_to_rarity(char):
    if char == 'C':
        return C
    if char == 'R':
        return R
    if char == 'RR':
        return RR
    if char == 'RRR':
        # Ambiguity resolution: Default to RRR unless specified otherwise
        return RRR
    raise ValueError(f"Invalid rarity character: {char}")


def get_card(rarity):
    query = "SELECT * FROM cards WHERE rarity = %s AND number LIKE %s ORDER BY RAND() LIMIT 1;"

    cursor.execute(query, (rarity, "BT01%"))
    
    card = cursor.fetchone()
    return card



total_C = 0
total_R = 0
total_RR = 0
total_RRR = 0

test_amt = 20
for i in range (0, test_amt):
    print(f"\nOpening pack {i+1}!")
    card_rarities = open_pack()
    total_C += card_rarities.count(C)
    total_R += card_rarities.count(R)
    total_RR += card_rarities.count(RR)
    total_RRR += card_rarities.count(RRR)
    
    for card_rarity in card_rarities:
        char_rarity = rarity_to_char(card_rarity)
        the_card = get_card(char_rarity)
        # print(the_card[1], the_card[17])


prob_C = total_C / (test_amt * 7)* 100
prob_R = total_R / (test_amt * 7)* 100
prob_RR = total_RR / (test_amt * 7)* 100
prob_RRR = total_RRR / (test_amt * 7)* 100

print(f"Probability of Common (C): {prob_C:.2f}%\tProbability of Rare (R): {prob_R:.2f}%\tProbability of Double Rare (RR): {prob_RR:.2f}%\tProbability of Triple Rare (RRR): {prob_RRR:.2f}%")

print(f"Collected {total_RRR} Triple Rare's (RRR)\n")
    
    
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



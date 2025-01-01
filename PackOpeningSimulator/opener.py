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
    else:
        # first four cards 90 % chance to be common
        for i in range (0, 4):
            rarity = random.uniform(0,100)
            card_rarity = -1
            match rarity:
                case x if x < 95:
                    card_rarity = C
                case x if x < 98:
                    card_rarity = R
                case x if x < 99.5:
                    card_rarity = RR
                case _:
                    card_rarity = RRR
            pack_rarities.append(card_rarity)
        # next two cards 50 % chance to be common
        for i in range (4,6):
            rarity = random.uniform(0, 100)
            card_rarity = -1
            match rarity:
                case x if x < 50:
                    card_rarity = C
                case x if x < 80:
                    card_rarity = R
                case x if x < 97.5:
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

# testing probabilities
total_C = 0
total_R = 0
total_RR = 0
total_RRR = 0
total_SP = 0
for i in range (0, 1000):
    cards = open_pack()
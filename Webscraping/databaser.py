import mysql.connector
import os

password = os.getenv("DB_PASSWORD")


conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password=password,
    database="Cardfight Vanguard Online - Local Database"
)

cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS cards (
               id INT AUTO_INCREMENT PRIMARY KEY,
               name VARCHAR(255) NOT NULL,
               image VARCHAR(255),
               type VARCHAR(255),
               `group` VARCHAR(255),
               race VARCHAR(255),
               nation VARCHAR(255),
               grade VARCHAR(255),
               power VARCHAR(255),
               critical VARCHAR(255),
               shield VARCHAR(255),
               skill VARCHAR(255),
               gift VARCHAR(255),
               effect TEXT,
               flavor VARCHAR(255),
               regulation VARCHAR(255),
               number VARCHAR(255),
               rarity VARCHAR(255),
               illstrator VARCHAR(255)
               ) 
               ''')
cursor.execute('''
    INSERT INTO cards (name, image, type, `group`, race, nation, grade, power, critical, shield, skill, gift, effect, flavor, regulation, number, rarity, illstrator)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
''', ('King of Knights, Alfred', 'https://en.cf-vanguard.com/wordpress/wp-content/images/cardlist/bt01/BT01_001EN.png', 'Normal Unit', 'Royal Paladin', 'Human', 'United Sanctuary', 'Grade 3', 'Power 10000', 'Critical 1', 'Shield -', 'Twin Drive!!', '-', '[CONT](VC):Your units cannot boost this unit.[CONT](VC):During your turn, this unit gets [Power] +2000 for each of your <Royal Paladin> rear-guards.[ACT](VC/RC):[Counter-Blast 3] Search your deck for up to one grade 2 or less <Royal Paladin>, call it to (RC), and shuffle your deck.', 'I command you under the name of the King of Knights! Warriors, heed my call!', 'G-Regulation', 'BT01/001EN', 'RRR', '伊藤彰'))

conn.commit() 
conn.close()
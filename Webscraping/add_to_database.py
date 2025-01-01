import mysql.connector
import os
import csv 

password = os.getenv("DB_PASSWORD")


conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password=password,
    database="Cardfight Vanguard Online - Local Database"
)

cursor = conn.cursor()

with open('./assets/cards.csv', mode='r', encoding ='utf-8') as file:
    csv_reader = csv.reader(file)
    next(csv_reader)
    query = """
        INSERT IGNORE INTO cards (name, image, type, `group`, race, nation, grade, power, critical, shield, skill, gift, effect, flavor, regulation, number, rarity, illstrator)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
    for row in csv_reader:
        cursor.execute(query, row)
        
    conn.commit()
            

conn.commit() 
conn.close()

print("Insertion successful")
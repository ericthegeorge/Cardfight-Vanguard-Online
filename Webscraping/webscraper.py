import requests
# import beautiful soup for webscraping
from bs4 import BeautifulSoup

# import selenium for loading pages properly
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
# time for delays
import time
# csv for databasing outputs
import csv

# CONSTANTS FOR CARD DATA   
NAME = 0
IMAGE = 1
TYPE = 2
GROUP = 3
RACE = 4
NATION = 5
GRADE = 6
POWER = 7
CRITICAL = 8
SHIELD = 9
SKILL = 10
GIFT = 11
EFFECT = 12
FLAVOR = 13
REGULATION = 14
NUMBER = 15
RARITY = 16
ILLSTRATOR = 17

# urls
# site uses relative urls, keep track of base url to actually visit it
base_url = "https://en.cf-vanguard.com"
url = "https://en.cf-vanguard.com/cardlist/cardsearch/?expansion=5"


# First, since the site is loaded dynamically, 
# we can use selenium to ensure all the cards are loaded
# before we continue with the webscraping

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get(url)

# let page load
time.sleep(5)

# time amount between attempts to load by scrolling
scroll_pause_time = 1
last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    # scroll to bottom, wait, check new scroll height and compare
    # if theres more to scroll continue, else break out

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(scroll_pause_time)

    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

print("Selenium has completed page loading via scrolling")

# use the page selenium loads to webscrape
card_list_div = driver.find_element


html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
card_list_div = soup.find('div', class_='cardlist_gallerylist')

# get link to specific cards first, to open those webpages for 
# card content and details

card_links = card_list_div.find_all('a')
all_links = []
for card in card_links:
    all_links.append(base_url + card['href'])
    # print(f"Link: {base_url + card['href']}")
#end for




card_images = card_list_div.find_all('img') if card_list_div else []

data_to_write = [
    ["Name", "Image", "Type", "Group", "Race", "Nation", "Grade", "Power", "Critical", "Shield", "Skill", "Gift", "Effect", "Flavor", "Regulation", "Number", "Rarity", "Illstrator"]
    ]
i = 0
for link in all_links:
    page_response = requests.get(all_links[i])

    data = ['','','','','','','','','','','','','','','','','','']
    card_soup = BeautifulSoup(page_response.text, 'html.parser')
    # card_name = card_soup.find('div', class_ = 'name')
    card_image_div = card_soup.find('div', class_='main')
    if card_image_div:
        card_image_tag = card_image_div.find('img') 
        data[NAME] = card_image_tag['title']
        data[IMAGE] = base_url + card_image_tag['src']
        # card_image = base_url + card_image_tag['src']
        # card_name = card_image_tag['title']
    else:
        print("Error finding card image")


        # Extract and clean text for each attribute

    data[TYPE] = card_soup.find('div', class_='type').text.strip() if card_soup.find('div', class_='type') else None
    data[GROUP] = card_soup.find('div', class_='group').text.strip() if card_soup.find('div', class_='group') else None
    data[RACE] = card_soup.find('div', class_='race').text.strip() if card_soup.find('div', class_='race') else None
    data[NATION] = card_soup.find('div', class_='nation').text.strip() if card_soup.find('div', class_='nation') else None
    data[GRADE] = card_soup.find('div', class_='grade').text.strip() if card_soup.find('div', class_='grade') else None
    data[POWER] = card_soup.find('div', class_='power').text.strip() if card_soup.find('div', class_='power') else None
    data[CRITICAL] = card_soup.find('div', class_='critical').text.strip() if card_soup.find('div', class_='critical') else None
    data[SHIELD] = card_soup.find('div', class_='shield').text.strip() if card_soup.find('div', class_='shield') else None
    data[SKILL] = card_soup.find('div', class_='skill').text.strip() if card_soup.find('div', class_='skill') else None
    data[GIFT] = card_soup.find('div', class_='gift').text.strip() if card_soup.find('div', class_='gift') else None
    data[EFFECT] = card_soup.find('div', class_='effect').text.strip() if card_soup.find('div', class_='effect') else None
    data[FLAVOR] = card_soup.find('div', class_='flavor').text.strip() if card_soup.find('div', class_='flavor') else None

    card_text_list_div = card_soup.findAll('div', class_= 'text-list')[1]

    card_regulation_div = card_text_list_div.find('div', class_='regulation')
    data[REGULATION] = card_regulation_div.text.strip() 

    card_number_div = card_text_list_div.find('div', class_='number')
    data[NUMBER] = card_number_div.text.strip() 

    card_rarity_div = card_text_list_div.find('div', class_='rarity')
    data[RARITY] = card_rarity_div.text.strip() 

    card_illstrator_div = card_text_list_div.find('div', class_='illstrator')
    data[ILLSTRATOR] = card_illstrator_div.text.strip() 


    if (i == 0):
        print(
    f"Name: {data[NAME]}\t Image: {data[IMAGE]}\t "
    f"Type: {data[TYPE]}\t Group: {data[GROUP]}\t "
    f"Race: {data[RACE]}\t Nation: {data[NATION]}\t Grade: {data[GRADE]}\t "
    f"Power: {data[POWER]}\t Critical: {data[CRITICAL]}\t Shield: {data[SHIELD]}\t "
    f"Skill: {data[SKILL]}\t Gift: {data[GIFT]}\t Effect: {data[EFFECT]}\t "
    f"Flavor: {data[FLAVOR]}\t Regulation: {data[REGULATION]}\t "
    f"Number: {data[NUMBER]}\t Rarity: {data[RARITY]}\t Illstrator: {data[ILLSTRATOR]}\n")

    # print(f"Name: {card_name}\t Image: {card_image}\n")
    data_to_write.append(data)
    i += 1


# for card in card_images:
#     card_name = card['title']  # The text of the <a> tag (card name)
#     card_pic = card['src']
#     print(f"Name: {card_name}, IMG: {base_url + card_pic}")

    # write to csv file
    # first check data

# for piece in data_to_write:
#     print(f"{piece}\n")

with open("cards.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerows(data_to_write)


driver.quit()

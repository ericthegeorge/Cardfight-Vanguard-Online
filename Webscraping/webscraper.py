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
scroll_pause_time = 2
last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    # scroll to bottom, wait, check new scroll height and compare
    # if theres more to scroll continue, else break out

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(scroll_pause_time)




response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

card_list_div = soup.find('div', class_='cardlist_gallerylist')

# get link to specific cards first, to open those webpages for 
# card content and details

card_links = card_list_div.find_all('a')
all_links = []
for card in card_links:
    all_links.append(base_url + card['href'])
    # print(f"Link: {base_url + card['href']}")





card_images = card_list_div.find_all('img') if card_list_div else []

for card in card_images:
    card_name = card['title']  # The text of the <a> tag (card name)
    card_pic = card['src']
    print(f"Name: {card_name}, IMG: {base_url + card_pic}")
import requests
from bs4 import BeautifulSoup

url = "https://en.cf-vanguard.com/cardlist/cardsearch/?expansion=5"
response = requests.get(url)


soup = BeautifulSoup(response.text, 'html.parser')

card_list_div = soup.find('div', class_='cardlist_gallerylist')
card_links = card_list_div.find_all('img') if card_list_div else []

for card in card_links:
    card_name = card['title']  # The text of the <a> tag (card name)
    card_url = card['src']
    print(f"Name: {card_name}, URL: {card_url}")
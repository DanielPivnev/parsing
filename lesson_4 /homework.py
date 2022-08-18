import requests
from bs4 import BeautifulSoup as bs

from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client.scraping_hw_4

print('START\n')

url = 'https://quotes.toscrape.com'
page = 1
quotes_list = []
next_page_exists = True
while next_page_exists:
    response = requests.get(url)

    if response.status_code == 200:
        print(f'Page {page}')
        html = bs(response.content, 'html.parser')
        quotes = html.find_all('div', class_='quote')

        for quote_num, quote in enumerate(quotes, 1):
            print(f'\tStart scraping quote {quote_num}')
            text = quote.find('span', class_='text').text
            author = quote.find('small', class_='author').text
            tags = [tag.text for tag in quote.find('div', class_='tags').find_all('a', class_='tag')]

            quote_dict = {
                'text': text,
                'author': author,
                'tags': tags
            }

            quotes_list.append(quote_dict)

        try:
            next_page = html.find('li', class_='next')
            url = 'https://quotes.toscrape.com' + next_page.find('a')['href']
            page += 1
        except AttributeError:
            next_page_exists = False
    else:
        next_page_exists = False

print('\nDONE')

db.cars.insert_many(quotes_list)

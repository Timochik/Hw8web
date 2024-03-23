import requests
from bs4 import BeautifulSoup
import json

# Функція для отримання даних про цитати та авторів з однієї сторінки
def scrape_quotes(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    quotes = []

    for quote in soup.find_all('div', class_='quote'):
        text = quote.find('span', class_='text').text
        author = quote.find('small', class_='author').text
        tags = [tag.text for tag in quote.find_all('a', class_='tag')]
        quotes.append({'author': author, 'quote': text, 'tags': tags})
        
    return quotes

# Функція для отримання посилання на наступну сторінку з цитатами
def get_next_page_url(soup):
    next_button = soup.find('li', class_='next')
    if next_button:
        return 'http://quotes.toscrape.com' + next_button.find('a')['href']
    else:
        return None

# Функція для скрапінгу всіх цитат з усіх сторінок сайту
def scrape_all_quotes():
    base_url = 'http://quotes.toscrape.com'
    url = base_url
    all_quotes = []

    while url:
        quotes_on_page = scrape_quotes(url)
        all_quotes.extend(quotes_on_page)
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        url = get_next_page_url(soup)

    return all_quotes

# Зберігання даних про цитати у файлі quotes.json
quotes_data = scrape_all_quotes()
with open('quotes.json', 'w', encoding='utf-8') as file:
    json.dump(quotes_data, file, ensure_ascii=False, indent=4)

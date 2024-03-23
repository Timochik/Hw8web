import requests
from bs4 import BeautifulSoup
import json

def scrape_author_info(url):
  response = requests.get(url)
  soup = BeautifulSoup(response.content, 'html.parser')

  # Find author details element
  author_details = soup.find('div', class_='author-details')

  # Extract information (assuming elements exist)
  fullname = author_details.find('h3').text.strip() if author_details else None
  born_date = author_details.find('span', class_='author-born-date').text.strip() if author_details else None
  born_location = author_details.find('span', class_='author-born-location').text.strip() if author_details else None
  description = author_details.find('div', class_='author-description').text.strip() if author_details else None

  # Return dictionary
  return {
      "fullname": fullname,
      "born_date": born_date,
      "born_location": born_location,
      "description": description
  }

authors_data = []

# Loop through two quote pages (modify the range as needed)
for page_num in range(1, 3):
  url = f"http://quotes.toscrape.com/page/{page_num}"
  response = requests.get(url)
  soup = BeautifulSoup(response.content, 'html.parser')

  # Find all quotes on the page
  quotes = soup.find_all('div', class_='quote')

  for quote in quotes:
    # Extract author URL from quote
    author_url = quote.find('a')['href']

    # Call function to scrape author info
    author_data = scrape_author_info(f"http://quotes.toscrape.com{author_url}")

    # Add author data to list (assuming data is retrieved successfully)
    if author_data:
        authors_data.append(author_data)

# Write data to JSON file with indentation
with open('authors.json', 'w') as outfile:
  json.dump(authors_data, outfile, indent=4)


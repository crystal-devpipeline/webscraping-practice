import requests
from bs4 import BeautifulSoup
from pprint import pprint
import os

url = 'https://www.billboard.com/artist/onerepublic/'
page_content = ''


def get_text_element(bs, tag, class_=None):
    result = bs.find(tag, class_=class_)
    if result:
            return result.text.strip()
    return ''

if not os.path.exists('onerepublic.html'):
    print("Loading page from the internet...")
    page = requests.get(url)
    page_content = page.content.decode()

    with open('onerepublic.html', 'w') as outfile:
        outfile.write(page_content)
else:
    print("Reading html from file...")
    with open('onerepublic.html', 'r') as infile:
        page = infile.read()
    page_content = page.encode('utf-8')

soup = BeautifulSoup(page_content, 'html.parser')

billboard = soup.find_all('div', class_='c-label')

billboard_data = []

for hit in billboard:
    artist = get_text_element(hit, 'span', class_='c-label')
    top_hit = get_text_element(hit, 'h3', class_='c-title')
    debut_date = get_text_element(hit, 'span', class_='c-span')
    peak_pos = get_text_element(hit, 'span', class_='c-span')
    peak_date = get_text_element(hit, 'span', class_='c-span')
    wks_on_chart = get_text_element(hit, 'span', class_='c-span')


    print(f"{hit['artist']}, {hit['top_hit']}, {hit['debut_date']}, {hit['peak_pos']} ({hit['peak_date']}, {hit['wks_on_chart']})\n")

# not working yet :(
import requests
from bs4 import BeautifulSoup
import os

url = "https://www.groupon.com/browse/salt-lake-city?lat=40.761&lng=-111.891&query=escape+rooms+in+orem&address=Salt+Lake+City&division=salt-lake-city&locale=en_US"


Headers = {
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'
}

def get_text_element(bs, tag, class_=None):
    result = bs.find(tag, class_=class_)
    if result:
            return result.text.strip()
    return ''

response = requests.get(url, headers=Headers)

if not os.path.exists('groupon.html'):
    print("Loading page from the internet...")
    page = requests.get(url)
    page_content = page.content.decode()

    with open('groupon.html', 'w') as outfile:
        outfile.write(page_content)
else:
    print("Reading html from file...")
    with open('groupon.html', 'r') as infile:
        page = infile.read()
    page_content = page.encode('utf-8')


soup = BeautifulSoup(response.content, 'html.parser')

deals_soup = soup.find_all('div', class_='cui-content')

for deal in deals_soup:
    name = get_text_element(deal, 'div', class_='cui-udc-title')
    location = get_text_element(deal, 'span', class_='cui-location-name')

    prices_soup = deal.find('div', class_='cui-price')
    original_price, price_discount, urgency_price = '','',''
    if prices_soup:
        original_price = get_text_element(deal, 'div', class_='cui-price-original')
        price_discount = get_text_element(deal, 'div', class_='cui-price-discount')
        urgency_price = get_text_element(deal, 'div', class_='cui-verbose-urgency-price')       
        
    if name:
        print(f'{name} ({location}) -- {original_price} -- {urgency_price}')



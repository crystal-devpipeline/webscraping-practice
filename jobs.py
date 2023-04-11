import requests
from bs4 import BeautifulSoup
from pprint import pprint
import os

url = 'http://realpython.github.io/fake-jobs/'

page_content = ''

if not os.path.exists('fake-jobs.html'):
    print("Loading page from the internet...")
    page = requests.get(url)
    page_content = page.content.decode()

    with open('fake-jobs.html', 'w') as outfile:
        outfile.write(page_content)
else:
    print("Reading html from file...")
    with open('fake-jobs.html', 'r') as infile:
        page = infile.read()
    page_content = page.encode('utf-8')

soup = BeautifulSoup(page_content, 'html.parser')

jobs = soup.find_all('div', class_='card-content')

jobs_data = []

for job in jobs:
    job_title = job.find('h2').text.strip()

    company_name = job.find('h3').text.strip()

    location = job.find('p', class_='location')
    city = ''
    province = ''
    if location:
        location = location.text.strip()
        lst = location.split(',')
        city = lst[0]
        province = lst[1].strip()
    else:
        location = ''

    date_posted = job.find('time').text.strip()

    link_href = ''
    links = job.find_all('a')

    for link in links:
        if link.text == 'Apply':
            link_href = link['href']

    description = ''
    job_detail_content = ''

    filename = link_href.split('/')[-1].strip()

    if not os.path.exists(filename):
        job_detail_page = requests.get(link_href)
        job_detail_content = job_detail_page.content.decode()

        with open(filename, 'w') as outfile:
            outfile.write(job_detail_content)
    else:
        with open(filename, 'r') as infile:
            page = infile.read()
        job_detail_content = page.encode('utf-8')
    
    job_soup = BeautifulSoup(job_detail_page.content, 'html.parser')
    content_soup = job_soup.find('div', class_='content')
    description = content_soup.find('p').text.strip()


    next_job = {
        'title': job_title,
        'company': company_name,
        'description': description,
        'city': city,
        'province': province,
        'date_posted': date_posted,
        'apply_link': link_href,
    }
    jobs_data.append(next_job)


for job in jobs_data:
    print(f"{job['title']}, {job['company']} ({job['city']}, {job['province']}) [posted: {job['date_posted']}]\n{job['apply_link']}\n{job['description']}\n")

pprint(jobs_data)
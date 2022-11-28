import requests
from bs4 import BeautifulSoup
import csv

url = 'https://www.prieskoniunamai.lt/prieskoniai?limit=60'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'}

html_page = requests.get(url, headers=headers)
soup = BeautifulSoup(html_page.content, 'lxml')
content = soup.find_all('div', class_='name')

for link in content:
    url_list = link.find('a')['href']
    print(url_list)













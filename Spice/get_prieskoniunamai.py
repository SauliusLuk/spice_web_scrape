import requests
from bs4 import BeautifulSoup
import csv
import time

urls = ['https://www.prieskoniunamai.lt/prieskoniai?limit=60',
        'https://www.prieskoniunamai.lt/prieskoniai?limit=60&page=2',
        'https://www.prieskoniunamai.lt/prieskoniai?limit=60&page=3']

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'}

csv_file = open('prieskoniunamai.csv', 'w', encoding='utf-8', newline='')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['Pardavėjas', 'Produktas', 'Svoris', 'Kaina'])

for url in urls:
    html_page = requests.get(url, headers=headers)
    soup = BeautifulSoup(html_page.content, 'lxml')
    content = soup.find_all('div', class_='name')
    text = 'Grynasis kiekis:'

    for link in content:
        try:
            url_list = link.find('a')['href']
            html_page = requests.get(url_list, headers=headers)
            soup = BeautifulSoup(html_page.content, 'lxml')

            product = []
            product_title = soup.find_all('strong', class_='page-title')[0].get_text()
            product_weight = soup.find_all(lambda tag: tag.name == "strong" and text in tag.text)[0].get_text().split()[
                2]
            product_price_eur = soup.find_all('span', id='price-update')[0].get_text()
            product_price_final = product_price_eur.replace('€', '')

            product.append(f'Prieskonių namai')
            product.append(product_title)
            product.append(product_weight)
            product.append(product_price_final)

            csv_writer.writerow(product)
            print(product)

            time.sleep(5)
        except:
            pass

import requests
from bs4 import BeautifulSoup
import csv
import time

urls = ['https://chaichai.lt/produkto-kategorija/prieskoniai/',
        'https://chaichai.lt/produkto-kategorija/prieskoniai/page/2/',
        'https://chaichai.lt/produkto-kategorija/prieskoniai/page/3/',
        'https://chaichai.lt/produkto-kategorija/prieskoniai/page/4/',
        'https://chaichai.lt/produkto-kategorija/prieskoniai/page/5/',
        'https://chaichai.lt/produkto-kategorija/prieskoniai/page/6/']
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'}

csv_file = open('chaichai.csv', 'w', encoding="utf-8", newline='')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['Pardavėjas', 'Produktas', 'Svoris', 'Kaina'])

for url in urls:
    html_page = requests.get(url, headers=headers)
    soup = BeautifulSoup(html_page.content, 'lxml')

    for i in range(0, 12):
        try:
            product = []
            product_title = soup.find('ul', class_='products columns-4 cards-grid').find_all('h2')[i].get_text()
            product_weight_g = soup.find('span', class_='chai-price__secondary').get_text()
            product_weight = product_weight_g.replace('g', '')
            product_price_eur = soup.find_all('bdi')[i].get_text()
            product_price = product_price_eur.replace('€', '')

            product.append('Chaichai')
            product.append(product_title)
            product.append(product_weight)
            product.append(product_price)

            csv_writer.writerow(product)
            time.sleep(5)

        except:
            pass

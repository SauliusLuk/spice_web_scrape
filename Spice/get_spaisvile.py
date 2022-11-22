import requests
from bs4 import BeautifulSoup
import csv
import time

urls = ['https://www.spaisvile.lt/prieskoniai-daro-stebuklus/grynieji-prieskoniai',
        'https://www.spaisvile.lt/prieskoniai-daro-stebuklus/grynieji-prieskoniai?limit=0&orderBy=0&page=2',
        'https://www.spaisvile.lt/prieskoniai-daro-stebuklus/grynieji-prieskoniai?limit=0&orderBy=0&page=3',
        'https://www.spaisvile.lt/prieskoniai-daro-stebuklus/prieskoniu-misiniai',
        'https://www.spaisvile.lt/prieskoniai-daro-stebuklus/prieskoniu-misiniai?limit=0&orderBy=0&page=2',
        'https://www.spaisvile.lt/prieskoniai-daro-stebuklus/prieskoniu-misiniai?limit=0&orderBy=0&page=3',
        'https://www.spaisvile.lt/prieskoniai-daro-stebuklus/prieskoniu-misiniai?limit=0&orderBy=0&page=4',
        'https://www.spaisvile.lt/prieskoniai-daro-stebuklus/prieskoniu-misiniai?limit=0&orderBy=0&page=5',
        'https://www.spaisvile.lt/prieskoniai-daro-stebuklus/prieskoniu-misiniai?limit=0&orderBy=0&page=6',
        'https://www.spaisvile.lt/prieskoniai-daro-stebuklus/prieskoniu-misiniai?limit=0&orderBy=0&page=7',
        'https://www.spaisvile.lt/prieskoniai-daro-stebuklus/prieskoniu-misiniai?limit=0&orderBy=0&page=8']

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'}

csv_file = open('spaisvile.csv', 'w', encoding="utf-8", newline='')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['Pardavėjas', 'Produktas', 'Svoris', 'Kaina'])

for url in urls:
    html_page = requests.get(url, headers=headers)
    soup = BeautifulSoup(html_page.content, 'lxml')
    div_content = soup.find_all('a', class_='shop-item')

    for i in range(0, 24):
        try:
            product = []
            product_title = div_content[i].find('div', class_='shop-item-title').get_text()
            product_weight_g = div_content[i].find('div', class_='shop-item-description').get_text().split()[-1:][0]
            product_weight = product_weight_g.replace('g', '')
            product_price = div_content[i].find('div', class_='shop-item-price').get_text()
            product_price_final = product_price.split(' ', 1)[1] # remove € sign and select price only

            product.append(f'Spaisvilė')
            product.append(product_title)
            product.append(product_weight)
            product.append(product_price_final)

            csv_writer.writerow(product)
            print(product)

            time.sleep(5)
        except:
            pass
import requests
from bs4 import BeautifulSoup
import csv
import time

source = requests.get('https://www.delona.lt/prieskoniai').text

soup = BeautifulSoup(source, 'html.parser')
div_content = soup.find_all('div', class_='caption')

csv_file = open('delona.csv', 'w', encoding="utf-8", newline='')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['Pardavėjas', 'Produktas', 'Svoris', 'Kaina'])

for i in range(0, 187):
    product = []
    product_title = div_content[i].find('h4').get_text()
    product_title_remove_space = product_title.replace(' g', 'g')  # kai kurios prekes turi tarpa svoryje '100 g'
    product_weight_g = product_title_remove_space.split(' ', 8)[-1:]
    product_weight_string = ' '.join(map(str, product_weight_g))
    product_weight = product_weight_string.replace('g', '')
    product_price = div_content[i].find('p', class_='price').get_text().split()
    product_price_string = ' '.join(map(str, product_price))  # create new string from product+price
    product_price_final = product_price_string.replace('€', '')

    product.append(f'Delona')
    product.append(product_title)
    product.append(product_weight)
    product.append(product_price_final)

    csv_writer.writerow(product)
    print(product)

    time.sleep(5)

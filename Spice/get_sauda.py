import requests
from bs4 import BeautifulSoup
import csv
import time
import re

urls = ['https://www.shop.sauda.lt/prieskoniai', 'https://www.shop.sauda.lt/prieskoniai/page/32',
        'https://www.shop.sauda.lt/prieskoniai/page/64']
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'}

csv_file = open('sauda.csv', 'w', encoding="utf-8", newline='')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['Pardavėjas', 'Produktas', 'Svoris', 'Kaina'])

for url in urls:
    try: # sitas try yra kad sustoti prieskoniu saraso pabaigoje
        html_page = requests.get(url, headers=headers)
        soup = BeautifulSoup(html_page.content, 'lxml')
        content = soup.find_all('div', class_='item-info-container')

        for i in range(0, 32):
            url_list = content[i].find_all('a')[0]
            url_href = url_list['href']
            html_page = requests.get(url_href, headers=headers)
            soup = BeautifulSoup(html_page.content, 'lxml')

            product = []

            # produktu urls turi skirtingus issidestymus, todel pradzioje ieskome 1kg svorio
            # jei nera, istraukiam default svori

            try:
                product_title_1 = soup.find('h2').get_text()
                product_price_eur_1kg = soup.find_all('strong', class_='price c1 fs6 fwb fl')[1].get_text().strip()
                product_price_1kg = product_price_eur_1kg.replace('€ su PVM', '')

                product.append(f'Sauda')
                product.append(product_title_1)
                product.append('1000')  # zinom, kad cia svoris 1kg, iskart pridedam 1000(g)
                product.append(product_price_1kg)

                csv_writer.writerow(product)
                print(product)
            except:
                product_title = soup.find('h2').get_text()
                product_price_eur = soup.find('strong', class_='price c1 fs6 fwb fl').get_text()
                product_price = product_price_eur.replace('€ su PVM', '').strip()

                try:
                    product_title_last_element = product_title.split()[-1:] # pasiimti tik svori (paskutinis elementas)
                    product_title_last_elem_str = product_title_last_element[0]
                    product_weight_list = re.findall('\d', product_title_last_elem_str)  # pasalinti raides, palikti skaicius, gauti skaiciu list
                    product_weight = ''.join(product_weight_list)  # sujungti list
                    x = int(product_weight) # paverciam string i integer, kad veiktu lambda apacioje
                    kg_to_grams = lambda kg: x*1000 if (x==1) else x # paversti kg i g
                    product_weight_in_g = kg_to_grams(x)

                    product.append(f'Sauda')
                    product.append(product_title)
                    product.append(product_weight_in_g)
                    product.append(product_price)

                except:
                    """Sitas exept padarytas vienam produktui SALDŽIOS RAUDONOS PAPRIKOS 40G (MALTOS)"""
                    product_title = soup.find('h2').get_text()
                    product_price_eur = soup.find('strong', class_='price c1 fs6 fwb fl').get_text()
                    product_price = product_price_eur.replace('€ su PVM', '').strip()

                    product.append(f'Sauda')
                    product.append(product_title)
                    product.append('40')
                    product.append(product_price)

                csv_writer.writerow(product)
                print(product)

            time.sleep(5)
    except:
        pass
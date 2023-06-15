import requests
from bs4 import BeautifulSoup
import csv
import time

base_url = "https://rekvizitai.vz.lt/imones/kavines_klubai_barai_restoranai/"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'
}

# Create a list to store the company data
company_data = []

# Iterate over each page
for page_num in range(1, 61):
    url = f"{base_url}{page_num}/"

    response = requests.get(url, headers=headers)
    html_content = response.text

    soup = BeautifulSoup(html_content, 'html.parser')

    # Find all company entries
    company_entries = soup.find_all('div', class_='company-info')

    # Iterate over each company entry
    for company in company_entries:
        # Extract the title
        title = company.find('a', class_='company-title').text.strip()

        # Extract the content
        content = company.find('a', class_='company-subtitle').text.strip()

        # Extract the activities if it exists, otherwise set it to None
        activities_element = company.find('div', class_='activities')
        activities = activities_element.text.strip() if activities_element else None

        # Extract the description if it exists, otherwise set it to None
        description_element = company.find('div', class_='description')
        description = description_element.text.strip() if description_element else None

        # Extract additional data
        details_block = company.find('div', class_='details-block__3')
        darbuotojai_value = None
        pardavimo_pajamos_value = None

        if details_block:
            darbuotojai_element = details_block.find('td', class_='name', text='Darbuotojai')
            if darbuotojai_element:
                darbuotojai_value = darbuotojai_element.find_next_sibling('td').text.strip()

            pardavimo_pajamos_element = details_block.find('td', class_='name', text='Pardavimo pajamos')
            if pardavimo_pajamos_element:
                pardavimo_pajamos_value = pardavimo_pajamos_element.find_next_sibling('td').text.strip()

        # Extract the company info link
        company_info_link = company.find('div', class_='see-info').find('a')['href']

        # Append the company data to the list
        company_data.append([title, content, activities, description, darbuotojai_value, pardavimo_pajamos_value, company_info_link])

        print(f"Record {len(company_data)} added")

        # Delay for 5 seconds between requests
        time.sleep(5)

# Write the data to a CSV file
filename = 'rekvizitai_kavines_kaunas.csv'
with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Title', 'Content', 'Activities', 'Description', 'Darbuotojai', 'Pardavimo pajamos', 'Company Info Link'])
    writer.writerows(company_data)

print(f"Data written to {filename} file.")

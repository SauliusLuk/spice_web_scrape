import requests
from bs4 import BeautifulSoup
import csv
import time

base_url = "https://rekvizitai.vz.lt/imones/maisto_gamyba/kaunas/"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'
}

# Create a list to store the company data
company_data = []

# Initialize the record counter
record_count = 1

# Iterate over each page
for page_num in range(1, 8):
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

        # Extract the company info link
        company_info_link = company.find('div', class_='see-info').find('a')['href']

        # Append the company data to the list
        company_data.append([record_count, title, content, activities, description, company_info_link])

        print(f"Record {record_count} added")

        # Increment the record counter
        record_count += 1

        # Delay for 10 seconds between requests
        time.sleep(10)

# Write the data to a CSV file
with open('rekvizitai_maisto_gamyba_kaunas.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Record Number', 'Title', 'Content', 'Activities', 'Description', 'Company Info Link'])
    writer.writerows(company_data)

print("Data written to rekvizitai_maisto_gamyba_kaunas.csv file.")

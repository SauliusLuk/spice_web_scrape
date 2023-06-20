import requests
from bs4 import BeautifulSoup
import csv
import time

url = "https://rekvizitai.vz.lt/imones/maisto_gamyba/kaunas/"

# Create a list to store the company data
company_data = []

# Initialize the record count
record_count = 0

# Iterate over each page
for page_num in range(1, 8):
    page_url = f"{url}{page_num}/"

    response = requests.get(page_url)
    html_content = response.content

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

        # Fetch the HTML content from the company info URL
        response = requests.get(company_info_link)
        html_content = response.content

        # Create a BeautifulSoup object for the company info URL
        soup_company_info = BeautifulSoup(html_content, 'html.parser')

        # Initialize the values as None
        darbuotojai_value = None
        pardavimo_pajamos_value = None

        try:
            # Find the <td> element with class="name" containing "Darbuotojai"
            td_element = soup_company_info.find('td', class_='name', text='Darbuotojai')

            # Extract the numeric value
            darbuotojai_value = ''.join(filter(str.isdigit, td_element.find_next_sibling('td').text))
        except AttributeError:
            pass

        try:
            # Find the <td> element with class="name" containing "Pardavimo pajamos"
            td_element = soup_company_info.find('td', class_='name', text='Pardavimo pajamos')

            # Find the following <td> element with class="value me-4"
            value_td = td_element.find_next_sibling('td', class_='value me-4')

            # Extract the numeric value
            value = value_td.text.strip().split(':')[1].split('€')[0].strip()
            pardavimo_pajamos_value = value
        except AttributeError:
            pass

        # Increment the record count
        record_count += 1

        # Add the data to the company_data list
        company_data.append({
            'Title': title,
            'Content': content,
            'Activities': activities,
            'Description': description,
            'Darbuotojai': darbuotojai_value,
            'Pardavimo pajamos': pardavimo_pajamos_value,
            'Company Info Link': company_info_link
        })

        # Print the record count and title
        print(f"Record {record_count} ('{title}') added.")

        # Sleep for 5 seconds before making the next request
        time.sleep(5)

# Specify the CSV file path
csv_file = 'rekvizitai_maisto_gamyba_kaunas.csv'

# Write the data to the CSV file
with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
    fieldnames = ['Title', 'Content', 'Activities', 'Description', 'Darbuotojai', 'Pardavimo pajamos', 'Company Info Link']
    writer = csv.DictWriter(file, fieldnames=fieldnames)

    writer.writeheader()
    writer.writerows(company_data)

print("Data extraction complete. The results have been saved to:", csv_file)

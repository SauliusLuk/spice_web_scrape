import requests
from bs4 import BeautifulSoup

url = 'https://rekvizitai.vz.lt/imone/kseda_uab/'

# Send a GET request to the URL
response = requests.get(url)

# Create a BeautifulSoup object with the response content
soup = BeautifulSoup(response.content, 'html.parser')

# Find the <td> element with class "name" and text "Darbuotojai"
darbuotojai_element = soup.find('td', class_='name', text='Darbuotojai')

if darbuotojai_element:
    # Get the following <td> element with class "value"
    value_element = darbuotojai_element.find_next('td', class_='value')

    # Extract the value from the element and remove non-digit characters
    value = ''.join(filter(str.isdigit, value_element.get_text()))

    print(value)
else:
    print("Element not found")

# Find the <td> element with class "name" and text "Pardavimo pajamos"
pardavimo_pajamos_element = soup.find('td', class_='name', text='Pardavimo pajamos')

if pardavimo_pajamos_element:
    # Get the following <td> element with class "value me-4"
    value_element = pardavimo_pajamos_element.find_next_sibling('td', class_='value me-4')

    if value_element:
        # Extract the value from the element
        value = value_element.get_text(strip=True)

        # Extract the number between ":" and "€"
        start_index = value.index(':') + 1
        end_index = value.index('€')
        number = value[start_index:end_index].strip()

        print(number)
    else:
        print("Value element not found")
else:
    print("Pardavimo pajamos element not found")

import requests
from bs4 import BeautifulSoup
import pandas as pd

# HTTP REQUEST
url = 'https://en.wikipedia.org/wiki/Thirty-six_Views_of_Mount_Fuji'
response = requests.get(url)
# print(response.status_code) # 200


# HTML PARSING
soup = BeautifulSoup(response.text, 'html.parser')

# Finding the specific table and the rows
table = soup.find('table', {'class':'wikitable'})
table_rows = table.find('tbody').find_all('tr')
# print(len(table_rows)) # 37 (The first row is the header)


# DATA EXTRACTION
data = []

# Skipping the first header row
for row in table_rows[1:]:
    item = {}  

    item['id'] = row.find_all('td')[0].text.strip()  
    item['english_title'] = row.find_all('td')[2].text.strip()  
    item['japonese_title'] = row.find_all('td')[3].text.split('\n')[0].strip() 

    data.append(item)


# SAVING DATA TO CSV
df = pd.DataFrame(data)

df.to_csv('views.csv', index=False)
print('Success')  

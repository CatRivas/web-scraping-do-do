import requests
from bs4 import BeautifulSoup
import os

def get_data(url, headers):
    img_urls = []  

    response = requests.get(url=url, headers=headers)

    soup = BeautifulSoup(response.text, 'html.parser')

    table = soup.find('table', {'class': 'wikitable'})
    table_rows = table.find('tbody').find_all('tr')

    for row in table_rows[1:]:
        img_src = row.find_all('td')[1].find('img').get('src')

        format_scr = img_src.replace('thumb/', '')
        format_scr = format_scr.rsplit('/', 1)[0]  
        format_img_scr = f'https:{format_scr}' 

        img_urls.append(format_img_scr)

    return img_urls    


# This function uses DIRECT WRITING with open(), use it if you just need to download the image, but if you want to manipulate the image use the 'pillow' library
def img_download(headers, urls_list, directory):
    # Creates the directory if it doesn't exist, but if it exists does nothing
    os.makedirs(directory, exist_ok=True)  

    for index, url in enumerate(urls_list):
        # Sending a GET request for each image URL
        response = requests.get(url=url, headers=headers)
        # print(type(response.content)) # type 'bytes' 

        if response.status_code == 200:
            file_name = os.path.join(directory, f'{index+1}.jpg')
            # Writing the image content (binary data) directly into a file using 'wb' mode
            with open(file_name, 'wb') as file:
                file.write(response.content)
                print(f"Image saved successfully! {file_name}")  

        else:
            print(f"Failed to download image. Status code: {response.status_code}")


if __name__ == '__main__': 
    # Simulating a browser user-agent to avoid being blocked as a bot (this was a huge problem for me)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}  

    url = 'https://en.wikipedia.org/wiki/Thirty-six_Views_of_Mount_Fuji'

    img_urls = get_data(url, headers)
    img_download(headers, img_urls, 'images')

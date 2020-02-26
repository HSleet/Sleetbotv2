import requests
import os
from bs4 import BeautifulSoup

url = 'https://api.thecatapi.com/v1/images/search'
cat_token = os.getenv('CATAPI')
headers = {'x-api-key': cat_token}

def get_cat():
    re = requests.get(url)
    cat = re.json()[0]['url']
    return cat

if __name__ == '__main__':
    print(get_cat())
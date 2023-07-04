import requests
from bs4 import BeautifulSoup

url = "https://www.apc.fr/"

response = requests.get(url)

print(response.status_code)
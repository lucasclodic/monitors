import requests
from bs4 import BeautifulSoup
import time

url = "https://www.apc.fr/soldes-30/men-sales/t-shirts-jeans.html"
webhook_url = "https://discord.com/api/webhooks/1124627340681551902/QM1T_hoo_Ta73VJOuBk57_cfNscB5bTyVIMThM6uHRAeb9hl_j7xR5aUfjys1AOK2FAt"

found_products = set()

while True: 
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    product_list = soup.find("ul", class_="product-list")
    products_items = product_list.find_all("li", class_="product-item")

    for product_item in products_items:
        product_name = product_item.find()

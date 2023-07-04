import requests
from bs4 import BeautifulSoup

url = "https://www.apc.fr/soldes-30/men-sales/t-shirts-jeans.html"

response = requests.get(url)

soup = BeautifulSoup(response.text, "html.parser")

product_list = soup.find('ul', class_='product-list')
products_items = product_list.find_all("li", class_="product-item")

found_products = set()

for product_item in products_items: 
    product_name = product_item.find("span", class_="product-name")
    
    if product_name not in found_products:
        found_products.add(product_name)
        product_price = product_item.find("span", class_="price-wrapper")
        product_link = product_item.find("a")




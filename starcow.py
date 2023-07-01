import requests
from bs4 import BeautifulSoup
import time

webhook_url = "https://discord.com/api/webhooks/1124627340681551902/QM1T_hoo_Ta73VJOuBk57_cfNscB5bTyVIMThM6uHRAeb9hl_j7xR5aUfjys1AOK2FAt"

def send_to_discord(product_name, product_price, image_url, product_link):
    # Ajoutez 'https:' au début de l'URL de l'image et du lien du produit
    if not image_url.startswith("https:"):
        image_url = f"https:{image_url}"
    if not product_link.startswith("https:"):
        product_link = f"https://www.starcowparis.com{product_link}"

    data = {
        "embeds": [
            {
                "title": product_name,
                "description": f"Price: {product_price}\n[View product here]({product_link})",
                "thumbnail": {"url": image_url},
                "color": 16711680,  # Couleur de la barre latérale de l'embed (rouge, par exemple)
            }
        ]
    }
    headers = {"Content-Type": "application/json"}
    response = requests.post(webhook_url, json=data, headers=headers)
    if response.status_code == 204:
        print(f"Sent to Discord: {product_name}")
    else:
        print(f"Failed to send to Discord: {response.status_code} - {response.text}")



url = "https://www.starcowparis.com/en/search?q=dunk+low&options%5Bprefix%5D=last&type=product"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36"
}

found_products = set()

while True:
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    product_list = soup.find("ul", class_="u-grid u-grid-cols-12 u-gap-5 3xl:u-gap-x-5-fluid-width")
    products_items = product_list.find_all("li", class_="u-col-span-6 lg:u-col-span-3 u-mb-20 md:u-mb-40 3xl:u-mb-40-fluid-height")

    for product_item in products_items:
        product_name_element = product_item.find("a", class_="u-block | u-text-14 3xl:u-text-[0.972vw] u-font-medium | u-extend-href")
        product_name = product_name_element.text

        if product_name not in found_products:
            found_products.add(product_name)
            product_price_element = product_item.find("p", class_="t-surtitle t-surtitle--price")
            product_price = product_price_element.text
            image_element = product_item.find("img", class_="c-card-product__thumbnail__img")
            image_url = image_element["src"] if image_element.has_attr("src") else image_element["data-src"]
            product_link_element = product_item.find("a", class_="u-block | u-text-14 3xl:u-text-[0.972vw] u-font-medium | u-extend-href")
            product_link = product_link_element["href"]

            send_to_discord(product_name, product_price, image_url, product_link)

    time.sleep(60 * 5)  # Vérifiez les nouveaux produits toutes les 5 minutes (modifiable selon vos préférences)


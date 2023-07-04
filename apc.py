import time
import requests
from bs4 import BeautifulSoup
from dhooks import Webhook, Embed

HOOK_URL = 'https://discord.com/api/webhooks/1124627340681551902/QM1T_hoo_Ta73VJOuBk57_cfNscB5bTyVIMThM6uHRAeb9hl_j7xR5aUfjys1AOK2FAt'
SITE_URL = 'https://www.apc.fr/soldes-30/men-sales/t-shirts-jeans.html'

def fetch_promotions():
    page = requests.get(SITE_URL)
    soup = BeautifulSoup(page.content, 'html.parser')

    ul = soup.find('ul', class_='product-list')
    items = ul.find_all('li', class_='product-item')

    promotions = []
    for item in items:
        promotion = {
            'link': item.find('a')['href'],
            'image': item.find('img', class_='product-image entered loaded exited')['src'],
            'name': item.find('span', class_='product-item-details').find('span', class_='product-name').text
        }
        promotions.append(promotion)

    return promotions

def send_to_discord(promotion):
    hook = Webhook(HOOK_URL)
    embed = Embed(
        description=f"[{promotion['name']}]({promotion['link']})",
        color=0x5CDBF0,
        timestamp='now'  
    )
    embed.set_image(promotion['image'])
    hook.send(embed=embed)

def main():
    seen_promotions = set()
    while True:
        promotions = fetch_promotions()
        for promotion in promotions:
            link = promotion['link']
            if link not in seen_promotions:
                send_to_discord(promotion)
                seen_promotions.add(link)
        time.sleep(60)  # Pause for 1 minute

if __name__ == "__main__":
    main()

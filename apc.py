from bs4 import BeautifulSoup
import requests
from discord_webhook import DiscordWebhook, DiscordEmbed
import schedule
import time

# Demander à l'utilisateur l'URL du site qu'il souhaite surveiller
url = input("Veuillez entrer l'URL du site à surveiller : ")

# Demander à l'utilisateur le webhook Discord où il souhaite recevoir les messages
webhook_url = input("Veuillez entrer l'URL de votre webhook Discord : ")

# Stockage des produits déjà vus
produits_vus = set()

def verifier_nouveaux_produits(initialisation=False):
    print("Vérification des nouveaux produits...")

    # Faire une requête GET au site
    response = requests.get(url)
    
    # Analyser le HTML de la page
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Trouver tous les éléments de produit sur la page
    produits = soup.find_all('li', {'class': 'product-item'})
    
    for produit in produits:
        # Récupérer les détails du produit
        nom = produit.find('span', {'class': 'product-name'}).text
        lien = produit.find('a', {'class': 'product-link'}).get('href')
        prix_avant_promo = produit.find('span', {'data-price-type': 'oldPrice'}).get('data-price-amount')
        prix_apres_promo = produit.find('span', {'data-price-type': 'finalPrice'}).get('data-price-amount')
        image = produit.find('img', {'class': 'product-image'}).get('data-src')
        
        # Si le produit n'a pas été vu auparavant, le notifier à Discord
        if nom not in produits_vus:
            produits_vus.add(nom)

            if not initialisation:
                print(f"Nouveau produit détecté : {nom}")

                # Créer un embed Discord avec les détails du produit
                embed = DiscordEmbed(title=nom, description=f"Prix avant promo : {prix_avant_promo}€\nPrix après promo : {prix_apres_promo}€", color=242424, url=lien)
                embed.set_image(url=image)
                
                # Envoyer le message à Discord
                webhook = DiscordWebhook(url=webhook_url)
                webhook.add_embed(embed)
                webhook.execute()
            else:
                print(f"Produit ajouté à la liste initiale : {nom}")

print("Initialisation de la liste de produits...")
verifier_nouveaux_produits(initialisation=True)

print("Initialisation terminée. Commencement des vérifications régulières.")

# Ensuite, exécuter la fonction toutes les 10 minutes
schedule.every(10).minutes.do(verifier_nouveaux_produits)

while True:
    schedule.run_pending()
    time.sleep(1)

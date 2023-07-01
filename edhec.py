import requests
from bs4 import BeautifulSoup
import time
from discord_webhook import DiscordWebhook, DiscordEmbed

url = "https://www.edhec.edu/fr/programmes/grande-ecole/admissions-et-financement/voies-admission/resultats-admission"

webhook_url = "https://discord.com/api/webhooks/1124627340681551902/QM1T_hoo_Ta73VJOuBk57_cfNscB5bTyVIMThM6uHRAeb9hl_j7xR5aUfjys1AOK2FAt"

# L'intervalle de temps entre chaque vérification, en secondes
interval = 600

# La dernière valeur du nombre que nous avons vue
last_count = None

while True:
    print(f"Vérification de la valeur sur {url}...")
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Trouver l'élément avec l'ID "ancre-42823" et naviguer jusqu'à la balise span
    div = soup.find(id='ancre-42823')
    span = div.find('span')

    # Extraire le nombre
    count = int(span.text)
    print(f"La valeur actuelle est {count}.")

    # Si le nombre a changé depuis la dernière fois, envoyer un webhook
    if last_count is None or count != last_count:
        print(f"La valeur a changé, envoi du webhook...")
        webhook = DiscordWebhook(url=webhook_url)
        embed = DiscordEmbed(title='Liste d\'attente Edhec', description=f'Le nombre a changé : {count}', color='FF0000')
        embed.set_thumbnail(url='https://upload.wikimedia.org/wikipedia/fr/thumb/5/53/Logo_EDHEC_Business_School.svg/2560px-Logo_EDHEC_Business_School.svg.png')
        webhook.add_embed(embed)
        response = webhook.execute()
        last_count = count

    # Attendre l'intervalle spécifié avant de vérifier à nouveau
    print(f"Attente de {interval} secondes avant la prochaine vérification.")
    time.sleep(interval)

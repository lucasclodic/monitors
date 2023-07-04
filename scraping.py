import requests
import json
import time
from datetime import datetime

# Insérez vos URLs d'API ici
API_URLs = [
    'https://tickets.compagnie-oceane.fr/ws/?&func=liste_horaires&num_voyage=0&num_passage=1&server_celya=webb-ha1&_=1688483324811',
    'https://tickets.compagnie-oceane.fr/ws/?&func=liste_horaires&num_voyage=0&num_passage=1&server_celya=webb-ha3&_=1688483325475',
    'https://tickets.compagnie-oceane.fr/ws/?&func=liste_horaires&num_voyage=0&num_passage=1&server_celya=webb-ha3&_=1688483325493',
    'https://tickets.compagnie-oceane.fr/ws/?&func=liste_horaires&num_voyage=0&num_passage=1&server_celya=webb-ha3&_=1688483325501'
]

# Insérez votre URL de webhook Discord ici
WEBHOOK_URL = 'https://discord.com/api/webhooks/1125808344758747237/2OsjYw2sla1S3I_u7DadCSNeZRZmtzP-qzOXm8cP2r3fy4QKnQ-xGht8ANvxv7R03W7X'

# Stocke l'état actuel des places disponibles
current_state = {}

# Cookies
cookies = {
    "LS_PARAMS": "null",
    "LSAlert": "1",
    "PHPSESSID": "mo082g6e9k17k5hk6f69o9p2oh",
    "SERVERID": "webb-ha3",
    "tarteaucitron": "!facebookpixel=true!googleadwordsconversion=true!analytics=true!gtag=true"
}

# Flag pour la première exécution
first_run = True

while True:
    for API_URL in API_URLs:
        print("Interrogation de l'API...")
        response = requests.get(API_URL, cookies=cookies)
        data = response.json()

        for h in data['liste_horaires']:
            # Combinaison de date_depart et texte_heure_depart pour une clé unique
            unique_key = f"{h['date_depart']}-{h['texte_heure_depart']}"
            date_depart = datetime.strptime(h['date_depart'], '%Y%m%d').strftime('%d/%m/%Y')
            heure_depart = h['texte_heure_depart']
            places_dispos = int(h['places_dispos'])

            print(f"Analyse de la traversée {unique_key}...")

            if unique_key not in current_state:
                # C'est la première fois que nous voyons cette croisière, donc nous l'ajoutons à notre état actuel
                current_state[unique_key] = places_dispos
                print(f"Première observation de la traversée {unique_key}. Nombre de places disponibles: {places_dispos}")
            else:
                # Nous avons déjà vu cette croisière, alors vérifions si le nombre de places a changé
                old_places_dispos = current_state[unique_key]

                if old_places_dispos != places_dispos and not first_run:
                    # Le nombre de places a changé, donc nous envoyons un webhook à Discord
                    discord_data = {
                        'embeds': [{
                            'title': "Des places viennent de se vendre",
                            'color': 16711935,
                            'fields': [
                                {'name': 'Date', 'value': date_depart, 'inline': False},
                                {'name': 'Horaire', 'value': heure_depart, 'inline': False},
                                {'name': 'Nombre de places disponibles avant', 'value': str(old_places_dispos), 'inline': True},
                                {'name': 'Nombre de places disponibles désormais', 'value': str(places_dispos), 'inline': True}
                            ],
                            'thumbnail': {'url': 'https://www.compagnie-oceane.fr/wp-content/themes/altibus/framework/website/assets/img/logo_compagnie_oceane.png'},
                        }]
                    }
                    print(f"Envoi d'un webhook à Discord: {discord_data['embeds'][0]['title']}")
                    requests.post(WEBHOOK_URL, json=discord_data)

                    # Met à jour l'état actuel avec le nouveau nombre de places
                    current_state[unique_key] = places_dispos

        # Mark first_run as False after the initial state recording
        first_run = False

        # Attend 60 secondes avant de vérifier à nouveau
        print("Attente de 60 secondes avant la prochaine vérification...\n")
        time.sleep(60)

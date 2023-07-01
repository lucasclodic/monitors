import requests
from bs4 import BeautifulSoup

url = "https://www.edhec.edu/fr/programmes/grande-ecole/admissions-et-financement/voies-admission/resultats-admission"

response = requests.get(url=url)

# Imprimer le statut de la réponse
print(response.status_code)

# Imprimer l'intégralité de la réponse
print(response.text)

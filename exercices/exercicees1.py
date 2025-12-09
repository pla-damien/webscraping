#Site : http://quotes.toscrape.com (site d'entraînement)

#Tâches 1. Récupérer la page d'accueil avec Requests '
#'2. Afficher le code de statut '
#'3. Afficher les 500 premiers caractères du HTML '
#'4. Vérifier l'encodage de la page 
# 5. Afficher les headers de la réponse
#  6. Récupérer le robots.txt du site 
# 7. Bonus : Utiliser une session pour faire 3 requêtes successives
from urllib.robotparser import RobotFileParser
import requests
import time
import random

BASE_URL = "http://quotes.toscrape.com"

response = requests.get(BASE_URL)

print("Code HTTP :", response.status_code)

print(response.text[:500])

print("Encodage : ",response.encoding)

print("Header", response.headers)

rp = RobotFileParser
rp.set_url = ''
urls = ['http://quotes.toscrape.com/,'
'http://quotes.toscrape.com/tag/abilities/page/1/',
'http://quotes.toscrape.com/tag/books/page/1/']


for url in urls:
    response = requests.get(url)
    print(f"Scraped: {url} (code HTTP {response.status_code})")

    delay = random.uniform(1, 3)
    print(f"Pause de {delay:.2f} secondes...")
    time.sleep(delay)
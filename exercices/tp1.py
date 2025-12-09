import requests
from requests.exceptions import RequestException, Timeout, ConnectionError
import os
import pandas as pd 
import time

BASE_URL = "http://quotes.toscrape.com"
BASE_URL_PAGE = "http://quotes.toscrape.com/page/"
#TP 1 - Scraper basique
#Objectif : Créer un scraper simple avec Requests
#Site : http://quotes.toscrape.com
#Mission 1. Créer une fonction fetch_page(url) avec gestion d'erreurs 
def fetch_page(url):
    session = requests.Session()

    try:
        response = session.get(url)

        response.raise_for_status()
        return response
        print(f"Timeout pour {url}")
        return None

    except ConnectionError:
        print(f"Erreur de connexion pour {url}")
        return None

    except requests.exceptions.HTTPError:
        # On peut accéder au code HTTP via response.status_code
        print(f"Erreur HTTP {response.status_code}: {url}")
        return None

    except RequestException as e:
        # Regroupe les autres erreurs possibles (ex: URL invalide)
        print(f"Erreur générale: {e}")
        return None 
log = []
# 2. Scraper les 3 premières pages du site 
for num in range(1,4):
    delay = time.time() 
    url=f"{BASE_URL_PAGE}{num}/"
    reponse = fetch_page(url)
    delay = time.time() - delay
    # 3. Pour chaque page, extraire le HTML brut
    print(reponse.text)
    # 4. Compter le nombre de caractères de chaque page 
    print("Nombre de caractères :", len(reponse.text))

    # 5. Sauvegarder chaque page dans un fichier HTML 
    filepath=f"page{num}.html"
    with open(filepath,"w",encoding='utf-8') as f :
        f.write(reponse.text)

    log.append({ 
        "url" : url,
        "Status HTTP" : reponse.status_code,
        "Taille" : len(reponse.content),
        "Temps de réponse" : round(delay)
    })

    time.sleep(1)

# 6. Créer un rapport CSV avec : - URL de la page - Statut HTTP - Taille en octets - Temps de réponse
df = pd.DataFrame(log)
df.to_csv("rappor.csv") 
#Contraintes - Utiliser une session - Ajouter un délai de 1 seconde entre requêtes - Gérer les erreurs proprement

#Bonus - Logger les étapes



    

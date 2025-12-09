import requests
from requests.exceptions import RequestException, Timeout, ConnectionError
import os
import pandas as pd 
import time
from src.utils.logger import setup_logger

BASE_URL = "http://quotes.toscrape.com"
BASE_URL_PAGE = "http://quotes.toscrape.com/page/"
log_file = "/logs/log"

#TP 1 - Scraper basique
#Objectif : Créer un scraper simple avec Requests
#Site : http://quotes.toscrape.com
#Mission 1. Créer une fonction fetch_page(url) avec gestion d'erreurs 
def fetch_page(url,logger):
    try:
        logger.info(f"Début de la requète sur {url}")
        session = requests.Session()
        response = session.get(url)

        response.raise_for_status()
        logger.info(f"Fin de la requète sur {url}")
        return response
       

    except ConnectionError:
        logger.error(f"Erreur de connexion pour {url}")
        return None

    except requests.exceptions.HTTPError:
        # On peut accéder au code HTTP via response.status_code
        logger.error(f"Erreur HTTP {response.status_code}: {url}")
        return None

    except RequestException as e:
        # Regroupe les autres erreurs possibles (ex: URL invalide)
        logger.error(f"Erreur générale: {e}")
        return None 
    


logger = setup_logger("ETL_API", "logs/etl_api.log")
log = []
# 2. Scraper les 3 premières pages du site 
for num in range(1,4):
    delay = time.time() 
    url=f"{BASE_URL_PAGE}{num}/"
    reponse = fetch_page(url,logger)
    delay = time.time() - delay
    # 3. Pour chaque page, extraire le HTML brut
    print(reponse.text)
    # 4. Compter le nombre de caractères de chaque page 
    print("Nombre de caractères :", len(reponse.text))

    # 5. Sauvegarder chaque page dans un fichier HTML 
    filepath=f"data/output/page{num}.html"
    with open(filepath,"w",encoding='utf-8') as f :
        logger.info(f"Creation du fichier {filepath}")
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
df.to_csv("logs/rappor.csv") 
#Contraintes - Utiliser une session - Ajouter un délai de 1 seconde entre requêtes - Gérer les erreurs proprement

#Bonus - Logger les étapes



    

from logger import setup_logger
import requests
from requests.exceptions import RequestException, Timeout, ConnectionError
from bs4 import BeautifulSoup
import json

BASE_URL = "http://quotes.toscrape.com"

def fetch_page(url,session,logger):
    try:
        logger.info(f"Debut de connection à {BASE_URL} ")
        response = session.get(url)
        logger.info(f"Fin de connection à {BASE_URL} ")
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


#Tâches 1. Récupérer la page d'accueil
logger = setup_logger("webscrap", "webscrap.log") 
session = requests.Session()
response= fetch_page(BASE_URL,session,logger).text

#2. Parser avec BeautifulSoup
soup=BeautifulSoup(response,"lxml")
# print(soup)

#3. Trouver toutes les citations (class="quote") ''
quotes = soup.select(".quote")
print("citations class=quote",quotes)

#4. Pour chaque citation, extraire : - Le texte de la citation - L'auteur - Les tags 
for quote in quotes:
    text = quote.select_one(".text").get_text()
    auteur = quote.select_one(".author").get_text()
    tags = quote.select(".tags")


# 5. Afficher les 5 premières citations 
top_5 = soup.select(".quote",limit=5)
for quote in top_5:
    print(quote.select_one(".text").get_text())

#6. Compter le nombre total de citations sur la page 
nb_citatations = len(soup.select(".quote"))
print(f"Il y a {nb_citatations} citations. ")

#7. Créer une liste de dictionnaires avec les données
list_citation = []
for quote in quotes:
    text = quote.select_one(".text").get_text()
    auteur = quote.select_one(".author").get_text()
    tags = quote.select(".tag")
    list_tag=[]
    for tag in tags:
        list_tag.append(tag.get_text())

    print(text,auteur,list_tag)
    list_citation.append({
        "text" : text,
        "Auteur" : auteur,
        "tag" : list_tag
    })


#Exercice - BeautifulSoup basique
#Objectif : Extraire des données avec BeautifulSoup

#Site : http://quotes.toscrape.com



#8. Bonus : Sauvegarder dans un fichier JSON
import json

# 8. Bonus : Sauvegarder dans un fichier JSON
with open("citations.json", "w", encoding="utf-8") as f:
    json.dump(list_citation, f)
    logger.info("Fichier Json créé")



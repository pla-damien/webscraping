from bs4 import BeautifulSoup
import requests
from requests.exceptions import RequestException, Timeout, ConnectionError
from src.utils.logger  import setup_logger
import pandas as pd
import os
import time 
# TP 2 - Scraper multi-pages
# Objectif : Scraper plusieurs pages avec pagination

BASE_URL = "http://quotes.toscrape.com"
# Site : http://quotes.toscrape.com

def fetch_page(url,session,logger):
    try:
        logger.info(f"Debut de connection à {url} ")
        response = session.get(url)
        logger.info(f"Fin de connection à {url} ")
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

def next_url(soup):
    if soup.find(class_=("next")):
        next_page = soup.find(class_=("next")).find("a")["href"]
        return next_page
    else:
        return None
    
def max_page(soup):
    list_soup = []
    compteur = 2
    next_page = soup.find(class_=("next")).find("a")["href"]
    url = f"{BASE_URL}{next_page}"
    response= fetch_page(url,session,logger).text
    soup = BeautifulSoup(response,"lxml")
    # while soup.find(class_=("next")):
    while next_url(soup):
        next_page = soup.find(class_=("next")).find("a")["href"]
        url = f"{BASE_URL}{next_page}"
        soup=scrap_soup(url)
        list_soup.append(soup)
        # logger.info(f"La page {compteur} éxiste !")
        compteur += 1
        
    
    # logger.info(f"La page {compteur+1} n'existe pas !")
    return list_soup

def to_one_df(list):
    df = pd.DataFrame(list[0])
    for dict in list[1:]:
        df2 = pd.DataFrame(dict)
        df = pd.DataFrame.merge(df,df2)
    df = pd.DataFrame(list)
    df = df.drop_duplicates(keep = 'first', inplace=True)
    return df

def scrap_soup(url):
    response= fetch_page(url,session,logger).text
    soup = BeautifulSoup(response,"lxml")
    return soup


def recup_quotes(soup):
    all_quotes = soup.find_all(class_=("quote"))
    return all_quotes


    

logger = setup_logger("webscrap","logs/webscrap.log")
session = requests.Session()
response= fetch_page(BASE_URL,session,logger).text
soup = BeautifulSoup(response,"lxml")


# Mission Créer un scraper complet qui : 
# 1. Détecte automatiquement le nombre de pages 
max_page(soup)
# 2. Scrape toutes les pages (jusqu'à 10 max) 
all_page = max_page(soup)
all_quotes_info = []
# 3. Pour chaque citation, extrait : - Texte - Auteur - Tags - URL de l'auteur 
for page in all_page:
    all_quotes = recup_quotes(page)
    print(len(all_quotes))
    for quote in all_quotes:
        all_quotes_info.append({
            "Texte": quote.find(class_=("text")).get_text(),
            "Auteur": quote.find(class_=("author")).get_text(),
            "Tags": quote.find("meta")["content"],
            "URL" : quote.find("a")["href"]
        })

# 4. Crée un fichier Excel avec 3 feuilles : - "Citations" : Toutes les citations - 
# "Auteurs" : Liste unique des auteurs avec nb de citations 
# - "Tags" : Liste des tags avec fréquence 
df = pd.DataFrame(all_quotes_info)
df_author_count = df.groupby("Auteur")["Texte"].count().reset_index()
df3=df.groupby("Tags")["Texte"].count().reset_index()
df3.columns = ["Tags","nb"]
with pd.ExcelWriter('output/Citations.xlsx',engine='openpyxl') as writer:
        df["Texte"].to_excel(writer,sheet_name="Citations",index=False)
        df_author_count.to_excel(writer,sheet_name="Auteurs",index=False)
        df3.to_excel(writer,sheet_name="Tags",index=False)



# 5. Génère des statistiques : - Top 5 auteurs les plus cités 
# - Top 10 tags les plus utilisés 
# - Longueur moyenne des citations
top_author = df_author_count.nlargest(5,"Texte")

# Contraintes - Code modulaire (fonctions) - Gestion d'erreurs complète - Logging - Respect du délai entre requêtes
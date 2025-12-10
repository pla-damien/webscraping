from bs4 import BeautifulSoup
import requests
from requests.exceptions import RequestException, Timeout, ConnectionError
from src.utils.logger import setup_logger
import pandas as pd
import os

BASE_URL = "http://books.toscrape.com"

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

def convert_note(note,logger):
    match note :
        case "One":
            return 1
        case "Two":
            return 2
        case "Three":
            return 3
        case "Four":
            return 4
        case "Five":
            return 5
        case _:
            logger.error("Note inconnue !!!")

def download_image(image_url, save_path):
    response = requests.get(image_url)
    # Création du dossier si nécessaire
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    with open(save_path, "wb") as f:
        f.write(response.content)

# Exercice - Scraping de livres
# Objectif : Scraper un catalogue de livres

# Site : http://books.toscrape.com

# Tâches 1. Récupérer la page d'accueil '
logger = setup_logger("webscrap", "logs/webscrap.log") 
session = requests.Session()
response= fetch_page(BASE_URL,session,logger).text
soup = BeautifulSoup(response,"lxml")

# '2. Pour chaque livre sur la page, extraire : - Titre - Prix (convertir en float) - Note (étoiles → nombre) - Disponibilité (In stock / Out of stock) - URL de l'image 
list_product = soup.find_all(class_="product_pod")

# print(list_product)
books = []
for product in list_product:
    title = product.find("h3").find("a")["title"]
    price = product.find(class_=("product_price")).find(class_="price_color").get_text()
    note = product.find("p")["class"][1]
    stock = product.find(class_=("instock availability")).get_text()
    url_image = product.find(class_=("thumbnail"))["src"]
    books.append({
        "titre" : title,
        "price" : float(price[2:]),
        "note" : convert_note(note,logger),
        "stock" : stock.strip(),
        "image" : url_image
    })
 
# 3. Créer un DataFrame Pandas par note 
df = pd.DataFrame(books)
df = df.sort_values("note",ascending=False)
df = df.reset_index()
# print(df)

# 5. Sauvegarder dans books.csv 
df.to_csv("data/output/books.csv")
# 4. Calculer : - Prix moyen 
avg_price = df["price"].mean()

# - Livre le plus cher 
most_exp = df.nlargest(1,"price")

# - Livre le moins cher - Répartition
less_exp = df.nsmallest(1,"price")

# 6. Bonus : Télécharger l'image du livre le plus cher
url_image = f"{BASE_URL}/{most_exp["image"].values[0]}"
download_image(url_image,"data/output/image.jpg")
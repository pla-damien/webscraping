import requests
import time
# # Exercice : Récupérer et analyser une page web

# **Site** : http://quotes.toscrape.com (site d'entraînement)

# config
url = "http://quotes.toscrape.com"
mon_headers = {
    'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

# **Tâches**
# 1. Récupérer la page d'accueil avec Requests
response = requests.get(url,headers=mon_headers)

# 2. Afficher le code de statut
print(f"Code Statut : {response.status_code}")

# 3. Afficher les 500 premiers caractères du HTML
print(f"500 premiers caractères du HTML: {response.text[:500]}")

# 4. Vérifier l'encodage de la page
print(f"encodage de la page : {response.encoding}")

# 5. Afficher les headers de la réponse
print(f"headers de la réponse : {response.headers}")

# 6. Récupérer le robots.txt du site
robot_url = f"{url}/robots.txt"
robot_response = requests.get(robot_url)
print(f"robots.txt : {robot_response.text}")

# 7. **Bonus** : Utiliser une session pour faire 3 requêtes successives
session = requests.Session()
session.headers.update(mon_headers)

pages = ["/","/page/2/","/tag/love/"]
for page in pages:
    full_url = url + page
    resp = session.get(full_url)
    print(f"Page : {page}, statut code : {resp.status_code}")
    time.sleep(1)

session.close()
## TP 1 - Scraper basique

**Objectif** : Créer un scraper simple avec Requests

**Site** : http://quotes.toscrape.com

**Mission**
1. Créer une fonction `fetch_page(url)` avec gestion d'erreurs
2. Scraper les 3 premières pages du site
3. Pour chaque page, extraire le HTML brut
4. Compter le nombre de caractères de chaque page
5. Sauvegarder chaque page dans un fichier HTML
6. Créer un rapport CSV avec :
   - URL de la page
   - Statut HTTP
   - Taille en octets
   - Temps de réponse

**Contraintes**
- Utiliser une session
- Ajouter un délai de 1 seconde entre requêtes
- Gérer les erreurs proprement

**Bonus**
- Logger les étapes
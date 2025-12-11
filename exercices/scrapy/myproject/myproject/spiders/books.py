import scrapy
from myproject.items import BookItems
# Exercice - Scrapy
# Objectif : Créer un spider Scrapy complet

# Site : http://books.toscrape.com

# Tâches 1. Créer un projet Scrapy bookstore 
# 2. Créer un spider books 
# 3. Définir un BookItem avec : title, price, rating, availability 
# 4. Scraper la première page 
# 5. Extraire tous les livres avec leurs informations 
# 6. Exporter en JSON et CSV 
# 7. Bonus : Ajouter la pagination (3 pages max)

class BooksSpider(scrapy.Spider):
    name = "books"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["http://books.toscrape.com"]
    max_page = 3
    compteur = 0
    def parse(self, response):
        books = response.css("article.product_pod")
        #Si pas book continue
        for book in books:
            item=BookItems()
            item["title"] = book.css("a::text").get()
            item["price"] = book.css("p.price_color::text").get()
            item["ratin"] = book.css("p::attr(class)").get()
            avai = book.css("p.instock::text").getall()
            item["availability"] = " ".join(avai[1].split())
            yield item
    
        # Suivre le lien "Next"
        next_page = response.css('li.next a::attr(href)').get()
        if next_page:
            self.compteur +=1
            while self.compteur < self.max_page:
                yield response.follow(next_page, self.parse) 
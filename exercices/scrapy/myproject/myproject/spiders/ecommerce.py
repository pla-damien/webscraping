import scrapy
from myproject.items import BookItems

class EcommerceSpider(scrapy.Spider):
    name = "ecommerce"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["http://books.toscrape.com"]

    def parse(self, response):
        books = response.css("article.product_pod")

        #Si pas de book continue
        for book in books:
            item=BookItems()
            item["title"] = book.css("a::text").get()
            item["price"] = book.css("p.price_color::text").get()
            item["ratin"] = book.css("p::attr(class)").get()
            avai = book.css("p.instock::text").getall()
            item["availability"] = " ".join(avai[1].split())
         
        #si next_page exist on recupere + yeild + changement de page/livre
        next_page = book.css("div.image_container a::attr(href)").get()
        next_page = f"{self.start_urls[0]}/{next_page}"
        print("Next page : ", next_page)
        if next_page:
            item["Catégories"] = book.css("a::text").get()
            item["avis"] = book.css("table.table")
            print("ITEMS : ",item)
            yield item
            
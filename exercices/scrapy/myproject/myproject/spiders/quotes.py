import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["https://quotes.toscrape.com"]

    def parse(self, response):
        quotes = response.css("div.quote")

        for quote in quotes:
            text = quote.css("span.text::text").get()
            author = quote.css("small.author::text").get()
            tags = quote.css("a.tag::text").getall()

            yield {
                "text" : text,
                "author" : author,
                "tags" : tags,
            }

# commande pour lancer ce spider
# scrapy crawl quotes => infos dans le terminal
# scrapy crawl quotes -O outputs/quotes_basic.json
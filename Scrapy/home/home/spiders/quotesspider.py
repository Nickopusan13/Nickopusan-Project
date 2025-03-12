import scrapy
from home.items import QuoteItem

class QuotesspiderSpider(scrapy.Spider):
    name = "quotesspider"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["https://quotes.toscrape.com/"]

    def parse(self, response):
        quote_table = response.css('div.quote')
        for quote in quote_table:
            quote_item = QuoteItem()
            quote_item['quote'] = quote.css('span::text').get()
            quote_item['author'] = quote.css('span small.author::text').get()
            yield quote_item
        
        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            next_page_url = "https://quotes.toscrape.com/" + next_page
        yield response.follow(next_page_url, callback=self.parse)

import scrapy


class HealthSpider(scrapy.Spider):
    name = "health"
    allowed_domains = ["reportcards.ncqa.org"]
    start_urls = ["https://reportcards.ncqa.org/health-plans?pg=1"]

    def parse(self, response):
        pass



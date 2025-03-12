import scrapy
from home.items import ImdbItem
from scrapy_playwright.page import PageMethod

class ImdbSpider(scrapy.Spider):
    name = "imdb"

    def start_requests(self):
        url = "https://www.imdb.com/chart/top/?ref_=nv_mv_250"
        yield scrapy.Request(url, meta={'playwright': True, 'playwright_page_methods':[PageMethod('wait_for_selector', 'li.ipc-metadata-list-summary-item')]})
    
    def parse(self, response):
        movies = response.css('li.ipc-metadata-list-summary-item')
        for movie in movies:
            relative_url = movie.css('div.ipc-title a::attr(href)').get()
            if relative_url is not None:
                movie_url = "https://www.imdb.com" + relative_url
            yield response.follow(movie_url, callback=self.parse)
            
    def parse_movie_page(self, response):
        imdb_item = ImdbItem()
        imdb_item['title'] = response.css('h1 span::text').get()
        imdb_item['rating'] = response.css('span.sc-d541859f-1::text').get()
        imdb_item['year'] = response.xpath('//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[2]/div[1]/ul/li[1]/a/text()').get()
        imdb_item['description'] = response.css('span.sc-42125d72-1::text').get()
        imdb_item['director'] = response.xpath('//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[3]/div[2]/div[1]/section/div[2]/div/ul/li[1]/div/ul/li/a/text()').getall()
        imdb_item['writers'] = response.xpath('//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[3]/div[2]/div[1]/section/div[2]/div/ul/li[2]/div/ul/li/a/text()').getall()
        imdb_item['stars'] = response.xpath('//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[3]/div[2]/div[1]/section/div[2]/div/ul/li[3]/div/ul/li/a/text()').getall()
        yield imdb_item

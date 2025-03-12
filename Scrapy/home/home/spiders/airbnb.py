import scrapy
from home.items import AirbnbItem
from scrapy_playwright.page import PageMethod

class AirbnbSpider(scrapy.Spider):
    name = "airbnb"
    
    def start_requests(self):
        url = "https://www.airbnb.com/s/Bandung/homes?refinement_paths%5B%5D=%2Fhomes"
        yield scrapy.Request(url, meta={
            'playwright': True, 
            'playwright_page_methods': [
                PageMethod('wait_for_selector', 'div.c4mnd7m'), 
                PageMethod('evaluate', 'window.scrollBy(0, document.body.scrollHeight)'),
                PageMethod('wait_for_timeout', 3000),
                PageMethod('evaluate', 'window.scrollBy(0, document.body.scrollHeight)'),
                PageMethod('wait_for_timeout', 3000)
            ], 
            'playwright_include_page': True,
        })
        
    async def parse(self, response):
        room_url = response.xpath("//div[@data-testid='card-container']//a[contains(@href, '/rooms/')]/@href").getall()
        for room in room_url:
            if room:
                full_url = 'https://www.airbnb.com' + room
                yield scrapy.Request(full_url, callback=self.parse_airbnb_page, meta={
                    'playwright': True, 'playwright_page_methods': [
                        PageMethod('wait_for_selector', 'div._1czgyoo'),
                        PageMethod('wait_for_timeout', 3000)]})
            else:
                print("******* Room URL not found! *******")
        
        next_page = response.css('a[aria-label="Next"]::attr(href)').get()
        if next_page:
            next_page_url = "https://www.airbnb.com" + next_page
            yield scrapy.Request(next_page_url, callback=self.parse, meta={'playwright': True, 'playwright_page_methods': [
                PageMethod('wait_for_selector', 'a[aria-label="Next"]'),
                PageMethod('wait_for_timeout', 2500)]})
        else:
            print("########## No more pages ##########")
        
    async def parse_airbnb_page(self, response):
        airbnb_item = AirbnbItem()
        airbnb_item['url'] = response.url
        airbnb_item['name'] = response.css('div._1czgyoo h1::text').get()
        airbnb_item['title'] = response.css('section div.toieuka h2::text').get()
        airbnb_item['price'] = response.css('span._hb913q::text').get()
        airbnb_item['price_discount'] = response.css('div._1jo4hgw span._4dhrua::text').get()
        airbnb_item['hosted_by'] = response.css('div.t1pxe1a4::text').get()
        airbnb_item['guest'] = response.xpath('//*[@id="site-content"]/div/div[1]/div[3]/div/div[1]/div/div[1]/div/div/div/section/div[2]/ol/li[1]/text()').get()
        airbnb_item['beds'] = response.xpath('//*[@id="site-content"]/div/div[1]/div[3]/div/div[1]/div/div[1]/div/div/div/section/div[2]/ol/li[3]/text()').get()
        airbnb_item['bedrooms'] = response.xpath('//*[@id="site-content"]/div/div[1]/div[3]/div/div[1]/div/div[1]/div/div/div/section/div[2]/ol/li[2]/text()').get()
        airbnb_item['baths'] = response.xpath('//*[@id="site-content"]/div/div[1]/div[3]/div/div[1]/div/div[1]/div/div/div/section/div[2]/ol/li[4]/text()').get()
        airbnb_item['reviews'] = response.css('div.rk4wssy a.l1ovpqvx::text').get() or response.css('div.rddb4xa div.r16onr0j::text').get()
        airbnb_item['stars'] = response.xpath('//*[@id="site-content"]/div/div[1]/div[3]/div/div[1]/div/div[1]/div/div/div/section/div[3]/div[2]/text()').get() or response.css('div.a8jhwcl div::text').get()
        yield airbnb_item
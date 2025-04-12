import scrapy
import re
import json
import os
from centris.items import CentrisItem
from scrapy_playwright.page import PageMethod

class CentrisSpiderSpider(scrapy.Spider):
    name = "centris_spider"
    allowed_domains = ["www.centris.ca"]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'config.json')
        with open(config_path, encoding='utf-8') as f:
            self.config = json.load(f)

        self.start_url = self.config.get("url_address")
        self.username = self.config.get("user_name")
        self.password = self.config.get("user_password")
        self.scraped_ids = set(self.config.get("already_scrape_id", []))
        
    def start_requests(self):
        login_url = "https://www.centris.ca/en/login?uc=1"
        yield scrapy.Request(login_url, callback=self.filter_url, meta={
            'playwright': True,
            'playwright_page_methods': [
                # PageMethod("click", 'button:has-text("Accept and continue")'), # Uncomment if headless is false 
                PageMethod("fill", 'input[type="text"]', self.config["user_name"]),
                PageMethod("fill", 'input[type="password"]', self.config["user_password"]),
                PageMethod("click", 'input[type="submit"]'),
                PageMethod("wait_for_timeout", 5000),
            ]
        })

    def filter_url(self, response):
        start_url = "https://www.centris.ca/en/my-searches"
        yield scrapy.Request(start_url, callback=self.search_item, meta={
            'playwright': True,
            'playwright_page_methods': [
                PageMethod("wait_for_selector", 'div.region div.saved-search-criteria'),
                PageMethod("evaluate", "window.scrollBy(0, document.body.scrollHeight);"),
                PageMethod("wait_for_timeout", 5000),
            ]
        })

    def search_item(self, response):
        search_url = response.css('div.region div.saved-search-criteria')
        self.logger.info(f"Found {len(search_url)} saved searches.")
        for search in search_url:
            url = search.css('div.cta-section a.btn.btn-primary::attr(href)').get()
            if url:
                full_url = response.urljoin(url)
                yield scrapy.Request(full_url, callback=self.parse, meta={
                    'playwright': True,
                    'playwright_include_page': True,
                    'playwright_page_methods': [
                        PageMethod("wait_for_selector", 'div.property-thumbnail-item'),
                        PageMethod("evaluate", "window.scrollBy(0, document.body.scrollHeight);"),
                        PageMethod("wait_for_timeout", 5000),
                    ]
                })
                
    async def parse(self, response):
        page = response.meta['playwright_page']
        try:
            centris_property = response.css('div.property-thumbnail-item')
            self.logger.info(f"Found {len(centris_property)} properties on this page.")
            for prop in centris_property:
                item = CentrisItem()
                url = prop.css('div.thumbnail.property-thumbnail-feature.legacy-reset a.property-thumbnail-summary-link::attr(href)').get()
                item['url'] = response.urljoin(url)
                item['id'] = item['url'].split('/')[-1].split('?')[0]
                item['image_urls'] = prop.css('div.thumbnail.property-thumbnail-feature.legacy-reset img[itemprop="image"]::attr(src)').getall()
                price_full = prop.css('div.price *::text').getall()
                item['price'] = ' '.join([p.strip() for p in price_full if p.strip()])
                item['banner'] = prop.css('div.banner::text').get()
                item['bedroom'] = prop.css('div.d-flex.justify-content-between.align-items-end.bottom div.cac::text').get()
                item['bathroom'] = prop.css('div.d-flex.justify-content-between.align-items-end.bottom div.sdb::text').get()
                raw_rev = prop.css('div.d-flex.justify-content-between.align-items-end.bottom div.plex-revenue span::text').get()
                if raw_rev:
                    match = re.search(r'[\d,.]+\s*\$', raw_rev)
                    item['pot_gross_rev'] = match.group(0) if match else None
                else:
                    item['pot_gross_rev'] = None
                item['land_area'] = prop.css('div.d-flex.justify-content-between.align-items-end.bottom div.land-area::text').get()
                item['title'] = prop.css('div.location-container div.category div::text').get()
                features_text = prop.css('div.features *::text').getall()
                features_text = [t.strip() for t in features_text if t.strip()]
                property_types = [
                    t for t in features_text
                    if not any(char.isdigit() for char in t) and t != "?"
                ]
                item['property_type'] = ' | '.join(property_types) if property_types else None
                for prop in response.css('div.property-thumbnail-item'):
                    address_parts = prop.css('div.address > div::text').getall()
                    item['address'] = ' '.join([part.strip() for part in address_parts if part.strip()])
                yield item
                self.logger.info(f"Scraped ID: {item['id']}")
            

            next_button = page.locator('ul.pager li.next').first
            if await next_button.count() > 0:
                next_button_class = await next_button.get_attribute("class")
                if "inactive" not in next_button_class:
                    self.logger.info("Clicking to next page...")
                    await next_button.click()
                    await page.wait_for_timeout(1000)
                    await page.wait_for_selector('div.property-thumbnail-item')

                    content = await page.content()
                    next_response = response.replace(body=content)

                    async for item in self.parse(next_response):
                        yield item
                else:
                    self.logger.info("Next button is inactive — reached the last page.")
            else:
                self.logger.info("No more pages to process.")
        finally:
            await page.close()
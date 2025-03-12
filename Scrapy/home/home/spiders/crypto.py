import scrapy
from scrapy_playwright.page import PageMethod
from home.items import CryptoItem
from scrapy.http import HtmlResponse


class CryptoSpider(scrapy.Spider):
    name = "crypto"
    
    def start_requests(self):
        url = "https://www.tradingview.com/markets/cryptocurrencies/prices-all/"
        yield scrapy.Request(url, meta={
        'playwright': True, 
        'playwright_page_methods': [
            PageMethod('wait_for_selector', 'tbody tr.row-RdUXZpkv'), 
            PageMethod('evaluate', 'window.scrollBy(0, document.body.scrollHeight)'),
            PageMethod('wait_for_timeout', 10000)
        ], 
        'playwright_include_page': True,
})
    
    async def parse(self, response):
        page = response.meta['playwright_page']
        while True:
            try:
                load_more = await page.query_selector('//*[@id="js-category-content"]/div[2]/div/div[4]/div[3]/button')
                if load_more:
                    await load_more.click()
                    self.logger.info("Clicked Load More")
                    await page.wait_for_timeout(3000)  # Tunggu konten baru dimuat
                else:
                    self.logger.info("No More Page To Load")
                    break
            except Exception as e:
                self.logger.info(f"Error saat mencoba klik Load More: {e}")
                break

        await page.wait_for_timeout(2000)
        content = await page.content()
        response = response.replace(body=content)

        crypto_item = CryptoItem()
        crypto_information = response.css('tbody tr.row-RdUXZpkv')
        for crypto in crypto_information:
            crypto_item['rank'] = crypto.css('td.cell-RLhfr_y4::text').get()
            crypto_item['initial'] = crypto.css('span.tickerCell-GrtoTeat a.apply-common-tooltip::text').get()
            crypto_item['name'] = crypto.css('span.tickerCell-GrtoTeat sup.apply-common-tooltip::text').get()
            crypto_item['price'] = crypto.css('td:nth-child(3)::text').get()
            crypto_item['change_percentage'] = crypto.css('td:nth-child(4) *::text').get()
            crypto_item['market_cap'] = crypto.css('td:nth-child(5)::text').get()
            crypto_item['volume'] = crypto.css('td:nth-child(6)::text').get()
            crypto_item['circ_supply'] = crypto.css('td:nth-child(7)::text').get()
            yield crypto_item
        await page.close()
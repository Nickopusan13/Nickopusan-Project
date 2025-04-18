from playwright.async_api import async_playwright
import csv
import os
import re

class GoogleMapsScraper:
    def __init__(self, progress_callback=None):
        self.seen_names = set()
        self.progress_callback = progress_callback
        self.url = "https://www.google.com/maps?hl=en"
        self.output_dir = r"C:\Freelance\Scrapy\pw_project\google_maps\output"
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        self.file_path = None

    def _sanitize_filename(self, name):
        sanitized = re.sub(r'[\\/*?:"<>|]', "_", name)
        return sanitized[:50]

    def _initialize_csv(self, search_query):
        base_name = self._sanitize_filename(search_query)
        self.file_path = os.path.join(self.output_dir, f"{base_name}.csv")
        
        with open(self.file_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Name', 'Rating', 'Review', 'Address', 'Price', 
                           'Phone Number', 'Website', 'Description', 'URL'])

    def write_to_csv(self, data):
        with open(self.file_path, 'a', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(data)

    async def start_url(self, search_query):
        self._initialize_csv(search_query)
        async with async_playwright() as playwright:
            browser = await playwright.chromium.launch(headless=True)
            context = await browser.new_context(
                locale='en-US', extra_http_headers={'Accept-Language': 'en-US,en;q=0.9'})
            page = await context.new_page()
            await page.goto(self.url)
            await page.fill("input#searchboxinput", search_query)
            await page.click("button#searchbox-searchbutton")
            await page.wait_for_selector("div.m6QErb div.Nv2PK.THOPZb.CpccDe")
            await self.scroll_page(page, 'div[role="feed"]')
    
    async def scroll_page(self, page, scroll_selector):
        feed = await page.query_selector(scroll_selector)
        while True:
            await feed.evaluate("el => el.scrollBy(0, el.scrollHeight)")
            await page.wait_for_timeout(2000)
            if await page.query_selector("div.PbZDve p.fontBodyMedium span span.HlvSq"):
                print("Reached the end of the page.")
                break
        await self.get_data(page)
    
    async def get_data(self, page):
        items = await page.query_selector_all("div.m6QErb div.Nv2PK.THOPZb.CpccDe")
        print(f"Total items: {len(items)}")
        for item in items:
            await item.click()
            await page.wait_for_timeout(2000)
            name = await self.safe_text(page, "h1.DUwDvf.lfPIob")
            
            if not name or name in self.seen_names:
                continue
                
            self.seen_names.add(name)
            
            if self.progress_callback:
                self.progress_callback(name)
            
            url = page.url
            rating = await self.safe_text(page, "div.skqShb span[aria-hidden='true']")
            review = await self.safe_text(page, "div.skqShb span[aria-label*='reviews']")
            address = await self.safe_text(page, "div.RcCsl.fVHpi.w4vB1d.NOE9ve.M0S7ae.AG25L div.rogA2c")
            price = await self.safe_text(page, "div.skqShb span.mgr77e")
            phone_number = await self.safe_text(page, "button[data-tooltip='Copy phone number'] div.rogA2c")
            website = await self.safe_attr(page, "div.RcCsl.fVHpi.w4vB1d.NOE9ve.M0S7ae.AG25L a.CsEnBe", "href")
            description = await self.safe_text(page, "div.WeS02d.fontBodyMedium div.PYvSYb")
            
            data_row = [name, rating, review, address, price, phone_number, website, description, url]
            self.write_to_csv(data_row)
            
            print(f"Name: {name}")
            print("========================================")

    async def safe_text(self, page, selector):
        try:
            element = await page.query_selector(selector)
            return await element.text_content() if element else None
        except:
            return None

    async def safe_attr(self, page, selector, attr):
        try:
            element = await page.query_selector(selector)
            return await element.get_attribute(attr) if element else None
        except:
            return None
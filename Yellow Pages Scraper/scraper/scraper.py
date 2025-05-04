from playwright.async_api import async_playwright
from playwright_stealth import stealth_async
from urllib.parse import urljoin
from middlewares import Middlewares
from cleaner import clean_phone
import asyncio
import csv
import os

class YellowPagesScraper:
    def __init__(self): 
        base_dir = os.path.dirname(os.path.abspath(__file__))
        output_dir = os.path.join(base_dir, ".." ,"output")
        os.makedirs(output_dir, exist_ok=True)
        self.filename = os.path.join(output_dir, "y1.csv")
        file_exists = os.path.isfile(self.filename)
        self.csv_file = open(self.filename, mode="a", newline="", encoding="utf-8")
        self.writer = csv.writer(self.csv_file)
        if not file_exists:
            self.writer.writerow(["Company", "Address", "Phone Number", "Website"])

    async def start(self, url):
        async with async_playwright() as playwright:
            self.browser = await playwright.firefox.launch(headless=True)
            await self.scrape_loop(url)
    
    async def scrape_loop(self, url):
        if hasattr(self, "context") and self.context:
            await self.context.close()
        self.headers, self.user_agents = Middlewares().get_random_headers()
        self.context = await self.browser.new_context(
            locale='en-US',
            user_agent=self.user_agents,
            extra_http_headers=self.headers
        )
        page = await self.context.new_page()
        await stealth_async(page)
        await page.goto(url, wait_until="networkidle")
        await page.wait_for_timeout(4000)
        await self.parse(page)
    
    async def parse(self, page):
        items = await page.query_selector_all("div.search-results.organic div.result")
        items_2 = await page.query_selector_all("ul.tappable-b li.business-card")
        if items:
            print(f"Number of items: {len(items)}")
            for item in items:
                company = await self.safe_text(item, "div.info-section.info-primary a.business-name span")
                phone_number = await self.safe_text(item, "div.info-section.info-secondary div.phones.phone.primary")
                address = await self.safe_text(item, "div.info-section.info-secondary div.adr")
                website = await self.safe_attr(item, "div.info-section.info-primary div.links a.track-visit-website", "href")
                data_row = [company, address, phone_number, website]
                self.writer.writerow(data_row)
        elif items_2:
            print(f"Number of items_2: {len(items_2)}")
            for item in items_2:
                company = await self.safe_text(item, "section.info h2.title.business-name")
                phone_number = clean_phone(await self.safe_attr(item, "div.business-card-footer a[itemprop='telephone']", "href"))
                address = await self.safe_text(item, "article.address-indicators div.address")
                website = await self.safe_attr(item, "div.business-card-footer a[itemprop='website']", "href")
                data_row = [company, address, phone_number, website]
                self.writer.writerow(data_row)
        else:
            print(f"Unknown Layout... Skipping {page}")
            html = await page.content()
            with open("output/debug_page.html", "w", encoding="utf-8") as f:
                f.write(html)
            print("🔍 Saved page HTML to output/debug_page.html for inspection.")
                
        next_page = await self.safe_attr(page, "div.pagination ul li a.next.ajax-page", "href")
        next_page_2 = await self.safe_attr(page, "div.paginator div.paginator-links a.paginator-next.arrow-next.active", "href")
        
        current_url = page.url
        next_page_url = None

        if next_page:
            next_page_url = urljoin(current_url, next_page)
        elif next_page_2:
            next_page_url = urljoin(current_url, next_page_2)

        if next_page_url:
            next_page_url = next_page_url.strip()
            print(f"Go To: {next_page_url}")
            if isinstance(next_page_url, str) and next_page_url.startswith("http"):
                await self.scrape_loop(next_page_url)
            else:
                print("❌ Skipping invalid URL")
        else:
            print("Next page not found....")

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

if __name__ == "__main__":
    url = "https://www.yellowpages.com/search?search_terms=Vacation+Rentals&geo_location_terms=Miami+Beach%2C+FL"
    asyncio.run(YellowPagesScraper().start(url))
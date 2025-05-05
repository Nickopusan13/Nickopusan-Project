from playwright.async_api import async_playwright
from playwright_stealth import stealth_async
from middlewares import Middlewares
from dotenv import load_dotenv
from urllib.parse import urljoin
import csv
import asyncio
import os

class AmazonScraper:
    def __init__(self):
        env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'key', '.env')
        base_dir = os.path.dirname(os.path.abspath(__file__))
        output_dir = os.path.join(base_dir, ".." ,"output")
        self.filename = os.path.join(output_dir, "y1.csv")
        file_exists = os.path.isfile(self.filename)
        self.csv_file = open(self.filename, mode="a", newline="", encoding="utf-8")
        self.writer = csv.writer(self.csv_file)
        if not file_exists:
            self.writer.writerow(["Title", "ASIN", "Url"])
        load_dotenv(env_path)
        self.email = os.getenv("AMAZON_EMAIL")
        self.password = os.getenv("AMAZON_PASSWORD")
        self.semaphore = asyncio.Semaphore(5)
        self.scraped_urls = set()
        
    async def start_url(self, url):
        async with async_playwright() as playwright:
            self.browser = await playwright.chromium.launch(headless=False)
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
        await page.wait_for_timeout(2000)
        await self.login(page)
    
    async def login(self, page):
        print("Login account....")
        await page.fill("input[type='email']", self.email)
        await page.click("input[type='submit']")
        await page.wait_for_selector("input[type='password']")
        await page.fill("input[type='password']", self.password)
        await page.click("input[type='submit']")
        await page.wait_for_timeout(3000)
        await self.search(page)
    
    async def search(self, page):
        print("Already Login... Now Searching Item...")
        await page.fill("div.nav-search-field input[type='text']", "Pencil")
        await page.click("input[type='submit']")
        await self.parse(page)
    
    async def parse(self, page):
        await page.wait_for_selector("div.s-main-slot.s-result-list div[role='listitem']")
        items = await page.query_selector_all("div.s-main-slot.s-result-list div[role='listitem']")
        print(f"Got {len(items)} items... Starting scraping...\n")

        tasks = []
        for i, item in enumerate(items, start=1):
            url_item = await self.safe_attr(item, "a.a-link-normal", "href")
            if url_item:
                full_url = urljoin("https://www.amazon.com", url_item)
                tasks.append(self.scrape_in_new_tab(full_url, i))
            else:
                print(f"⚠️ No href found for item {i}, skipping...")
        await asyncio.gather(*tasks)
        print(f"\n✅ Total product titles scraped: {len(self.scraped_urls)}")
        i = 1
        while True:
            next_page = await self.safe_attr(page, "div[role='navigation'] ul li.s-list-item-margin-right-adjustment span a.s-pagination-item.s-pagination-next", "href")
            if next_page:
                next_page_url = urljoin("https://www.amazon.com", next_page)
                print(f"➡️ Go to next page {i}: {next_page_url}")
                await page.goto(next_page_url)
                await self.parse(page)
                i += 1
            else:
                print("❌ No more next page found. Pagination ended.")
                break

            
    async def scrape_in_new_tab(self, url, index):
        async with self.semaphore:
            if url in self.scraped_urls:
                return
            self.scraped_urls.add(url)

            for attempt in range(2):
                new_page = await self.context.new_page()
                try:
                    await new_page.goto(url, wait_until="domcontentloaded", timeout=15000)
                    title = await self.safe_text(new_page, "span[id='productTitle']")
                    asin = await self.safe_text(new_page, "table#productDetails_detailBullets_sections1 tr:has(th:has-text('ASIN')) td")
                    if title:
                        print(f"✅ Scraped {index}: {title.strip()} | ASIN: {asin}")
                        self.writer.writerow([title.strip(), asin, url])
                        return
                    else:
                        print(f"⚠️ Missing data on attempt {attempt+1} for {url}")
                except Exception as e:
                    print(f"❌ Attempt {attempt+1} failed for {url}: {e}")
                finally:
                    await new_page.close()
                await asyncio.sleep(1)
            print(f"❌ Completely failed scraping {url} after 3 attempts")

    async def parse_item(self, page, index):
        await page.wait_for_timeout(1000)
        title = await self.safe_text(page, "span[id='productTitle']")
        if title:
            print(f"✅ Scraped {index}: {title}")
        else:
            print(f"❌ No title found for product {index}")
        
    
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
    url = "https://www.amazon.com/ap/signin?openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.amazon.com%2F%3F%26tag%3Dgoogleglobalp-20%26ref%3Dnav_custrec_signin%26adgrpid%3D159651196451%26hvpone%3D%26hvptwo%3D%26hvadid%3D675114638367%26hvpos%3D%26hvnetw%3Dg%26hvrand%3D17511973823310375650%26hvqmt%3De%26hvdev%3Dc%26hvdvcmdl%3D%26hvlocint%3D%26hvlocphy%3D9124631%26hvtargid%3Dkwd-10573980%26hydadcr%3D2246_13468515&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.assoc_handle=usflex&openid.mode=checkid_setup&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0"
    asyncio.run(AmazonScraper().start_url(url))
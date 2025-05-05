from playwright.async_api import async_playwright
from middlewares import Middlewares
from playwright_stealth import stealth_async
from dotenv import load_dotenv
import os
import csv
import asyncio

class AmazonReview:
    def __init__(self):
        env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'key', '.env')
        base_dir = os.path.dirname(os.path.abspath(__file__))
        output_dir = os.path.join(base_dir, ".." ,"output")
        self.filename = os.path.join(output_dir, "w1.csv")
        file_exists = os.path.isfile(self.filename)
        self.csv_file = open(self.filename, mode="a", newline="", encoding="utf-8")
        self.writer = csv.writer(self.csv_file)
        if not file_exists:
            self.writer.writerow(["Name", "Title", "Date", "Description", "Rating"])
        load_dotenv(env_path)
        self.email = os.getenv("AMAZON_EMAIL")
        self.password = os.getenv("AMAZON_PASSWORD")
        
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
        await self.parse(page)
    
    async def parse(self, page):
        await page.goto("https://www.amazon.com/product-reviews/B0CNNK7KPF/ref=cm_cr_arp_d_viewopt_sr?ie=UTF8&filterByStar=all_stars&reviewerType=all_reviews&pageNumber=1#reviews-filter-bar")
        await page.wait_for_timeout(2000)
        while True:
            reviews = await page.query_selector_all("ul.a-unordered-list.a-nostyle.a-vertical li.review.aok-relative")
            print(f"Found {len(reviews)} reviews on this page")
            for review in reviews:
                name = await self.safe_text(review, "a.a-profile div span.a-profile-name")
                title_element = await review.query_selector_all('div.a-row h5 a span')
                title = (await title_element[-1].inner_text()).strip() if title_element else None
                date = await self.safe_text(review, "span.a-size-base.a-color-secondary.review-date")
                description = await self.safe_text(review, "span.a-size-base.review-text.review-text-content")
                rating = await self.safe_text(review, "div.a-row h5 a i[data-hook='review-star-rating']")
                print(f"Name : {name}")
                self.writer.writerow([name.strip(), title.strip(), date.strip(), description.strip(), rating.strip()])
            next_button = page.locator("li.a-last a")
            if await next_button.count() > 0:
                await page.wait_for_timeout(2000)
                await next_button.first.click()
            else:
                print("***** NO MORE PAGES *****")
                break

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
    asyncio.run(AmazonReview().start_url(url))
from oauth2client.service_account import ServiceAccountCredentials
from cleaner import clean_text, extract_number, extract_rating, clean_hosted_by, clean_amenities, clean_rules, from_char_list
from playwright.async_api import async_playwright
from dotenv import load_dotenv
import threading
import gspread
import asyncio
import os

class AirbnbScraper:
    def __init__(self, search_location, max_pages=1, sheet_name="Airbnb Listings", concurrency=3, delay=5, stop_event=None, log_callback=None):
        self.search_location = search_location
        self.max_pages = max_pages
        self.sheet_name = sheet_name
        self.concurrency = concurrency
        self.delay = delay
        self.stop_event = stop_event or threading.Event()
        self.log = log_callback or (lambda x: None)
        env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'key', '.env')
        load_dotenv(env_path)
        self.email = os.getenv("AIRBNB_EMAIL")
        self.password = os.getenv("AIRBNB_PASSWORD")
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        key_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'key', 'key.json')
        creds = ServiceAccountCredentials.from_json_keyfile_name(key_path, scope)
        client = gspread.authorize(creds)
        self.sheet = client.open(self.sheet_name).sheet1
        self.sheet.clear()
        self.sheet.append_row(["Title", "Short Description","Guest Favorite" ,"Price", "Price Discount", "Hosted By", "Reviews", "Rating", "Guest", "Beds", "Bedrooms", "Baths", "Amenities" , "Amenities Not Included", "Cleanliness", "Accuracy", "Check-In", "Communication", "Location", "Value", "House Rules", "Additional Rules", "Safety & Property", "URL", "Image URL"])
        self.semaphore = asyncio.Semaphore(self.concurrency)
        
    async def start(self):
        async with async_playwright() as playwright:
            self.browser = await playwright.chromium.launch(headless=True)
            self.context = await self.browser.new_context(locale='en-US', extra_http_headers={'Accept-Language': 'en-US,en;q=0.9'})
            page = await self.context.new_page()
            await page.goto("https://www.airbnb.com/login")
            await page.click("button[aria-label='Continue with email']")
            await page.fill("input[inputmode='email']", self.email)
            await page.click("button[type='submit']")
            await page.fill("input[name='user[password]']", self.password)
            await page.click("button[type='submit']")
            await page.fill("input[placeholder='Search destinations']", self.search_location)
            await page.click("button[data-testid='structured-search-input-search-button']")
            await page.wait_for_selector("div.dmzfgqv.atm_5sauks_glywfm.dir.dir-ltr")
            await self.search(page, current_page=1)
            await self.browser.close()
            
    async def search(self, page, current_page):
        if current_page > self.max_pages or self.stop_event.is_set():
            self.log(f"Reached max pages ({self.max_pages}) or stop requested")
            return
            
        self.log(f"Processing page {current_page}")
        
        items = await page.query_selector_all("div.c965t3n.atm_9s_11p5wf0.atm_dz_1osqo2v.dir.dir-ltr")
        self.log(f"Found {len(items)} listings on page {current_page}")
        
        tasks = []
        for index, item in enumerate(items):
            if self.stop_event.is_set():
                break
                
            url = await self.safe_attr(item, "a", "href")
            img_url = await self.safe_attr(item, "div.cjv59qb.atm_mk_h2mmj6 img", "src")
            if url:
                full_url = f"https://www.airbnb.com{url}"
                tasks.append(self.process_item(full_url, img_url))
                
        await asyncio.gather(*tasks)
        
        # Pagination
        next_page_url = await self.safe_attr(page, "a[aria-label='Next']", "href")
        if next_page_url and not self.stop_event.is_set():
            full_next_page_url = f"https://www.airbnb.com{next_page_url}"
            await page.goto(full_next_page_url)
            await self.search(page, current_page + 1)

    async def process_item(self, url, img_url):
        async with self.semaphore: 
            page = await self.context.new_page()
            try:
                await self.get_data(page, url, img_url)
            except Exception as e:
                self.log(f"Error processing {url}: {str(e)}")
            finally:
                await page.close()
                
    async def get_data(self, page, url, img_url):
        if self.stop_event.is_set():
            return     
        await page.goto(url)
        if self.delay > 0:
            await asyncio.sleep(self.delay)
        await self.close_popup(page)
        await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        
        await page.click("div.b9672i7.atm_h3_8tjzot.atm_h3_1ph3nq8__oggzyc button[type='button']")
        await page.wait_for_timeout(1000)
        amenities_element = await page.query_selector_all("ul._2f5j8p li div.twad414.atm_7l_jt7fhx")
        amenities = []
        for elem in amenities_element:
            text = await elem.text_content()
            if text:
                amenities.append(text.strip())
        amenities_text = ", ".join(amenities)
        cleaned = clean_amenities(amenities_text)
        included_amenities = ", ".join(cleaned["available"])
        not_included_amenities = ", ".join(cleaned["unavailable"])
        await page.click("div[aria-label='What this place offers'] button[aria-label='Close']")
        
        await page.click("button[aria-label='More information about house rules']")
        await page.wait_for_timeout(1000)
        house_rules_element = await page.query_selector_all("div.ce5nonf.atm_gq_1yuitx div.c1r78wbb.atm_9s_1txwivl")
        house_rules_raw = []

        for elem in house_rules_element:
            text = await elem.text_content()
            if text:
                house_rules_raw.append(text.strip())

        # Join rules together
        house_rules_text = ", ".join(house_rules_raw)

        # Clean it
        cleaned = clean_rules(house_rules_text)

        # No need to use from_char_list anymore
        house_rules = cleaned["house_rules"]
        additional_rules = cleaned["additional_rules"]

        await page.click("button[aria-label='Close']")

        
        await page.click("button[aria-label='More information about safety and property']")
        await page.wait_for_timeout(1000)
        safety_element = await page.query_selector_all("div.ce5nonf.atm_gq_1yuitx div.c1r78wbb.atm_9s_1txwivl")
        safety = []
        for elem in safety_element:
            text = await elem.text_content()
            if text:
                safety.append(text.strip())
        safety_text = ", ".join(safety)
        await page.click("button[aria-label='Close']")
        
        title = clean_text(await self.safe_text(page, "div._1e9g34tc h1.hpipapi"))
        short_description = clean_text(await self.safe_text(page, "div.t1kjrihn h2.hpipapi.atm_7l_1kw7nm4"))
        price = await self.safe_text(page, "span._1qgfaxb1 span._4dhrua") or await self.safe_text(page, "span._1qgfaxb1 span.u1y3vocb.atm_7l_rb934l.atm_cs_1peztlj.dir.dir-ltr")
        price_discount = await self.safe_text(page, "span._1qgfaxb1 span._hb913q")
        hosted_by = clean_hosted_by(await self.safe_text(page, "div.t1lpv951.atm_c8_2x1prs.atm_g3_1jbyh58.atm_fr_11a07z3.atm_cs_10d11i2.dir.dir-ltr"))
        reviews = extract_number(await self.safe_text(page, "div.rgr5sph.atm_c8_km0zk7 a.l1ovpqvx.atm_1he2i46_1k8pnbi_10saat9") or await self.safe_text(page, "div[data-testid='pdp-reviews-highlight-banner-host-review'] span.a8jt5op.atm_3f_idpfg4"))
        rating = extract_rating(await self.safe_text(page, "div[data-testid='pdp-reviews-highlight-banner-host-rating'] span.a8jt5op.atm_3f_idpfg4") or await self.safe_text(page, "div.rgr5sph.atm_c8_km0zk7 div.rmtgcc3.atm_c8_o7aogt.atm_c8_l52nlx__oggzyc"))
        try:
            element = await page.query_selector("div[data-section-id='GUEST_FAVORITE_BANNER']")
            guest_favorite = "Yes" if element else "No"
        except:
            guest_favorite = "No"
        info_items = await page.query_selector_all("ol.lgx66tx.atm_gi_idpfg4.atm_l8_idpfg4.dir.dir-ltr li")
        guest = beds = bedrooms = baths = None
        for item in info_items:
            text = await item.text_content()
            if not text:
                continue
            text_lower = text.lower()
            if "guest" in text_lower:
                guest = extract_number(text)
            elif "bedroom" in text_lower:
                bedrooms = extract_number(text)
            elif "bed" in text_lower and "bedroom" not in text_lower:
                beds = extract_number(text)
            elif "bathroom" in text_lower or "bath" in text_lower:
                baths = extract_number(text)
        rating_blocks = await page.query_selector_all("div.awuxh4x div.cgod704 div.l925rvg.atm_9s_1txwivl")
        cleanliness = accuracy = check_in = communication = location = value = None
        for block in rating_blocks:
            text = await block.inner_text()
            parts = text.split("\n")
            if len(parts) >= 2:
                label = parts[0].strip().lower()
                score = parts[1].strip()
                if label == "cleanliness":
                    cleanliness = score
                elif label == "accuracy":
                    accuracy = score
                elif label == "check-in":
                    check_in = score
                elif label == "communication":
                    communication = score
                elif label == "location":
                    location = score
                elif label == "value":
                    value = score
        
        self.sheet.append_row([title or "N/A", short_description or "N/A", guest_favorite, price or "N/A", price_discount or "N/A", hosted_by or "N/A", reviews or "N/A", rating or "N/A", guest or "N/A", beds or "N/A", bedrooms or "N/A", baths or "N/A", included_amenities or "N/A", not_included_amenities or "N/A", cleanliness or "N/A", accuracy or "N/A", check_in or "N/A", communication or "N/A", location or "N/A", value or "N/A", house_rules or "N/A", additional_rules or "N/A", safety_text or "N/A", url, img_url])
        self.log(f"Scraped: {title}")
    
    async def close_popup(self, page):
        try:
            close_button = await page.wait_for_selector("div[aria-label='Translation on'] button[aria-label='Close']", timeout=1000)
            await close_button.click()
            self.log("Closed translation popup")
        except:
            pass
        
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
    url = "https://www.airbnb.com/login"
    asyncio.run(AirbnbScraper().start_url(url))
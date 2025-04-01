import asyncio
from playwright.async_api import async_playwright
import json
import csv
import os
import time

async def start_url(url):
    cookies_path = os.path.join(os.path.dirname(__file__), 'amazon_cookies.json')
    save_path = os.path.join(os.path.dirname(__file__), 'amazon_review.csv')
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=True)
        context = await browser.new_context()
        with open(cookies_path, 'r') as f:
            cookies = json.load(f)
        await context.add_cookies(cookies)

        page = await context.new_page()
        await page.goto(url)
        csvfile = open(save_path, 'w', newline='', encoding='utf-8')
        field_name = ["name", "title", "date", "review", "rating"]
        writer = csv.DictWriter(csvfile, fieldnames=field_name)
        writer.writeheader()

        while True:
            reviews = await page.query_selector_all("ul.a-unordered-list.a-nostyle.a-vertical li.review.aok-relative")
            print(f"Found {len(reviews)} reviews on this page")
            for review in reviews:
                name_element = await review.query_selector("a.a-profile div span.a-profile-name")
                title_element = await review.query_selector_all('div.a-row h5 a span')
                date_element = await review.query_selector("span.a-size-base.a-color-secondary.review-date")
                rating_element = await review.query_selector("div.a-row h5 a i[data-hook='review-star-rating']")
                description_element = await review.query_selector("span.a-size-base.review-text.review-text-content")
                
                name = (await name_element.inner_text()).strip() if name_element else None
                title = (await title_element[-1].inner_text()).strip() if title_element else None
                date = (await date_element.inner_text()).strip() if date_element else None
                rating = (await rating_element.inner_text()).strip() if rating_element else None
                description = (await description_element.inner_text()).strip() if description_element else None
                item = {"name": name, "title": title, "date": date, "review": description, "rating":rating}
                writer.writerow(item)
                
            next_button = page.locator("li.a-last a")
            if await next_button.count() > 0:
                time.sleep(2)
                await next_button.first.click()
            else:
                print("***** NO MORE PAGES *****")
                break
        await browser.close()

if __name__ == "__main__":
    url = "https://www.amazon.com/product-reviews/B0B7B8Q274/"
    asyncio.run(start_url(url))
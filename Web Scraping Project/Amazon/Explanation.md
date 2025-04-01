# Amazon Review Scraper Explanation
This Python script automates the process of scraping customer reviews from an Amazon product page using the `playwright` library. It extracts review details such as the reviewer’s name, review title, date, rating, and review text, then saves the data into a CSV file for further analysis.

## Overview
- **Purpose**: Scrape customer reviews from a specific Amazon product page.
- **Tools**:
  - `playwright.async_api`: Automates a Chromium browser to handle dynamic content.
  - `csv`: Writes the scraped data to a CSV file.
  - `json`: Loads cookies from a JSON file to simulate a logged-in session.
  - `asyncio`: Manages asynchronous operations for efficient web scraping.
  - `os and time`: Handle file paths and introduce delays to mimic human behavior.
- **Output**: A CSV file (`amazon_review.csv`) containing columns: `name`, `title`, `date`, `review`, and `rating`.
## Code Breakdown
### Full Script
```python
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
```
## How It Works
### 1. Setup and Browser Initialization
- The script defines an asynchronous function `start_url` that takes a URL as input.
-  It constructs file paths for `amazon_cookies.json` (cookies file) and `amazon_review.csv` (output file) using `os.path.join`.
-  A headless Chromium browser is launched with `playwright.chromium.launch(headless=True)`—headless mode means it runs without a visible UI.
- Cookies are loaded from `amazon_cookies.json` to simulate a logged-in session, which may help avoid CAPTCHAs or restrictions.
A new browser context and page are created, and the script navigates to the provided URL.
```python
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
```
### 2. CSV File Creation
- A CSV file (`amazon_review.csv`) is opened in write mode with UTF-8 encoding to handle special characters.
- The CSV headers are defined as `name`, `title`, `date`, `review`, and `rating`, and written to the file using `csv.DictWriter`.
```python
csvfile = open(save_path, 'w', newline='', encoding='utf-8')
field_name = ["name", "title", "date", "review", "rating"]
writer = csv.DictWriter(csvfile, fieldnames=field_name)
writer.writeheader()
```
### 3. Scraping Reviews
- The script enters a `while True` loop to scrape reviews from the current page and handle pagination.
- It uses `query_selector_all` with the CSS selector `ul.a-unordered-list.a-nostyle.a-vertical li.review.aok-relative` to find all review elements on the page.
- For each review, it extracts:
  - **Name**: From the `span.a-profile-name` element inside the profile link.
  - **Title**: From the last span inside `div.a-row h5 a`, as multiple spans might exist.
  - **Date**: From `span.review-date`.
  - **Rating**: From the star rating element with `data-hook='review-star-rating'`.
  - **Review Text**: From `span.review-text-content`.
- Each field is extracted using `inner_text()` and stripped of whitespace. If an element is missing, the value defaults to `None`.
- The data is stored in a dictionary and written to the CSV file.
```python
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
    item = {"name": name, "title": title, "date": date, "review": description, "rating": rating}
    writer.writerow(item)
```
### 4. Pagination Handling
- After scraping reviews on the current page, the script looks for a "Next" button using the locator `li.a-last a`.
- If the button exists (`count() > 0`), it waits 2 seconds with `time.sleep(2)` to mimic human behavior and avoid detection, then clicks the button to load the next page.
- If no "Next" button is found, it prints a message and breaks the loop.
```python
next_button = page.locator("li.a-last a")
if await next_button.count() > 0:
    time.sleep(2)
    await next_button.first.click()
else:
    print("***** NO MORE PAGES *****")
    break
```
### 5. Cleanup
After all pages are scraped, the browser is closed with await `browser.close()` to free up resources.
## Key Features
- **Dynamic Web Scraping**: Uses `playwright` to handle dynamically loaded content and simulate user interactions like clicking the "Next" button.
- **Structured Output**: Saves review data in a CSV format for easy analysis in tools like Excel or pandas.
- **Session Management**: Loads cookies to simulate a logged-in session, potentially bypassing some anti-scraping measures.
- **Asynchronous Execution**: Leverages `asyncio` for efficient handling of browser operations and I/O tasks.

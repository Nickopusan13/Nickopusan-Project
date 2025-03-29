# CME Group Trading Hours Scraper
This Python script automates the process of scraping trading hours data from the CME Group Trading Hours page using the playwright library. It extracts product names and their associated trading hours, then saves the data into a timestamped CSV file for easy analysis or record-keeping.

## Overview
- **Purpose**: Scrape trading hours data for various financial products listed on the CME Group website.
- **Tools**:
  - `playwright.async_api`: Automates a Chromium browser to interact with dynamic web content.
  - `csv`: Writes the scraped data to a CSV file.
  - `datetime`: Generates timestamps for unique CSV filenames.
  - `asyncio`: Manages asynchronous operations for efficient web scraping.
- **Output**: A CSV file (e.g., trading_hours_20231024_153022.csv) containing columns: Product Name, Trade Group, and Trade Group Text.
## How It Works
### 1. Setup and Browser Initialization
- The script launches a Chromium browser in non-headless mode (visible for debugging) using `playwright`.
- It navigates to the target URL: `https://www.cmegroup.com/trading-hours.html`.
```python
async with async_playwright() as playwright:
    browser = await playwright.chromium.launch(headless=False)
    page = await browser.new_page()
    await page.goto(url)
```
### 2. CSV File Creation
- A timestamp is generated using `datetime` to ensure each CSV file has a unique name (e.g., `trading_hours_20231024_153022.csv`).
- The CSV file is opened with headers: `Product Name`, `Trade Group`, and `Trade Group Text`.
```python
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
csv_filename = f"trading_hours_{timestamp}.csv"
with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Product Name', 'Trade Group', 'Trade Group Text'])
```
### 3. Interacting with Filters
- The script clicks a dropdown menu on the webpage to reveal filter options (e.g., categories of trading products).
- It iterates through each filter, clicking one at a time to load the corresponding trading hours data.
```python
await page.click("div.reverse.holidays.filter-section div.universal-dropdown.filter-menu")
filters = await page.query_selector_all("div.dropdown-menu.show div.simplebar-mask a.dropdown-item.dropdown-item")
for i in range(len(filters)):
    filters = await page.query_selector_all("div.dropdown-menu.show div.simplebar-mask a.dropdown-item.dropdown-item")
    await filters[i].click()
    await get_data(page, writer)
    await page.click("div.reverse.holidays.filter-section div.universal-dropdown.filter-menu")
```
### 4. Data Extraction
- The `get_data` function extracts data from a table displayed after each filter is applied.
- For each row in the table:
  - **Product Name**: Extracted from the `product-code` column.
  - **Trade Groups**: Extracted from multiple `events-data` columns, which contain trading hours details.
  - Each trade group’s text is written to the CSV file alongside the product name and a trade group identifier (e.g., "Trade Group 1").
```python
async def get_data(page, writer):
    rows = await page.query_selector_all("div.table-section table.trading-hours-table.holiday tbody tr")
    for row in rows:
        product_element = await row.query_selector("td.product-code a span")
        tables = await row.query_selector_all('xpath=//td[@class="events-data"]')
        for table_index, table in enumerate(tables):
            product_name = await product_element.inner_text()
            trade_groups = await table.query_selector_all('.trade-group')
            for i, trade_group in enumerate(trade_groups):
                text = await trade_group.text_content()
                writer.writerow([product_name, f"Trade Group {i + 1}", text.strip()])
```
### 5. Asynchronous Execution
- The script uses asyncio to handle asynchronous browser operations, such as waiting for page elements to load or actions to complete.
- The main function start_url is executed with asyncio.run().
```python
if __name__ == "__main__":
    url = "https://www.cmegroup.com/trading-hours.html"
    asyncio.run(start_url(url))
```
## Key Features
- Dynamic Web Scraping: Handles dynamically loaded content by automating browser interactions.
- Structured Output: Saves data in a CSV format, making it easy to analyze or share.
- Console Feedback: Prints the number of filters, rows, and extracted data for monitoring progress.

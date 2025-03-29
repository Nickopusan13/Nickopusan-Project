import asyncio
from playwright.async_api import async_playwright
import csv
from datetime import datetime

async def start_url(url):
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=False)
        page = await browser.new_page()
        await page.goto(url)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        csv_filename = f"trading_hours_{timestamp}.csv"
        
        with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Product Name', 'Trade Group', 'Trade Group Text'])  # Header
            await page.click("div.reverse.holidays.filter-section div.universal-dropdown.filter-menu")
            filters = await page.query_selector_all("div.dropdown-menu.show div.simplebar-mask a.dropdown-item.dropdown-item")
            print(f"Total filters: {len(filters)}")
            
            for i in range(len(filters)):
                filters = await page.query_selector_all("div.dropdown-menu.show div.simplebar-mask a.dropdown-item.dropdown-item")
                if i < len(filters):
                    await filters[i].click()
                    print(f"Filter {i+1} clicked")
                    await get_data(page, writer)
                    await page.click("div.reverse.holidays.filter-section div.universal-dropdown.filter-menu")
                    await page.wait_for_selector("div.dropdown-menu.show")

async def get_data(page, writer):
    rows = await page.query_selector_all("div.table-section table.trading-hours-table.holiday tbody tr")
    print(len(rows))
    for row in rows:
        product_element = await row.query_selector("td.product-code a span")
        tables = await row.query_selector_all('xpath=//td[@class="events-data"]')
        for table_index, table in enumerate(tables):
            print(f"\n🔹 Table {table_index + 1} 🔹")  
            product_name = await product_element.inner_text()
            trade_groups = await table.query_selector_all('.trade-group')
            for i, trade_group in enumerate(trade_groups):
                text = await trade_group.text_content()
                writer.writerow([product_name, f"Trade Group {i + 1}", text.strip()])
                print(f"Product Name: {product_name}")
                print(f"Trade Group {i + 1}: {text.strip()}")

if __name__ == "__main__":
    url = "https://www.cmegroup.com/trading-hours.html"
    asyncio.run(start_url(url))
# Centris Web Scraper
This Scrapy project is designed to scrape property listings from the [`Centris`](https://www.centris.ca/) real estate platform website. It leverages Scrapy for web scraping and Playwright for browser automation to handle dynamic content, user authentication, and page navigation. The scraped data is cleaned, structured, and saved as JSON files, with associated images downloaded to organized directories.

## Key Features
- **Configuration**:
The project uses a [`config.json`](config.json) file to store sensitive information such as the username, password, and root download folder for scraped data. It also tracks already scraped listing IDs to prevent duplicate scraping.
- **Login Handling**:
The spider logs into the Centris website using credentials provided in [`config.json`](config.json), enabling access to user-specific saved searches.
- **Saved Searches**:
It navigates to the "My Searches" page on Centris and extracts URLs of saved searches, which are then used to scrape property listings.
- **Property Scraping**:
For each saved search, the spider scrapes property listings, extracting details including:
  - **URL**
  - **Listing ID**
  - **Image URLs**
  - **Price**
  - **Address**
  - **Number of bedrooms and bathrooms**
  - **Property type**
  - **Land area**
  - **Potential gross revenue**
- **Data Cleaning and Storage**:
Scraped data is cleaned (e.g., removing extra whitespace and non-breaking spaces) and structured into a dictionary. Each listing is saved as a JSON file in a directory named after its ID, with associated images downloaded to the same location.
- **Pagination**:
The spider uses Playwright to interact with the "next" button, scraping all available pages of listings.
- **User Agent Rotation**:
Fake user agents are rotated using the ScrapeOps API to make requests appear as though they come from different browsers, reducing the likelihood of being blocked.
- **Proxy Support**:
The project includes optional support for rotating proxies (currently commented out), which can be enabled for additional anonymity.
Project Structure
- [`config.json`](config.json):
Stores configuration details such as:
  - `user_name`: Centris login email
  - `user_password`: Centris login password
  - `already_scrape_id`: List of previously scraped listing IDs
  - `root_download_folder`: Directory path for saving scraped data
- [`pipelines.py`](pipelines.py):
Defines the `CentrisPipeline` class, which:
Cleans scraped data
Structures it into a dictionary
Saves it as JSON files
Downloads and stores images
centris/settings.py:
Configures Scrapy settings, including:
Playwright launch options (e.g., headless mode)
Middleware for user agent rotation
Pipeline integration
Proxy settings (commented out)
centris/items.py:
Defines the CentrisItem class, specifying fields for scraped data (e.g., url, id, price, etc.).
centris/middlewares.py:
Contains custom middleware:
ScrapeOpsFakeUserAgentMiddleware: Rotates user agents via the ScrapeOps API
MyProxyMiddleware: Manages rotating proxies (currently disabled)
centris/spiders/centris_spider.py:
The main spider class (CentrisSpiderSpider) that:
Logs into Centris
Navigates to saved searches
Scrapes property listings
Handles pagination
How to Use
Follow these steps to set up and run the project:

Configuration:
Update the config.json file with your Centris credentials and desired output directory. Example:
json

Collapse

Wrap

Copy
{
    "user_name": "your_email@example.com",
    "user_password": "your_password",
    "already_scrape_id": [],
    "root_download_folder": "C:/path/to/output"
}
Install Dependencies:
Install the required libraries using pip and set up Playwright:
bash

Collapse

Wrap

Copy
pip install scrapy playwright
playwright install
Run the Spider:
Execute the spider from the project directory with:
bash

Collapse

Wrap

Copy
scrapy crawl centris_spider
Notes
Ensure you have a valid Centris account, as the spider requires login credentials to access saved searches.
The project is configured to run in headless mode by default. To debug visually, set "headless": False in PLAYWRIGHT_LAUNCH_OPTIONS in settings.py.
Proxy support can be enabled by uncommenting the proxy middleware in settings.py and providing a list of proxies in ROTATING_PROXY_LIST.
Example Output
For each scraped listing, the project creates a directory named after the listing ID (e.g., 12345678) containing:

12345678.json: A JSON file with structured property details
Image files (e.g., abc123.jpg): Downloaded images associated with the listing
This project demonstrates a robust approach to web scraping with Scrapy and Playwright, effectively handling authentication, dynamic content, and data storage for real estate data extraction.

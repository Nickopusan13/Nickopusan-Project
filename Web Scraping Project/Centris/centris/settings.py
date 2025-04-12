import os
import json

CONFIG_PATH = os.path.join(os.path.dirname(__file__), '..', 'config.json')
try:
    with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
        config = json.load(f)
except FileNotFoundError:
    config = {}
    print("⚠️ config.json not found. Using default values.")

# Default value fallback
ROOT_DOWNLOAD_FOLDER = config.get("root_download_folder", "centris_output")

BOT_NAME = "centris"

SPIDER_MODULES = ["centris.spiders"]
NEWSPIDER_MODULE = "centris.spiders"
LOG_LEVEL = 'INFO'

PLAYWRIGHT_LAUNCH_OPTIONS = {
    "headless": True,  # Set to false if you want to see the browser in action
    "timeout": 30000,
    "args": [
        "--no-sandbox",
        "--disable-setuid-sandbox",
        "--disable-blink-features=AutomationControlled",
        "--disable-dev-shm-usage",
        "--disable-infobars",
        "--disable-web-security",
        "--disable-extensions",
        "--disable-gpu",
        "--start-maximized",
        "--hide-scrollbars",
        "--mute-audio",
    ],
}


# Obey robots.txt rules
ROBOTSTXT_OBEY = False
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"

# Fake User Agent
SCRAPEOPS_API_KEY = 'c6b36cca-74ea-4c45-9397-af10c76a7d27'
SCRAPEOPS_ENDPOINT = 'https://headers.scrapeops.io/v1/user-agents'
SCRAPEOPS_FAKE_USER_AGENT_ENABLED = True
SCRAPEOPS_NUM_RESULTS = 50

# Rotating Proxies
HTTPPROXY_ENABLED = True
ROTATING_PROXY_LIST = [
   # "http://15.204.76.66:3128", # Example proxy, replace with your own
]
RETRY_ENABLED = True
RETRY_TIMES = 2 

DOWNLOADER_MIDDLEWARES = {
   "centris.middlewares.ScrapeOpsFakeUserAgentMiddleware": 400,
   # "centris.middlewares.MyProxyMiddleware": 543, # Uncomment if you already have a proxy list
   "scrapy.downloadermiddlewares.cookies.CookiesMiddleware": 700,
}

# Playwright
import asyncio

asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
CONCURRENT_REQUESTS = 50
CONCURRENT_REQUESTS_PER_DOMAIN = 5
DOWNLOAD_DELAY = 0
PLAYWRIGHT_BROWSER_TYPE = "chromium"

DOWNLOAD_HANDLERS = {
   "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
   "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
}

ITEM_PIPELINES = {
   "centris.pipelines.CentrisPipeline": 300,
}
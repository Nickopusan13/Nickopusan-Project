# Scrapy settings for home project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = "home"

SPIDER_MODULES = ["home.spiders"]
NEWSPIDER_MODULE = "home.spiders"

# Fake User Agent
SCRAPEOPS_API_KEY = 'c6b36cca-74ea-4c45-9397-af10c76a7d27'
SCRAPEOPS_ENDPOINT = 'https://headers.scrapeops.io/v1/user-agents'
SCRAPEOPS_FAKE_USER_AGENT_ENABLED = True
SCRAPEOPS_NUM_RESULTS = 50

# Rotating Proxies
# ROTATING_PROXY_LIST_PATH = r"C:\Users\mochw\Downloads\Webshare 10 proxies.txt"
# PROXY_USER = "xmvrguyj"
# PROXY_PASSWORD = "o29a603lgm1e"

# RETRY_ENABLED = True
# RETRY_TIMES = 2 
LOG_LEVEL = 'INFO'

# Playwright
import random

CONCURRENT_REQUESTS = 100
CONCURRENT_REQUESTS_PER_DOMAIN = 50
DOWNLOAD_DELAY = 0

DOWNLOAD_HANDLERS = {
   "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
   "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
}

PLAYWRIGHT_LAUNCH_OPTIONS = {
    "headless": True,
    "timeout": 30000,
    "args": ["--no-sandbox", "--disable-setuid-sandbox", "--disable-blink-features=AutomationControlled"],
}

PLAYWRIGHT_DEFAULT_NAVIGATION_TIMEOUT = 60000
DOWNLOAD_DELAY = random.uniform(1, 5)
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 1
AUTOTHROTTLE_MAX_DELAY = 15
AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"

def should_abort_request(request):
   blocked_resources = ["image", "stylesheet", "font"]
   return request.resource_type in blocked_resources

PLAYWRIGHT_ABORT_REQUEST = should_abort_request

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Enable or disable downloader middlewares
DOWNLOADER_MIDDLEWARES = {
   "home.middlewares.ScrapeOpsFakeUserAgentMiddleware": 400,
   # "scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware": 340,
   # "home.middlewares.MyProxyMiddleware": 350,
}

# Configure item pipelines
ITEM_PIPELINES = {
   "home.pipelines.CryptoPipeline": 300
   # "home.pipelines.AirbnbPipeline": 300
   # "home.pipelines.BookPipeline": 300,
   # "home.pipelines.ImdbPipeline": 300,
}

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = "home (+http://www.yourdomain.com)"

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
#    "Accept-Language": "en",
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    "home.middlewares.HomeSpiderMiddleware": 543,
#}


# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    "scrapy.extensions.telnet.TelnetConsole": None,
#}


# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = "httpcache"
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"

# Set settings whose default value is deprecated to a future-proof value
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"



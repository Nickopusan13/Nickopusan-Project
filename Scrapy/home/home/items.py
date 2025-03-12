# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
import scrapy.item

class BookItem(scrapy.Item):
    upc = scrapy.Field()
    product_type = scrapy.Field()
    price_excl_tax = scrapy.Field()
    price_incl_tax = scrapy.Field()
    tax = scrapy.Field()
    availability = scrapy.Field()
    number_of_reviews = scrapy.Field()
    title = scrapy.Field()
    description = scrapy.Field()
    genre = scrapy.Field()
    rating = scrapy.Field()

class QuoteItem(scrapy.Item):
    quote = scrapy.Field()
    author = scrapy.Field()

class ImdbItem(scrapy.Item):
    title = scrapy.Field()
    rating = scrapy.Field()
    year = scrapy.Field()
    description = scrapy.Field()
    director = scrapy.Field()
    writers = scrapy.Field()
    stars = scrapy.Field()

class AirbnbItem(scrapy.Item):
    url = scrapy.Field()
    name = scrapy.Field()
    title = scrapy.Field()
    price = scrapy.Field()
    price_discount = scrapy.Field()
    hosted_by = scrapy.Field()
    guest = scrapy.Field()
    beds = scrapy.Field()
    bedrooms = scrapy.Field()
    baths = scrapy.Field()
    reviews = scrapy.Field()
    stars = scrapy.Field()

class CryptoItem(scrapy.Item):
    rank = scrapy.Field()
    initial = scrapy.Field()
    name = scrapy.Field()
    price = scrapy.Field()
    change_percentage = scrapy.Field()
    market_cap = scrapy.Field()
    volume = scrapy.Field()
    circ_supply = scrapy.Field()
    
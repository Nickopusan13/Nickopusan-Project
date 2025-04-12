import scrapy

class CentrisItem(scrapy.Item):
    url = scrapy.Field()
    id = scrapy.Field()
    image_urls = scrapy.Field()
    image = scrapy.Field()
    price = scrapy.Field()
    banner = scrapy.Field()
    address = scrapy.Field()
    bedroom = scrapy.Field()
    bathroom = scrapy.Field()
    title = scrapy.Field()
    land_area = scrapy.Field()
    pot_gross_rev = scrapy.Field()
    property_type = scrapy.Field()
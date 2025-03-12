# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ZeroinfyItem(scrapy.Item):
    url = scrapy.Field()
    img = scrapy.Field()
    price = scrapy.Field()
    discounted_price = scrapy.Field()
    course_name = scrapy.Field()
    brand = scrapy.Field()
    reviews = scrapy.Field()
    ratings = scrapy.Field()
    recording = scrapy.Field()
    delivery_mode = scrapy.Field()
    offer_type = scrapy.Field()
    kit_contents = scrapy.Field()
    video_language = scrapy.Field()
    study_materials = scrapy.Field()
    amendments = scrapy.Field()
    validity = scrapy.Field()
    mode = scrapy.Field()
    runs_on = scrapy.Field()
    doubt_solving = scrapy.Field()
    total_views = scrapy.Field()
    duration = scrapy.Field()
    highlights = scrapy.Field()
    please_note = scrapy.Field()
    requirements = scrapy.Field()
    technical_support = scrapy.Field()
    demo_tour = scrapy.Field()
    demo = scrapy.Field()
    other_details = scrapy.Field()
    configuration = scrapy.Field()
    about_faculty = scrapy.Field()
    
    

import scrapy
from scrapy_playwright.page import PageMethod
from project.items import ZeroinfyItem

class ZeroinfySpider(scrapy.Spider):
    name = "zeroinfy"
    
    def start_requests(self):
        url = "https://zeroinfy.in/collections/all?t=1741504351433"
        yield scrapy.Request(url,callback=self.parse)

    def parse(self, response):
        zeroinfy = response.css("div.product-list-2 div.product-card-2")
        for i in zeroinfy:
            relative_url = i.css("a::attr(href)").get()
            if relative_url:
                full_url = "https://zeroinfy.in" + relative_url
                yield scrapy.Request(full_url,callback=self.parse_zeroinfy_item)

        next_page = response.css("span.next a::attr(href)").get()
        if next_page:
            next_page_url = "https://zeroinfy.in" + next_page
            yield scrapy.Request(next_page_url, callback=self.parse)

    def parse_zeroinfy_item(self, response):
        zeroinfy_item = ZeroinfyItem()
        zeroinfy_item['url'] = response.url
        zeroinfy_item['img'] = response.css("img.product-img-main::attr(src)").get()
        zeroinfy_item['price'] = response.css("div.price-block li span.product-single__price::text").get()
        zeroinfy_item['discounted_price'] = response.css('div.price-block li s.product-single__price::text').get()
        zeroinfy_item['course_name'] = response.css('div.tdesktop h1::text').get()
        zeroinfy_item['brand'] = response.css('div.tdesktop a::text').get()
        zeroinfy_item['reviews'] = response.css('div.jdgm-prev-badge::attr(data-number-of-reviews)').get()
        zeroinfy_item['ratings'] = response.css('div.jdgm-prev-badge::attr(data-average-rating)').get()
        zeroinfy_item['delivery_mode'] = response.css('select[id^="SingleOptionSelector-0"] option::text').getall()
        zeroinfy_item['offer_type'] = response.css('select[id^="SingleOptionSelector-2"] option::text').getall()
        zeroinfy_item['kit_contents'] = response.xpath('//td[contains(., "Kit Contents")]/following-sibling::td//li//text()').getall()
        zeroinfy_item['duration'] = response.xpath('//td[contains(., "Duration")]/following-sibling::td//li//text()').getall()
        zeroinfy_item['recording'] = response.xpath('//td[contains(., "Recording")]/following-sibling::td//li//text()').getall()
        zeroinfy_item['validity'] = response.xpath('//td[contains(., "Validity")]/following-sibling::td//li//text()').getall()
        zeroinfy_item['total_views'] = response.xpath('//td[contains(., "Total Views")]/following-sibling::td//li//text()').getall()
        zeroinfy_item['mode'] = response.xpath('//td[contains(., "Mode")]/following-sibling::td//li//text()').getall()
        zeroinfy_item['doubt_solving'] = response.xpath('//td[contains(., "Doubt Solving")]/following-sibling::td//li//text()').getall()
        zeroinfy_item['video_language'] = response.xpath('//td[contains(., "Video Language")]/following-sibling::td//li//text()').getall()
        zeroinfy_item['study_materials'] = response.xpath('//td[contains(., "Study")]/following-sibling::td//li//text()').getall()
        zeroinfy_item['technical_support'] = response.xpath('//td[contains(., "Technical")]/following-sibling::td//li//text()').getall()
        zeroinfy_item['amendments'] = response.xpath('//td[contains(., "Amendments")]/following-sibling::td//li//text()').getall()
        zeroinfy_item['demo_tour'] = response.xpath('//td[contains(., "Demo")]/following-sibling::td//li//@href').getall()
        zeroinfy_item['other_details'] = response.xpath('//td[contains(., "Other Details")]/following-sibling::td//li//text()').getall()
        zeroinfy_item['highlights'] = response.xpath('//td[contains(., "Highlights")]/following-sibling::td//li//text()').getall()
        zeroinfy_item['requirements'] = response.xpath('//td[contains(., "Requirements")]/following-sibling::td//li//text()').getall()
        zeroinfy_item['please_note'] = response.xpath('//td[contains(., "Please Note")]/following-sibling::td//li//text()').getall()
        zeroinfy_item['runs_on'] = response.xpath('//td[contains(., "Runs On")]/following-sibling::td//li//text()').getall()
        zeroinfy_item['demo'] = response.xpath('//a[contains(text(), "See Here")]/@href').getall()
        zeroinfy_item['configuration'] = response.xpath('//td[contains(., "Configuration")]/following-sibling::td//li//text()').getall()
        zeroinfy_item['about_faculty'] = response.xpath("//div[contains(@class, 'easytabs-content-holder')]//p[contains(text(), 'CA')]/text()").get()
        yield zeroinfy_item
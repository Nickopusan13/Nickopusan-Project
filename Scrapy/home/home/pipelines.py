# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import re

class BookPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        # Strip whitespace
        field_names = adapter.field_names()
        for field_name in field_names:
            if field_name != 'description':
                value = adapter.get(field_name)
                adapter[field_name] = value.strip()
        
        # To lowercase
        lower_case_keys = ['genre']
        for lower_case in lower_case_keys:
            value = adapter.get(lower_case)
            adapter[lower_case] = value.lower()
        
        # Availability
        availability = adapter.get('availability')
        split_availability = availability.split('(')
        if len(split_availability) < 2:
            adapter['availability'] = 0
        else:
            availability_array = split_availability[1].split(' ')
            adapter['availability'] = int(availability_array[0])
        
        # Convert price to float
        price_keys = ['price_excl_tax', 'price_incl_tax', 'tax']
        for price_key in price_keys:
            value = adapter.get(price_key)
            value = value.replace('£', '')
            adapter[price_key] = float(value)
         
        # Convert number of reviews to int
        num_review_keys = ['number_of_reviews']
        for num_review in num_review_keys:
            value = adapter.get(num_review)
            adapter[num_review] = int(value)
        
        stars_rating = adapter.get('rating')
        stars_rating_low = stars_rating.lower()
        if stars_rating_low == 'zero':
            adapter['rating'] = 0
        elif stars_rating_low == 'one':
            adapter['rating'] = 1
        elif stars_rating_low == 'two':
            adapter['rating'] = 2
        elif stars_rating_low == 'three':
            adapter['rating'] = 3
        elif stars_rating_low == 'four':
            adapter['rating'] = 4
        elif stars_rating_low == 'five':
            adapter['rating'] = 5
        return item

class ImdbPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if 'title' in item:
            item['title'] = re.sub(r'^\d+\.\s', '', item['title'])

        field_names = adapter.field_names()
        for field_name in field_names:
            value = adapter.get(field_name)
            if isinstance(value, str) and field_name != 'description':
                adapter[field_name] = value.strip()
            
            if isinstance(value, str) and field_name != 'description':
                adapter[field_name] = [v.strip() for  v in value if isinstance(value, str)]
        return item

class AirbnbPipeline():
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        
        field_names = adapter.field_names()
        for field_name in field_names:
            value = adapter.get(field_name)
            if isinstance(value, str):
                adapter[field_name] = value.strip()
        
        price_keys = ['price', 'price_discount']
        for i in price_keys:
            value = adapter.get(i)
            if value:
                value = value.replace('Rp', '').replace(',', '').strip()
                try:
                    adapter[i] = float(value)
                except ValueError:
                    adapter[i] = None
        
        hosted_keys = ['hosted_by']
        for i in hosted_keys:
            value = adapter.get(i)
            value = value.replace('Hosted by', '')
            adapter[i] = value.strip()
        
        guest_keys = ['guest']
        for i in guest_keys:
            value = adapter.get(i)
            value = value.replace('guests', '').replace('guest', '')
            adapter[i] = value.strip()
        
        beds_keys = ['beds']
        for i in beds_keys:
            value = adapter.get(i)
            value = value.replace('beds', '').replace('bed', '')
            adapter[i] = value.strip()            
            
        bedrooms_keys = ['bedrooms']
        for i in bedrooms_keys:
            value = adapter.get(i)
            value = value.replace('bedrooms', '').replace('bedroom', '')
            adapter[i] = value.strip()            
            
        baths_keys = ['baths']
        for i in baths_keys:
            value = adapter.get(i)
            value = value.replace('baths', '').replace('bath', '')
            adapter[i] = value.strip()            
            
        reviews_keys = ['reviews']
        for i in reviews_keys:
            value = adapter.get(i)
            value = value.replace('reviews', '').replace('review', '')
            adapter[i] = value.strip()            
        
        return item

class CryptoPipeline():
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        field_names = adapter.field_names()
        for field_name in field_names:
            value = adapter.get(field_name)
            if isinstance(value, str):
                adapter[field_name] = value.strip()
        
        price_keys = ['price']
        for i in price_keys:
            value = adapter.get(i)
            value = value.replace(',', '')   
            adapter[i] = float(value)
        
        market_cap_keys = ['market_cap']
        for i in market_cap_keys:
            value = adapter.get(i)
            if value:
                value = value.replace(',', '')
                if 'T' in value:
                    value = float(value.replace('T', '')) * 1000000000000
                elif 'B' in value:
                    value = float(value.replace('B', '')) * 1000000000
                elif 'M' in value:
                    value = float(value.replace('M', '')) * 1000000
                elif 'K' in value:
                    value = float(value.replace('K', '')) * 1000
                adapter[i] = value
        
        volume_keys = ['volume']
        for i in volume_keys:
            value = adapter.get(i)
            if value:
                value = value.replace(',', '')
                if 'T' in value:
                    value = float(value.replace('T', '')) * 1000000000000
                elif 'B' in value:
                    value = float(value.replace('B', '')) * 1000000000
                elif 'M' in value:
                    value = float(value.replace('M', '')) * 1000000
                elif 'K' in value:
                    value = float(value.replace('K', '')) * 1000
                adapter[i] = value
        
        circ_supply_keys = ['circ_supply']
        for i in circ_supply_keys:
            value = adapter.get(i)
            if value:
                value = value.replace(',', '')
                if 'T' in value:
                    value = float(value.replace('T', '')) * 1000000000000
                elif 'B' in value:
                    value = float(value.replace('B', '')) * 1000000000
                elif 'M' in value:
                    value = float(value.replace('M', '')) * 1000000
                elif 'K' in value:
                    value = float(value.replace('K', '')) * 1000
                adapter[i] = value
                
        return item
        
        
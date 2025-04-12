import os
import json
import re
import requests
import mimetypes
from hashlib import md5
from itemadapter import ItemAdapter
from scrapy.utils.project import get_project_settings


class CentrisPipeline:
    def __init__(self):
        settings = get_project_settings()
        self.output_dir = settings.get('ROOT_DOWNLOAD_FOLDER', 'centris_output')
        os.makedirs(self.output_dir, exist_ok=True)

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        # Clean all fields
        for field_name in adapter.field_names():
            if field_name in ['image_urls', 'images']:
                continue

            value = adapter.get(field_name)

            if isinstance(value, str):
                cleaned_value = re.sub(r'\s+', ' ', value).strip().replace('\xa0', '').replace('\t', '')
                adapter[field_name] = cleaned_value if cleaned_value else None

            elif isinstance(value, list):
                cleaned_list = [
                    re.sub(r'\s+', ' ', v).strip().replace('\xa0', '').replace('\t', '')
                    for v in value if v.strip()
                ]
                adapter[field_name] = cleaned_list if cleaned_list else None

            if adapter.get(field_name) in ['', [], None]:
                adapter[field_name] = None

        # Structured data output
        data = {
            "Id": adapter.get("id"),
            "Url": adapter.get("url"),
            "Title": adapter.get("title"),
            "Address": adapter.get("address"),
            "Price": adapter.get("price"),
            "Image URLs": adapter.get("image_urls"),
            "Banner": adapter.get("banner"),
            "Bedroom": adapter.get("bedroom"),
            "Bathroom": adapter.get("bathroom"),
            "Property Type": adapter.get("property_type"),
            "Land Area": adapter.get("land_area"),
            "Pot Gross Rev": adapter.get("pot_gross_rev"),
        }

        # Create folder for the listing
        listing_id = adapter.get("id") or "unknown"
        item_dir = os.path.join(self.output_dir, listing_id)
        os.makedirs(item_dir, exist_ok=True)

        # Save JSON
        json_path = os.path.join(item_dir, f"{listing_id}.json")
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        # Download images
        image_urls = adapter.get("image_urls") or []
        for idx, image_url in enumerate(image_urls):
            try:
                response = requests.get(image_url, timeout=10)
                if response.status_code == 200:
                    # Get content type from header
                    content_type = response.headers.get('Content-Type', '').split(';')[0]
                    ext = mimetypes.guess_extension(content_type)
                    if not ext:
                        ext = '.jpg'  # Default fallback

                    # Generate unique filename
                    image_hash = md5(image_url.encode()).hexdigest()
                    image_filename = f"{image_hash}{ext}"
                    image_path = os.path.join(item_dir, image_filename)

                    with open(image_path, 'wb') as img_file:
                        img_file.write(response.content)
            except Exception as e:
                print(f"❌ Exception downloading {image_url}: {e}")

        return item
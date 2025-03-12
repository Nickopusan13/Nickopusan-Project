# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import re
from itemadapter import ItemAdapter

class ZeroinfyPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        for field_name in adapter.field_names():
            value = adapter.get(field_name)

            if isinstance(value, str):
                # Hapus karakter whitespace berlebih termasuk tab, newline, dan non-breaking space
                cleaned_value = re.sub(r'\s+', ' ', value).strip()
                cleaned_value = cleaned_value.replace('\xa0', '').replace('\t', '')  # Hapus \xa0 (non-breaking space) & \t (tab)
                adapter[field_name] = cleaned_value if cleaned_value else None

            elif isinstance(value, list):
                cleaned_list = [
                    re.sub(r'\s+', ' ', v).strip().replace('\xa0', '').replace('\t', '')
                    for v in value if v.strip()
                ]
                adapter[field_name] = cleaned_list if cleaned_list else None

            if adapter[field_name] in ['', [], None]:
                adapter[field_name] = None

        return item





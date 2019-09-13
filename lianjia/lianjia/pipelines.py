# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exporters import JsonLinesItemExporter
from lianjia.items import EsfItem,ZfItem

class LianjiaPipeline(object):
    def __init__(self):
        self.esfhouse_fp = open("esfhouse.json","wb")
        self.esfhouse_exporter = JsonLinesItemExporter(self.esfhouse_fp,ensure_ascii=False)
        self.zfhouse_fp = open("zfhouse.json", "wb")
        self.zfhouse_exporter = JsonLinesItemExporter(self.zfhouse_fp, ensure_ascii=False)

    def process_item(self, item, spider):
        if isinstance(item,EsfItem):
            self.esfhouse_exporter.export_item(item)
            return item
        else:
            self.zfhouse_exporter.export_item(item)
            return item

    def close_spider(self,spider):
        self.esfhouse_fp.close()
        self.zfhouse_fp.close()



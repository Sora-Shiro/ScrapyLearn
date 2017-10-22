# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from items import *


class AskScoreToUniversityItemPipeline(object):
    def __init__(self):
        pass

    def process_item(self, item, spider):
        if item is AskScoreToUniversityItem:
            item_info = dict(item)
            print item_info
        return item


class ScrapyTiebaPipeline(object):
    def process_item(self, item, spider):
        if item is TiebaPostItem:
            pass
        return item

# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapyTiebaItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class AskScoreToUniversityItem(scrapy.Item):
    title = scrapy.Field()
    href = scrapy.Field()
    province = scrapy.Field()
    university = scrapy.Field()
    author = scrapy.Field()
    date = scrapy.Field()


class TiebaPostItem(scrapy.Item):
    # 用户ID
    name_user = scrapy.Field()
    # 贴吧名
    name_tieba = scrapy.Field()
    # 帖子主题名
    title = scrapy.Field()
    # 帖子主题链接
    url = scrapy.Field()
    # 回复内容
    content = scrapy.Field()
    # 回复所在楼层数
    level = scrapy.Field()
    # 回复所在楼中楼层数，在回复内容所在位置非楼中楼时数值为-1
    level_in_level = scrapy.Field()
    # 回复时间
    time = scrapy.Field()

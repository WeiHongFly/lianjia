# -*- coding: utf-8 -*-
import scrapy


class LianjiaItem(scrapy.Item):
    # 链家各个城市二手房在售数量和成交数量
    province = scrapy.Field()
    city = scrapy.Field()
    city_ershoufang_zaishou = scrapy.Field()
    city_ershoufang_zaishou_href = scrapy.Field()
    city_ershoufang_chengjiao = scrapy.Field()
    city_ershoufang_chengjiao_href = scrapy.Field()
    city_ershoufang_xiaoqu_href = scrapy.Field()
    city_ershoufang_xiaoqu = scrapy.Field()
    crawl_time = scrapy.Field()

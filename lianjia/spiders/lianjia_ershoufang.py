# -*- coding:utf-8 -*-  
""" 
@file: lianjia_ershoufang.py 
@time: 2019/08/22
"""
import scrapy
from lianjia.items import LianjiaItem
from datetime import datetime


class LianJiaErShouFang(scrapy.Spider):
    name = "lianjia_ershoufang"

    def start_requests(self):
        urls = ["https://www.lianjia.com/city/"]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for p in response.xpath('//li[@class="city_list_li city_list_li_selected"]/div[@class="city_list"]/div[@class="city_province"]'):
            province = p.xpath('div/text()').get()
            for c in p.xpath('ul/li/a'):
                item = LianjiaItem()
                city = c.xpath('text()').get()
                href = c.xpath('@href').get()
                item["province"] = province
                item["city"] = city
                item["crawl_time"] = datetime.now()

                if "fang" in href:
                    self.logger.warning("City %s does not have ershoufang page" % city)
                else:
                    href_zaishou = href + "ershoufang/"  # 有二手房页面一定有在售页面，不一定有成交页面。
                    item["city_ershoufang_zaishou_href"] = href_zaishou
                    yield scrapy.Request(href_zaishou, self.parse_city_zaishou, meta={"item": item})

    def parse_city_zaishou(self, response):
        item = response.meta["item"]
        ershoufang_zaishou_cnt = response.xpath('//h2[@class="total fl"]/span/text()').get()
        item["city_ershoufang_zaishou"] = ershoufang_zaishou_cnt if ershoufang_zaishou_cnt else None
        href_chengjiao = response.xpath('//div[@class="menuLeft"]/ul[@class="typeList"]/li/a[text()="成交"]/@href').get()
        if href_chengjiao:
            href_chengjiao = response.urljoin(href_chengjiao)
            item["city_ershoufang_chengjiao_href"] = href_chengjiao
            yield scrapy.Request(href_chengjiao, self.parse_city_chengjiao, meta={"item": item})
        else:
            yield item

    def parse_city_chengjiao(self, response):
        item = response.meta["item"]
        ershoufang_chengjiao_cnt = response.xpath('//div[@class="resultDes clear"]/div[@class="total fl"]/span/text()').get()
        item["city_ershoufang_chengjiao"] = ershoufang_chengjiao_cnt if ershoufang_chengjiao_cnt else None
        yield item

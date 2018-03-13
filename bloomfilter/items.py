# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ProxyTestItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class Job51Item(scrapy.Item):
    name = scrapy.Field()
    co_name = scrapy.Field()
    area = scrapy.Field()
    salary = scrapy.Field()
    exp = scrapy.Field()
    edu = scrapy.Field()
    num = scrapy.Field()
    time = scrapy.Field()
    otherq = scrapy.Field()
    welfare = scrapy.Field()
    info = scrapy.Field()
    local = scrapy.Field()
    co_url = scrapy.Field()
    co_type = scrapy.Field()
    spider_name = scrapy.Field() # 爬虫名称
    target_id = scrapy.Field()

class ZhilianItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()       # 职位名称
    co_name = scrapy.Field()    # 公司名称
    area = scrapy.Field()       # 工作区域 （城市）
    salary = scrapy.Field()     # 薪资
    exp = scrapy.Field()        # 经验
    edu = scrapy.Field()        # 学历
    num = scrapy.Field()        # 招聘人数
    time = scrapy.Field()       # 发布时间
    welfare = scrapy.Field()    # 福利
    info = scrapy.Field()       # 职位信息
    local = scrapy.Field()      # 工作地点
    co_type = scrapy.Field()    #公司类别(公司性质)
    co_url = scrapy.Field()      #网址
    spider_name = scrapy.Field() # 爬虫名称
    otherq = scrapy.Field() # 爬虫名称
    #company_local = scrapy.Field() # 公司地址
    target_id = scrapy.Field()


class LiepinItem(scrapy.Item):
    name = scrapy.Field()
    co_name = scrapy.Field()
    area = scrapy.Field()
    salary = scrapy.Field()
    exp = scrapy.Field()
    edu = scrapy.Field()
    num = scrapy.Field()
    time = scrapy.Field()
    otherq = scrapy.Field()
    welfare = scrapy.Field()
    info = scrapy.Field()
    local = scrapy.Field()
    co_url = scrapy.Field()
    co_type = scrapy.Field()
    spider_name = scrapy.Field() # 爬虫名称
    target_id = scrapy.Field()


class LagouItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    co_name = scrapy.Field()
    area = scrapy.Field()
    salary = scrapy.Field()
    exp = scrapy.Field()
    edu = scrapy.Field()
    num = scrapy.Field()
    time = scrapy.Field()
    welfare = scrapy.Field()
    info = scrapy.Field()
    local = scrapy.Field()
    co_url = scrapy.Field()
    co_type = scrapy.Field()
    spider_name = scrapy.Field()
    otherq = scrapy.Field()
    target_id = scrapy.Field()


class BossItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    co_name = scrapy.Field()
    area = scrapy.Field()
    salary = scrapy.Field()
    exp = scrapy.Field()
    edu = scrapy.Field()
    num = scrapy.Field()
    time = scrapy.Field()
    welfare = scrapy.Field()
    info = scrapy.Field()
    local = scrapy.Field()
    co_url = scrapy.Field()
    co_type = scrapy.Field()
    spider_name = scrapy.Field()
    otherq = scrapy.Field()
    target_id = scrapy.Field()



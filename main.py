# -*- coding:utf-8 -*-
import redis
from scrapy import cmdline
from redis_bloom import defaults
print defaults

r = redis.Redis(host=defaults.REDIS_HOST, port=defaults.REDIS_PORT, db=defaults.REDIS_DB)

test = 'https://www.zhipin.com/0'

#if r.llen("boss:start_urls")<1:  # 列表长度
    #r.lpush("boss:start_urls","https://www.zhipin.com")

#cmdline.execute("scrapy crawl boss".split())


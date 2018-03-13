# -*- coding:utf-8 -*-
from scrapy.commands import ScrapyCommand
from scrapy.utils.project import get_project_settings
from redis_bloom import defaults
import redis

r = redis.Redis(host=defaults.REDIS_HOST, port=defaults.REDIS_PORT, db=defaults.REDIS_DB)


class Command(ScrapyCommand):
 
    requires_project = True
 
    def syntax(self):
        return '[options]'
 
    def short_desc(self):
        return 'Runs all of the spiders'
 
    def run(self, args, opts):
        spider_list = self.crawler_process.spiders.list()

        #初始化start_urls
        #if r.llen("zhilian:start_urls")<1:  # 列表长度
            #r.lpush("zhilian:start_urls","http://www.zhaopin.com")
        #self.crawler_process.crawl('fiveone', **opts.__dict__)

        #print(spider_list)
        for name in spider_list:
            startK = name+":start_urls"
            if r.llen(startK)<1:
                r.lpush(startK, defaults.SCHEDULER_RULES[name]['start_url'])
            self.crawler_process.crawl(name, **opts.__dict__)

        self.crawler_process.start()
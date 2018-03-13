# -*- coding: utf-8 -*-

# Scrapy settings for bloomfilter project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'bloomfilter'

SPIDER_MODULES = ['bloomfilter.spiders']
NEWSPIDER_MODULE = 'bloomfilter.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'bloomfilter (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False
# Retry many times since proxies often fail
RETRY_TIMES = 40
DOWNLOAD_TIMEOUT = 10
CONCURRENT_REQUESTS = 8

# Retry on most error codes since proxies fail for different reasons
RETRY_HTTP_CODES = [500, 503, 504, 400, 403, 404, 408]

DOWNLOAD_DELAY = 0.3 # 5,000 ms of delay

DOWNLOADER_MIDDLEWARES = {
                    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware' : None,
                    #'bloomfilter.middlewares.RotateUserAgentMiddleware' : 100,
                    'bloomfilter.middlewares.RandomProxyMiddleware': 200,
                    'scrapy.downloadermiddlewares.retry.RetryMiddleware': 300,
                    'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 400,
                }

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'bloomfilter.middlewares.ProxyTestSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
    #'bloomfilter.middlewares.RandomProxyMiddleware': 543,
#}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    'bloomfilter.pipelines.ProxyTestPipeline': 300,
#}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
ITEM_PIPELINES = {
   # 'job51.pipelines.Job51Pipeline': 300,
   #'redis_bloom.pipelines.RedisPipeline': 999,  # 数据统一存到redis服务器上的 管道文件
   'bloomfilter.pipelines.MysqlTwistedPipeline': 300, #异步保存到mysql
}

# url 过滤 用redis_bloom
DUPEFILTER_CLASS = "redis_bloom.dupefilter.RFPDupeFilter"

# 调度器改成 scrapy-redis 调度器
SCHEDULER = "redis_bloom.scheduler.Scheduler"
# 可以暂停
SCHEDULER_PERSIST = True

# 请求队列模式
SCHEDULER_QUEUE_CLASS = "redis_bloom.queue.SpiderPriorityQueue" # 优先级
# SCHEDULER_QUEUE_CLASS = "redis_bloom.queue.SpiderQueue"  # 队列
# SCHEDULER_QUEUE_CLASS = "redis_bloom.queue.SpiderStack"  # 栈  先进后出
SCHEDULER_DEBUG = True

#同时运行多个
COMMANDS_MODULE = 'bloomfilter.commands'

#mysql数据库配置
MYSQL_HOST = "127.0.0.1"
MYSQL_DBNAME = "zhilian"
MYSQL_USER = "root"
MYSQL_PASSWORD = "123456"
MYSQL_PORT = 9306
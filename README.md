# jobs_scrapy_redis_mysql_bloomfilter
51job,liepin,zhilian,boss,lagou: scrapy_redis_mysqltwisted_bloomfilter_ipproxy_mongo 对scrapy_redis二次开发优化去重和url存储

此项目为scrapy学习项目，尚有诸多地方需要优化。

重点功能：

1. 可以同时爬取spider目录下的多个爬虫，此例中有5个：51job,liepin,zhilian,boss,lagou
配置如下：
SCHEDULER_RULES = {
    'boss':{
        'id':'bs', #两个字符,用于去重前缀判定
        'start_url':'https://www.zhipin.com',
        'refresh_agent':True, #是否更新user agent
        'headers':'', #可以设置个常量, 否则使用第一次
        #爬虫下配置相应url模板，不超过10个
        'base_url':[
            'https://www.zhipin.com/i%s-c%s-p%s/h_%s/?page=%s', #基准url_0
            'https://www.zhipin.com/i%s-c%s/h_%s/?page=%s', #基准url_1
            'https://www.zhipin.com/job_detail/%s.html', #基准url_2 1417413175
        ]
    },
}

2. 随机代理IP（使用的是七夜的IPPROXY），从mongo数据库中随机获取

3. 随机获取USER-AGENT：
- 前期使用scrapy中间件
- 后期因优化redis存储，写在了sheduler里面

4. scrapy_reids配置
- 过滤器使用了bloomfilter：DUPEFILTER_CLASS = "redis_bloom.dupefilter.RFPDupeFilter"
- 调度器改成 scrapy-redis 调度器，SCHEDULER = "redis_bloom.scheduler.Scheduler"
- 为优化内存，pipeline不再存入redis，而是直接异步写入mysql

5. bloomfilter
- 优化fingerprint， 使用前缀+参数的方式
- 优化dont_filter, 每次都要重复爬取得，都不进行过滤算法

6. 配置mysql异步写入
- 对mysql数据库在settings中配置，例如：
    MYSQL_HOST = "127.0.0.1"
    MYSQL_DBNAME = "zhilian"
    MYSQL_USER = "root"
    MYSQL_PASSWORD = "123456"
    MYSQL_PORT = 9306
- 设置pipeline： 'bloomfilter.pipelines.MysqlTwistedPipeline': 300
- 使用mysql连接池插入数据库，这里没有进行分表插入，为了爬取效率，数据后期处理

7. 配置优先级和爬取策略：
- settings配置按请求优先级:SCHEDULER_QUEUE_CLASS = "redis_bloom.queue.SpiderPriorityQueue"
- priority设置：其他页码最低，接着第一页，然后详情页
- 在utils中配置MORE_PAGE， true表示除了第一页还爬其他页，false表示只爬第一页（每日增量）

# -*- coding: utf-8 -*-
import redis

#Conigure Redis Server
REDIS_HOST = '127.0.0.1'
REDIS_PORT = 6379
REDIS_DB = 1

# For standalone use.
DUPEFILTER_KEY = 'dupefilter:%(timestamp)s'

PIPELINE_KEY = '%(spider)s:items'

REDIS_CLS = redis.StrictRedis
REDIS_ENCODING = 'utf-8'

# Sane connection defaults.
REDIS_PARAMS = {
    'socket_timeout': 30,
    'socket_connect_timeout': 30,
    'retry_on_timeout': True,
    'encoding': REDIS_ENCODING,
    'url':'redis://'+REDIS_HOST+':'+str(REDIS_PORT)+'/'+str(REDIS_DB),
    'host':REDIS_HOST,
    'port':REDIS_PORT,
}

SCHEDULER_QUEUE_KEY = '%(spider)s:requests'
SCHEDULER_QUEUE_CLASS = 'redis_bloom.queue.PriorityQueue'

#share dupefilter,not created for each single one
#SCHEDULER_DUPEFILTER_KEY = '%(spider)s:dupefilter'
SCHEDULER_DUPEFILTER_KEY = 'common:dupefilter'
SCHEDULER_DUPEFILTER_CLASS = 'redis_bloom.dupefilter.RFPDupeFilter'

START_URLS_KEY = '%(name)s:start_urls'
START_URLS_AS_SET = False

#定义url规则
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
    'liepin':{
        'id':'lp',
        'start_url':"https://www.liepin.com/zhaopin",
        'refresh_agent':True, #是否更新user agent
        'headers':'', #可以设置个常量, 否则使用第一次
        #爬虫下配置相应url模板，不超过10个
        'base_url':[
            'https://www.liepin.com/zhaopin/?&fromSearchBtn=2&ckid=3ff03f8bf33c6fa6&d_=&&sfrom=click-pc_homepage-centre_searchbox-search_new&init=-1&dqs=%s&industryType=&&&degradeFlag=0&industries=%s&salary=%s&compscale=%s&&&key=&headckid=868e6dec6ba02432&d_pageSize=40&siTag=1B2M2Y8AsgTpgAmY7PhCfg~HjSmCnkUpSjgS7HPdUS6mw&d_headId=e9694c6e8bfe655bfb1a281091ef8886&d_ckId=f186d69a3499a961e77eb21f0be617b0&d_sfrom=search_fp&d_&curPage=%s', #hot city

            'https://www.liepin.com/zhaopin/?&fromSearchBtn=2&ckid=3ff03f8bf33c6fa6&d_=&&sfrom=click-pc_homepage-centre_searchbox-search_new&init=-1&dqs=%s&industryType=&&&degradeFlag=0&salary=%s&compscale=%s&&&key=&headckid=868e6dec6ba02432&d_pageSize=40&siTag=1B2M2Y8AsgTpgAmY7PhCfg~HjSmCnkUpSjgS7HPdUS6mw&d_headId=e9694c6e8bfe655bfb1a281091ef8886&d_ckId=f186d69a3499a961e77eb21f0be617b0&d_sfrom=search_fp&d_&curPage=%s', #normal list

            'https://www.liepin.com/job/%s.shtml' #detailt
        ]
    },
    'fiveone':{
        'id':'fo',
        'start_url':"http://www.51job.com",
        'refresh_agent':True, #是否更新user agent
        'headers':'', #可以设置个常量, 否则使用第一次
        #爬虫下配置相应url模板，不超过10个
        'base_url':[
            'http://search.51job.com/list/%s,000000,0000,00,9,%s,%s,2,%s.html?lang=c&stype=1&postchannel=0000&workyear=99&cotype=99&degreefrom=%s&jobterm=99&companysize=99&lonlat=0%s0&radius=-1&ord_field=0&confirmdate=9&fromType=1&dibiaoid=0&address=&line=&specialarea=00&from=&welfare=', #list

            'http://jobs.51job.com/%s.html' #detail
        ]
    },
    'zhilian':{
        'id':'zl',
        'start_url':"http://www.zhaopin.com",
        'refresh_agent':False, #是否更新user agent
        'headers':{
            # 'Host': 'jobs.zhaopin.com',
            'Connection': 'keep-alive',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8',
        }, 

        #爬虫下配置相应url模板，不超过10个
        'base_url':[
            "http://sou.zhaopin.com/jobs/searchresult.ashx?jl=%s&isadv=0&ct=%s&isfilter=1&et=%s&el=%s&p=%s", #list
            "http://jobs.zhaopin.com/%s.htm" #detail
        ]
    },

    'lagou':{
        'id':'lg',
        'start_url':"https://www.lagou.com",
        'refresh_agent':False, #是否更新user agent
        'headers':{
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Connection': 'keep-alive',
            'Cookie': 'user_trace_token=20170905102116-70d8d5d7-41ad-4135-9a22-cf7539effd8b; LGUID=20170905102117-e6099290-91e0-11e7-85ea-525400f775ce; index_location_city=%E6%88%90%E9%83%BD; JSESSIONID=ABAAABAACBHABBIAAF383376CE201609E3297A0617821EA; hideSliderBanner20180305WithTopBannerC=1; PRE_UTM=; PRE_HOST=; PRE_SITE=; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2F; TG-TRACK-CODE=index_company; _gat=1; _gid=GA1.2.980037332.1520234494; _ga=GA1.2.2123768700.1504578077; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1519439422,1519721843,1519788922,1520234500; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1520234721; LGSID=20180305152138-d8135f5f-2045-11e8-b126-5254005c3644; LGRID=20180305152521-5cfa2796-2046-11e8-9cf2-525400f775ce',
            'Host': 'www.lagou.com',
            'Origin': 'https://www.lagou.com',
            'Referer': 'https://www.lagou.com/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
        }, #手动更新cookie

        #爬虫下配置相应url模板，不超过10个
        'base_url':[
            #"http://sou.zhaopin.com/jobs/searchresult.ashx?jl=%s&isadv=0&ct=%s&isfilter=1&et=%s&el=%s&p=%s", #list
            #"http://jobs.zhaopin.com/%s.htm" #detail
        ]
    },

}

     